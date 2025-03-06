import unittest
from src.a1.a1_ex2 import RateLimiter
from unittest.mock import patch

# Helper class to simulate time progression.
class FakeTime:
    def __init__(self, start=1000.0):
        self.current = start
    def time(self):
        return self.current
    def advance(self, seconds):
        self.current += seconds

class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        self.fake_time = FakeTime()

    def test_initial_calls(self):
        limiter = RateLimiter(3, 5.0)
        with patch('a1_ex2.time.time', new=self.fake_time.time):
            self.assertTrue(limiter())
            self.assertTrue(limiter())
            self.assertTrue(limiter())

    def test_call_limit_reached(self):
        limiter = RateLimiter(3, 5.0)
        with patch('a1_ex2.time.time', new=self.fake_time.time):
            limiter()
            limiter()
            limiter()
            self.assertFalse(limiter())

    def test_calls_after_window(self):
        limiter = RateLimiter(3, 5.0)
        with patch('a1_ex2.time.time', new=self.fake_time.time):
            self.assertTrue(limiter())
            self.assertTrue(limiter())
            self.assertTrue(limiter())
            self.assertFalse(limiter())
            self.fake_time.advance(6)  # Advance beyond the time window.
            self.assertTrue(limiter())

    def test_exact_boundary(self):
        limiter = RateLimiter(3, 5.0)
        with patch('a1_ex2.time.time', new=self.fake_time.time):
            self.assertTrue(limiter())  # At time 1000.0
            self.fake_time.advance(5)     # Time now 1005.0; difference equals 5 (not > 5), so remains.
            self.assertTrue(limiter())    # Second call
            self.assertTrue(limiter())    # Third call
            self.assertFalse(limiter())   # Fourth call should be rejected.
            self.fake_time.advance(0.001)  # Advance slightly so the first call expires.
            self.assertTrue(limiter())

    def test_multiple_cycles(self):
        limiter = RateLimiter(2, 3.0)
        with patch('a1_ex2.time.time', new=self.fake_time.time):
            self.assertTrue(limiter())
            self.assertTrue(limiter())
            self.assertFalse(limiter())
            self.fake_time.advance(4)
            self.assertTrue(limiter())
            self.assertTrue(limiter())
            self.assertFalse(limiter())

    def test_zero_max_calls(self):
        limiter = RateLimiter(0, 5.0)
        with patch('a1_ex2.time.time', new=self.fake_time.time):
            self.assertFalse(limiter())
            self.fake_time.advance(10)
            self.assertFalse(limiter())

    def test_deque_cleanup(self):
        limiter = RateLimiter(3, 5.0)
        with patch('a1_ex2.time.time', new=self.fake_time.time):
            limiter()
            limiter()
            limiter()
            self.assertFalse(limiter())
            self.fake_time.advance(6)
            self.assertTrue(limiter())
            self.assertTrue(limiter())
            self.assertTrue(limiter())

    def test_simultaneous_calls(self):
        limiter = RateLimiter(3, 5.0)
        # All calls occur with the same timestamp.
        with patch('a1_ex2.time.time', new=lambda: 1000.0):
            self.assertTrue(limiter())
            self.assertTrue(limiter())
            self.assertTrue(limiter())
            self.assertFalse(limiter())

    def test_order_of_calls(self):
        limiter = RateLimiter(3, 5.0)
        with patch('a1_ex2.time.time', new=self.fake_time.time):
            t1 = self.fake_time.time()
            self.assertTrue(limiter())
            self.fake_time.advance(1)
            t2 = self.fake_time.time()
            self.assertTrue(limiter())
            self.fake_time.advance(1)
            t3 = self.fake_time.time()
            self.assertTrue(limiter())
            # Check that timestamps are recorded in order.
            self.assertEqual(list(limiter.timestamps), [t1, t2, t3])

    def test_boundary_condition(self):
        limiter = RateLimiter(3, 5.0)
        with patch('a1_ex2.time.time', new=self.fake_time.time):
            self.assertTrue(limiter())
            self.fake_time.advance(5)  # Exactly at the boundary.
            self.assertTrue(limiter())
            self.assertTrue(limiter())
            self.assertFalse(limiter())

if __name__ == '__main__':
    unittest.main()
