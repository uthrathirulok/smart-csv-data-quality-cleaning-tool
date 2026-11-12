import unittest
from src.csv_loader import load_csv


class TestCSVLoader(unittest.TestCase):

    def test_load_customers_csv(self):

        records = load_csv("customers.csv")

        self.assertIsNotNone(records)
        self.assertEqual(len(records), 13)

    def test_load_employees_csv(self):

        records = load_csv("employees.csv")

        self.assertIsNotNone(records)
        self.assertEqual(len(records), 3)

    def test_missing_csv(self):

        records = load_csv("unknown_file.csv")

        self.assertIsNone(records)


if __name__ == "__main__":
    unittest.main()