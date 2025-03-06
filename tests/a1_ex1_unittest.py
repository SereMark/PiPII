import unittest
from src.a1.a1_ex1 import Product, organize_catalog
from datetime import datetime

class TestCatalogOrganize(unittest.TestCase):
    def setUp(self):
        self.products = [
            Product("Product A", "Books", 10.0, 4.5, "2022-01-01", True),
            Product("Product B", "Electronics", 20.0, 4.7, "2023-06-15", True),
            Product("Product C", "Books", 15.0, 4.5, "2021-12-31", False),  # out of stock
            Product("Product D", "Books", 8.0, 4.5, "2023-01-01", True),
            Product("Product E", "Electronics", 20.0, 4.7, "2022-05-20", True),
            Product("Product F", "Outdoors", 25.0, 4.9, "2023-03-15", False),
        ]

    def test_cheapest_mode(self):
        # Filter out out-of-stock and sort by price ascending.
        result = organize_catalog(self.products, "cheapest")
        prices = [p.price for p in result]
        # In-stock products: A, B, D, E. Sorted by price: D (8.0), A (10.0), B (20.0), E (20.0)
        expected = [8.0, 10.0, 20.0, 20.0]
        self.assertEqual(prices, expected)

    def test_best_rated_mode(self):
        # Filter out out-of-stock and sort by rating descending, tie-break with name.
        result = organize_catalog(self.products, "best_rated")
        ratings = [p.rating for p in result]
        # In-stock: A (4.5), B (4.7), D (4.5), E (4.7) → expect two 4.7 then two 4.5.
        self.assertEqual(ratings, [4.7, 4.7, 4.5, 4.5])
        # Check that for equal ratings the names are in ascending order.
        names = [p.name for p in result if p.rating == 4.7]
        self.assertEqual(names, sorted(names))

    def test_newest_mode(self):
        # Filter out out-of-stock and sort by launch_date descending.
        result = organize_catalog(self.products, "newest")
        dates = [datetime.strptime(p.launch_date, "%Y-%m-%d") for p in result]
        self.assertTrue(all(dates[i] >= dates[i+1] for i in range(len(dates)-1)))

    def test_category_then_price_mode(self):
        # Filter out out-of-stock and sort by category ascending, then price ascending.
        result = organize_catalog(self.products, "category_then_price")
        # In-stock: A (Books, 10.0), D (Books, 8.0), B (Electronics, 20.0), E (Electronics, 20.0)
        # Expect Books sorted by price (D then A) then Electronics.
        self.assertEqual(result[0].name, "Product D")
        self.assertEqual(result[1].name, "Product A")
        self.assertIn(result[2].name, ["Product B", "Product E"])
        self.assertIn(result[3].name, ["Product B", "Product E"])

    def test_all_mode_includes_out_of_stock(self):
        # Mode "all" should include out-of-stock and sort by name (case-insensitive).
        result = organize_catalog(self.products, "all")
        names = [p.name for p in result]
        expected_names = sorted([p.name for p in self.products], key=lambda n: n.lower())
        self.assertEqual(names, expected_names)

    def test_unknown_mode_raises_value_error(self):
        with self.assertRaises(ValueError):
            organize_catalog(self.products, "unknown_mode")

    def test_product_str_method(self):
        p = Product("Test Product", "Category", 99.99, 4.0, "2023-04-01", True)
        expected_str = "Test Product (Category, 4.0, 2023-04-01) - 99.99"
        self.assertEqual(str(p), expected_str)

    def test_filter_all_out_of_stock(self):
        # When all products are out-of-stock, non-"all" modes return an empty list.
        out_of_stock = [Product("X", "Cat", 5.0, 3.0, "2022-01-01", False) for _ in range(3)]
        result = organize_catalog(out_of_stock, "cheapest")
        self.assertEqual(result, [])

    def test_tie_break_best_rated(self):
        # With same ratings, best_rated mode should sort alphabetically.
        products = [
            Product("Alpha", "Cat", 10.0, 4.5, "2023-01-01", True),
            Product("Beta", "Cat", 15.0, 4.5, "2023-01-02", True),
            Product("Gamma", "Cat", 20.0, 4.5, "2023-01-03", True),
        ]
        result = organize_catalog(products, "best_rated")
        names = [p.name for p in result]
        self.assertEqual(names, sorted(names))

    def test_newest_sorting_dates(self):
        # Verify that products with later launch_date come first.
        products = [
            Product("Old", "Cat", 10.0, 4.0, "2020-01-01", True),
            Product("New", "Cat", 15.0, 4.0, "2022-01-01", True),
            Product("Newest", "Cat", 20.0, 4.0, "2023-01-01", True),
        ]
        result = organize_catalog(products, "newest")
        self.assertEqual(result[0].name, "Newest")
        self.assertEqual(result[1].name, "New")
        self.assertEqual(result[2].name, "Old")

if __name__ == '__main__':
    unittest.main()
