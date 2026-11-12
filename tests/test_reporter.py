
import unittest
import os
import tempfile
import json

from src.reporter import generate_quality_report, generate_json_report


class TestQualityReport(unittest.TestCase):

    def test_quality_score_calculation(self):

        records = [
            {
                "email": "rahul@gmail.com",
                "phone": "9876543210",
                "age": "25"
            }
        ]

        config = {
            "email": {
                "require_at_symbol": True,
                "require_dot_in_domain": True
            },
            "age": {
                "minimum": 18,
                "maximum": 100
            },
            "phone": {
                "required_digits": 10,
                "country_code": "+91",
                "remove_characters": [" ", "-", "(", ")"]
            }
        }

        # Create a temporary folder for the report
        with tempfile.TemporaryDirectory() as temp_folder:

            original_folder = os.getcwd()
            os.chdir(temp_folder)

            try:
                generate_quality_report(records, config)

                # Read the generated TXT report
                with open("quality_report.txt", "r", encoding="utf-8") as file:
                    report = file.read()

                # Check whether the score is 100%
                self.assertIn("Data Quality Score: 100.00%", report)

            finally:
                os.chdir(original_folder)

    def test_json_quality_score_calculation(self):

        records = [
            {
                "email": "rahul@gmail.com",
                "phone": "9876543210",
                "age": "25"
            }
        ]

        config = {
            "email": {
                "require_at_symbol": True,
                "require_dot_in_domain": True
            },
            "age": {
                "minimum": 18,
                "maximum": 100
            },
            "phone": {
                "required_digits": 10,
                "country_code": "+91",
                "remove_characters": [" ", "-", "(", ")"]
            }
        }

        # Create a temporary folder for the JSON report
        with tempfile.TemporaryDirectory() as temp_folder:

            original_folder = os.getcwd()
            os.chdir(temp_folder)

            try:
                generate_json_report(records, config)

                # Read the generated JSON report
                with open("quality_report.json", "r", encoding="utf-8") as file:
                    report = json.load(file)

                # Check whether the score is 100%
                self.assertEqual(report["data_quality_score"], 100.0)

            finally:
                os.chdir(original_folder)

    def test_empty_records_quality_score(self):

        records = []

        config = {
            "email": {
                "require_at_symbol": True,
                "require_dot_in_domain": True
            },
            "age": {
                "minimum": 18,
                "maximum": 100
            },
            "phone": {
                "required_digits": 10,
                "country_code": "+91",
                "remove_characters": [" ", "-", "(", ")"]
            }
        }

        with tempfile.TemporaryDirectory() as temp_folder:

            original_folder = os.getcwd()
            os.chdir(temp_folder)

            try:
                generate_quality_report(records, config)
                generate_json_report(records, config)

                # Check TXT report
                with open("quality_report.txt", "r", encoding="utf-8") as file:
                    txt_report = file.read()

                self.assertIn("Data Quality Score: 0.00%", txt_report)

                # Check JSON report
                with open("quality_report.json", "r", encoding="utf-8") as file:
                    json_report = json.load(file)

                self.assertEqual(json_report["data_quality_score"], 0)

            finally:
                os.chdir(original_folder)
if __name__ == "__main__":
    unittest.main()
