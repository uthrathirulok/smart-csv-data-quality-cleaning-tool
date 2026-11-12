
import unittest
from io import StringIO
from contextlib import redirect_stdout

from src.duplicate_checker import (
    find_duplicate_emails,
    find_duplicate_rows,
    find_duplicate_combinations
)


class TestDuplicateEmails(unittest.TestCase):

    def test_duplicate_email_detection(self):

        records = [
            {"name": "Asha", "email": "asha@gmail.com"},
            {"name": "Ravi", "email": "ravi@gmail.com"},
            {"name": "Neha", "email": "RAVI@GMAIL.COM"},
            {"name": "Priya", "email": "asha@gmail.com"}
        ]

        output = StringIO()

        with redirect_stdout(output):
            find_duplicate_emails(records)

        result = output.getvalue()

        self.assertIn("Duplicate Emails Found: 2", result)

    def test_email_normalization_and_invalid_emails(self):

        records = [
            {"name": "Asha", "email": "  ASHA@GMAIL.COM  "},
            {"name": "Ravi", "email": "asha@gmail.com"},
            {"name": "Neha", "email": ""},
            {"name": "Sam", "email": "invalid-email"}
        ]

        output = StringIO()

        with redirect_stdout(output):
            find_duplicate_emails(records)

        result = output.getvalue()

        self.assertIn("Duplicate Emails Found: 1", result)
        self.assertIn("Missing Emails: 1", result)
        self.assertIn("Invalid Emails Skipped: 1", result)


class TestDuplicateRows(unittest.TestCase):

    def test_duplicate_row_detection(self):

        records = [
            {
                "id": "1",
                "name": "Arun",
                "email": "arun@gmail.com",
                "phone": "9876543210",
                "age": "25",
                "city": "Chennai"
            },
            {
                "id": "2",
                "name": "Priya",
                "email": "priya@gmail.com",
                "phone": "9876543211",
                "age": "26",
                "city": "Mumbai"
            },
            {
                "id": "1",
                "name": "Arun",
                "email": "arun@gmail.com",
                "phone": "9876543210",
                "age": "25",
                "city": "Chennai"
            }
        ]

        output = StringIO()

        with redirect_stdout(output):
            find_duplicate_rows(records)

        result = output.getvalue()

        self.assertIn("Duplicate", result)


class TestDuplicateCombinations(unittest.TestCase):

    def test_duplicate_combination_detection(self):

        records = [
            {
                "name": "Asha",
                "phone": "9876543210"
            },
            {
                "name": "Ravi",
                "phone": "9876543211"
            },
            {
                "name": " ASHA ",
                "phone": "9876543210"
            }
        ]

        config = {
            "duplicates": {
                "combination_columns": ["name", "phone"]
            }
        }

        output = StringIO()

        with redirect_stdout(output):
            find_duplicate_combinations(records, config)

        result = output.getvalue()

        self.assertIn("Row 3 is a duplicate of Row 1", result)
        self.assertIn("Duplicate Records Found: 1", result)
        self.assertIn("Records Skipped: 0", result)

    def test_missing_values_in_duplicate_combinations(self):

        records = [
            {
                "name": "Asha",
                "phone": "9876543210"
            },
            {
                "name": "",
                "phone": "9876543211"
            },
            {
                "name": "Ravi",
                "phone": ""
            },
            {
                "name": "Priya",
                "phone": "9876543212"
            }
        ]

        config = {
            "duplicates": {
                "combination_columns": ["name", "phone"]
            }
        }

        output = StringIO()

        with redirect_stdout(output):
            find_duplicate_combinations(records, config)

        result = output.getvalue()

        self.assertIn("Duplicate Records Found: 0", result)
        self.assertIn("Records Skipped: 2", result)


if __name__ == "__main__":
    unittest.main()
