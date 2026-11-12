
import unittest
import csv
import os
import tempfile

from src.exporter import export_cleaned_data


class TestExportCleanedData(unittest.TestCase):

    def setUp(self):
        self.original_directory = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.original_directory)
        self.temp_dir.cleanup()

    def test_export_includes_duplicate_combination_columns(self):

        records = [
            {
                "id": "1",
                "name": "Asha",
                "email": "asha@gmail.com",
                "phone": "9876543210",
                "age": "25",
                "city": "Chennai"
            },
            {
                "id": "2",
                "name": "Ravi",
                "email": "ravi@gmail.com",
                "phone": "9876543211",
                "age": "30",
                "city": "Mumbai"
            },
            {
                "id": "3",
                "name": " ASHA ",
                "email": "other@gmail.com",
                "phone": "9876543210",
                "age": "26",
                "city": "Delhi"
            }
        ]

        config = {
            "email": {
                "require_at_symbol": True,
                "require_dot_in_domain": True
            },
            "age": {
                "minimum": 0,
                "maximum": 120
            },
            "phone": {
                "required_digits": 10,
                "country_code": "+91",
                "remove_characters": [" ", "-"]
            },
            "duplicates": {
                "combination_columns": ["name", "phone"]
            }
        }

        export_cleaned_data(records, config)

        # Check whether the exported CSV file exists
        self.assertTrue(os.path.exists("cleaned_data.csv"))

        # Read the exported CSV file
        with open(
            "cleaned_data.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            exported_records = list(csv.DictReader(file))

        # Check whether duplicate combination columns exist
        self.assertIn(
            "Duplicate_Combination_Status",
            exported_records[0]
        )

        self.assertIn(
            "Duplicate_Combination_Issue",
            exported_records[0]
        )

        # Check duplicate detection results
        self.assertEqual(
            exported_records[0]["Duplicate_Combination_Status"],
            "Unique"
        )

        self.assertEqual(
            exported_records[1]["Duplicate_Combination_Status"],
            "Unique"
        )

        self.assertEqual(
            exported_records[2]["Duplicate_Combination_Status"],
            "Duplicate"
        )

        # Check the duplicate explanation
        self.assertIn(
            "row 1",
            exported_records[2]["Duplicate_Combination_Issue"]
        )


    def test_export_skips_records_with_missing_combination_values(self):

        records = [
            {
                "id": "1",
                "name": "Asha",
                "email": "asha@gmail.com",
                "phone": "9876543210",
                "age": "25",
                "city": "Chennai"
            },
            {
                "id": "2",
                "name": "",
                "email": "ravi@gmail.com",
                "phone": "9876543211",
                "age": "30",
                "city": "Mumbai"
            }
        ]

        config = {
            "email": {
                "require_at_symbol": True,
                "require_dot_in_domain": True
            },
            "age": {
                "minimum": 0,
                "maximum": 120
            },
            "phone": {
                "required_digits": 10,
                "country_code": "+91",
                "remove_characters": [" ", "-"]
            },
            "duplicates": {
                "combination_columns": ["name", "phone"]
            }
        }

        export_cleaned_data(records, config)

        with open(
            "cleaned_data.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            exported_records = list(csv.DictReader(file))

        self.assertEqual(
            exported_records[0]["Duplicate_Combination_Status"],
            "Unique"
        )

        self.assertEqual(
            exported_records[1]["Duplicate_Combination_Status"],
            "Skipped"
        )

    def test_export_handles_empty_records(self):

        records = []

        config = {
            "email": {
                "require_at_symbol": True,
                "require_dot_in_domain": True
            },
            "age": {
                "minimum": 0,
                "maximum": 120
            },
            "phone": {
                "required_digits": 10,
                "country_code": "+91",
                "remove_characters": [" ", "-"]
            },
            "duplicates": {
                "combination_columns": ["name", "phone"]
            }
        }

        export_cleaned_data(records, config)

        # Check that no CSV file was created
        self.assertFalse(os.path.exists("cleaned_data.csv"))


if __name__ == "__main__":
    unittest.main()
