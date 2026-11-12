import unittest
from io import StringIO
from contextlib import redirect_stdout

from src.cleaner import clean_phone_numbers


TEST_CONFIG = {
    "phone": {
        "required_digits": 10,
        "country_code": "+91",
        "remove_characters": [" ", "-"]
    }
}


class TestPhoneCleaning(unittest.TestCase):

    def test_phone_cleaning_counts(self):

        records = [
            {"name": "Asha", "phone": "9876543210"},
            {"name": "Ravi", "phone": "+91 98765-43211"},
            {"name": "Neha", "phone": "12345"},
            {"name": "Priya", "phone": ""}
        ]

        output = StringIO()

        with redirect_stdout(output):
            clean_phone_numbers(records, TEST_CONFIG)

        result = output.getvalue()

        self.assertIn("Total Customers: 4", result)
        self.assertIn("Successfully Cleaned: 2", result)
        self.assertIn("Missing Phone Numbers: 1", result)
        self.assertIn("Invalid Phone Numbers: 1", result)


if __name__ == "__main__":
    unittest.main()