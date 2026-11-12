
import csv


def load_csv(file_path):

    try:
        with open(file_path, "r", newline="", encoding="utf-8-sig") as file:

            reader = csv.DictReader(file)

            # Check whether the CSV contains column headers
            if not reader.fieldnames:
                print("Error: CSV file is empty or has no headers.")
                return None

            # Convert CSV records into a list of dictionaries
            records = list(reader)

            print("CSV file loaded successfully!")
            print("Total records:", len(records))
            print("Columns:", reader.fieldnames)

            return records

    except FileNotFoundError:
        print("Error: File not found.")
        return None

    except PermissionError:
        print("Error: You do not have permission to read this file.")
        return None
