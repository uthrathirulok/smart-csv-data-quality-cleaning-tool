import unittest
from io import StringIO
from contextlib import redirect_stdout

from src.validators import validate_emails, validate_ages


# Test configuration
TEST_CONFIG = {
    "email": {
        "require_at_symbol": True,
        "require_dot_in_domain": True
    },
    "age": {
        "minimum": 0,
        "maximum": 120
    }
}


class TestEmailValidation(unittest.TestCase):

    def test_email_validation_counts(self):

        records = [
            {"name": "Asha", "email": "asha@gmail.com"},
            {"name": "Ravi", "email": "ravi.gmail.com"},
            {"name": "Neha", "email": ""}
        ]

        output = StringIO()

        with redirect_stdout(output):
            validate_emails(records, TEST_CONFIG)

        result = output.getvalue()

        self.assertIn("Valid Emails: 1", result)
        self.assertIn("Invalid Emails: 1", result)
        self.assertIn("Missing Emails: 1", result)
    
    def test_email_without_at_symbol_when_not_required(self):

        records = [
            {"name": "Test User", "email": "plainaddress"}
        ]

        config = {
            "email": {
                "require_at_symbol": False,
                "require_dot_in_domain": False
            }
        }

        output = StringIO()

        with redirect_stdout(output):
            validate_emails(records, config)

        result = output.getvalue()

        self.assertIn("Valid Emails: 1", result)
        self.assertIn("Invalid Emails: 0", result)


class TestAgeValidation(unittest.TestCase):

    def test_age_validation_counts(self):

        records = [
            {"name": "Asha", "age": "25"},
            {"name": "Ravi", "age": "150"},
            {"name": "Neha", "age": "abc"},
            {"name": "Priya", "age": ""}
        ]

        output = StringIO()

        with redirect_stdout(output):
            validate_ages(records, TEST_CONFIG)

        result = output.getvalue()

        self.assertIn("Valid Ages: 1", result)
        self.assertIn("Invalid Ages: 2", result)
        self.assertIn("Missing Ages: 1", result)


if __name__ == "__main__":
    unittest.main()