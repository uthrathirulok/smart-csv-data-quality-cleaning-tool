from src.csv_loader import load_csv
from src.validators import validate_emails, validate_ages
from src.duplicate_checker import (
    find_duplicate_emails,
    find_duplicate_rows,
    find_duplicate_combinations
)
from src.reporter import generate_quality_report, generate_json_report
from src.cleaner import clean_phone_numbers
from src.exporter import export_cleaned_data
from src.config_loader import load_config

# Load configuration
config = load_config()


# DAY 4: Find Missing Values
def find_missing_values(records):

    print("\nMISSING VALUES REPORT")
    print("=====================")

    for row in records:

        name = (row.get("name") or "").strip()
        email = (row.get("email") or "").strip()
        phone = (row.get("phone") or "").strip()
        age = (row.get("age") or "").strip()

        if email == "":
            print(name, "- Missing Email")

        if phone == "":
            print(name, "- Missing Phone")

        if age == "":
            print(name, "- Missing Age")


# Select a CSV file provided by the user
def load_selected_csv():

    print("\nSELECT CSV FILE")
    print("================")

    file_path = input(
        "Enter CSV filename or full file path: "
    ).strip().strip('"')

    if file_path == "":
        print("Error: Please enter a CSV file path.")
        return None

    records = load_csv(file_path)

    return records

# MAIN MENU
def display_menu():

    print("\n================================")
    print("       PYTHON DATA CLEANER")
    print("================================")

    print("1. Find Missing Values")
    print("2. Find Duplicate Emails")
    print("3. Validate Email Addresses")
    print("4. Validate Customer Ages")
    print("5. Clean Phone Numbers")
    print("6. Export Cleaned Customer Data")
    print("7. Generate Data Quality Report")
    print("8. Advanced Duplicate Detection")
    print("9. Exit")

    print("================================")


# MAIN PROGRAM

while True:

    display_menu()

    choice = input("Enter your choice (1-9): ").strip()

    
    if choice == "1":
        print("Find Missing Values selected")

        records = load_selected_csv()

        if records is not None:
            find_missing_values(records)
    
    elif choice == "2":
        print("Find Duplicate Emails selected")

        records = load_selected_csv()

        if records is not None:

            if config["duplicates"]["check_email"]:
                find_duplicate_emails(records)

            else:
                print("Duplicate email checking is disabled in config.json.")

    elif choice == "3":
        print("Validate Email Addresses selected")

        records = load_selected_csv()

        if records is not None:
            validate_emails(records, config)

    elif choice == "4":
        print("Validate Customer Ages selected")

        records = load_selected_csv()

        if records is not None:
            validate_ages(records, config)

    elif choice == "5":
        print("Clean Phone Numbers selected")

        records = load_selected_csv()

        if records is not None:
            clean_phone_numbers(records, config)

    elif choice == "6":
        print("Export Cleaned Customer Data selected")

        records = load_selected_csv()

        if records is not None:
            export_cleaned_data(records, config)

    elif choice == "7":
        print("Generate Data Quality Report selected")

        records = load_selected_csv()

        if records is not None:
            generate_quality_report(records, config)
            generate_json_report(records, config)

    elif choice == "8":
        print("Advanced Duplicate Detection selected")

        records = load_selected_csv()

        if records is not None:

            if config["duplicates"]["check_complete_rows"]:
                find_duplicate_rows(records)
            else:
                print("Complete duplicate row checking is disabled.")

            find_duplicate_combinations(records, config)

    elif choice == "9":
        print("Thank you for using Python Data Cleaner!")
        break

    else:
        print("Please enter a valid option between 1 and 9.")
