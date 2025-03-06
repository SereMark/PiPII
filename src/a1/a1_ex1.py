class Product:
    def __init__(self, name: str, category: str, price: float, rating: float, launch_date: str, in_stock: bool) -> None:
        self.name, self.category, self.price, self.rating, self.launch_date, self.in_stock = name, category, price, rating, launch_date, in_stock

    def __str__(self) -> str:
        return f"{self.name} ({self.category}, {self.rating}, {self.launch_date}) - {self.price}"

def organize_catalog(products: list[Product], mode: str = "cheapest") -> list[Product]:
    if mode == "all":
        return sorted(products, key=lambda p: p.name.lower())
    in_stock = [p for p in products if p.in_stock]
    mapping = {
        "cheapest": (lambda p: p.price, False),
        "best_rated": (lambda p: p.rating, True),
        "newest": (lambda p: p.launch_date, True),
        "category_then_price": (lambda p: (p.category, p.price), False)
    }
    if mode not in mapping:
        raise ValueError("Unknown mode: " + mode)
    key_func, reverse = mapping[mode]
    return sorted(in_stock, key=key_func, reverse=reverse)