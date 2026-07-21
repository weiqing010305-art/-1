import unittest
from decimal import Decimal

from src.main import calculate_simple_interest


class SimpleInterestTests(unittest.TestCase):
    def test_calculates_and_rounds_interest(self) -> None:
        result = calculate_simple_interest(
            Decimal("10000"),
            Decimal("0.035"),
            Decimal("1"),
        )
        self.assertEqual(result, Decimal("350.00"))

    def test_rejects_negative_principal(self) -> None:
        with self.assertRaises(ValueError):
            calculate_simple_interest(
                Decimal("-1"),
                Decimal("0.035"),
                Decimal("1"),
            )


if __name__ == "__main__":
    unittest.main()
