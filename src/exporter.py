
import csv


# Export Cleaned Data with Validation Status and Issue Reasons
def export_cleaned_data(records, config):

    if len(records) == 0:
        print("No records available to export.")
        return

    total_records = 0
    seen_emails = []
    seen_combinations = {}

    # Read configuration rules
    email_rules = config["email"]
    age_rules = config["age"]
    phone_rules = config["phone"]

    duplicate_rules = config.get("duplicates", {})
    combination_columns = duplicate_rules.get(
        "combination_columns", []
    )

    minimum_age = age_rules["minimum"]
    maximum_age = age_rules["maximum"]

    required_digits = phone_rules["required_digits"]
    country_code = phone_rules["country_code"]
    remove_characters = phone_rules["remove_characters"]

    # Check whether configured combination columns exist
    combination_columns_available = (
        combination_columns
        and all(
            column in records[0]
            for column in combination_columns
        )
    )

    # Define output columns
    fieldnames = list(records[0].keys())

    new_columns = [
        "Email_Status",
        "Email_Issue",
        "Duplicate_Email_Status",
        "Duplicate_Email_Issue",
        "Duplicate_Combination_Status",
        "Duplicate_Combination_Issue",
        "Phone_Status",
        "Phone_Issue",
        "Age_Status",
        "Age_Issue"
    ]

    for column in new_columns:
        if column not in fieldnames:
            fieldnames.append(column)

    # Create cleaned CSV file
    with open("cleaned_data.csv", "w", newline="", encoding="utf-8") as output_file:

        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for row_number, original_row in enumerate(records, start=1):

            row = original_row.copy()
            total_records += 1

            name = (row.get("name") or "").strip()
            row["name"] = name

            # Email validation
            email = (row.get("email") or "").strip().lower()
            row["email"] = email

            email_issue = ""

            if email == "":
                email_status = "Missing"
                email_issue = "Email field is empty."

            elif email_rules["require_at_symbol"] and "@" not in email:
                email_status = "Invalid"
                email_issue = "Missing @ symbol."

            elif email.count("@") > 1:
                email_status = "Invalid"
                email_issue = "More than one @ symbol."

            else:
                parts = email.split("@")

                if len(parts) != 2:
                    email_status = "Invalid"
                    email_issue = "Incorrect email format."

                elif parts[0] == "":
                    email_status = "Invalid"
                    email_issue = "Email username is missing."

                elif parts[1] == "":
                    email_status = "Invalid"
                    email_issue = "Email domain is missing."

                elif email_rules["require_dot_in_domain"] and "." not in parts[1]:
                    email_status = "Invalid"
                    email_issue = "Domain is missing a dot."

                elif parts[1].startswith(".") or parts[1].endswith("."):
                    email_status = "Invalid"
                    email_issue = "Incorrect dot position in domain."

                else:
                    email_status = "Valid"
                    email_issue = "No issues found."

            # Duplicate email detection
            if email == "":
                duplicate_email_status = "Missing"
                duplicate_email_issue = (
                    "Cannot check duplicate because email is empty."
                )

            elif email.count("@") != 1:
                duplicate_email_status = "Skipped"
                duplicate_email_issue = (
                    "Cannot check duplicate because email format is invalid."
                )

            else:
                username, domain = email.split("@")

                if username == "" or domain == "" or "." not in domain:
                    duplicate_email_status = "Skipped"
                    duplicate_email_issue = (
                        "Cannot check duplicate because email format is invalid."
                    )

                elif email in seen_emails:
                    duplicate_email_status = "Duplicate"
                    duplicate_email_issue = (
                        "Email already exists in another record."
                    )

                else:
                    duplicate_email_status = "Unique"
                    duplicate_email_issue = "No duplicate found."
                    seen_emails.append(email)

            # Duplicate combination detection
            if not combination_columns_available:

                duplicate_combination_status = "Skipped"
                duplicate_combination_issue = (
                    "Configured combination columns are unavailable."
                )

            else:

                combination = tuple(
                    (original_row.get(column) or "").strip().lower()
                    for column in combination_columns
                )

                if any(value == "" for value in combination):

                    duplicate_combination_status = "Skipped"
                    duplicate_combination_issue = (
                        "Cannot check duplicate because one or more "
                        "combination values are missing."
                    )

                elif combination in seen_combinations:

                    first_row = seen_combinations[combination]

                    duplicate_combination_status = "Duplicate"
                    duplicate_combination_issue = (
                        f"Combination already exists in row {first_row}."
                    )

                else:

                    seen_combinations[combination] = row_number

                    duplicate_combination_status = "Unique"
                    duplicate_combination_issue = (
                        "No duplicate combination found."
                    )

            # Phone cleaning and validation
            phone = (row.get("phone") or "").strip()
            cleaned_phone = phone

            for character in remove_characters:
                cleaned_phone = cleaned_phone.replace(character, "")

            if country_code and cleaned_phone.startswith(country_code):
                cleaned_phone = cleaned_phone[len(country_code):]

            phone_issue = ""

            if phone == "":
                phone_status = "Missing"
                phone_issue = "Phone number is empty."

            elif not cleaned_phone.isdigit():
                phone_status = "Invalid"
                phone_issue = "Phone number must contain only digits."

            elif len(cleaned_phone) != required_digits:
                phone_status = "Invalid"
                phone_issue = (
                    f"Phone number must contain {required_digits} digits."
                )

            else:
                phone_status = "Valid"
                phone_issue = "No issues found."
                row["phone"] = cleaned_phone

            # Age validation
            age = (row.get("age") or "").strip()
            age_issue = ""

            if age == "":
                age_status = "Missing"
                age_issue = "Age field is empty."

            else:
                try:
                    age_number = int(age)

                    if age_number < minimum_age or age_number > maximum_age:
                        age_status = "Invalid"
                        age_issue = (
                            f"Age must be between {minimum_age} "
                            f"and {maximum_age}."
                        )

                    else:
                        age_status = "Valid"
                        age_issue = "No issues found."

                except ValueError:
                    age_status = "Invalid"
                    age_issue = "Age must be a numeric value."

            # Add validation statuses and issue explanations
            row["Email_Status"] = email_status
            row["Email_Issue"] = email_issue

            row["Duplicate_Email_Status"] = duplicate_email_status
            row["Duplicate_Email_Issue"] = duplicate_email_issue

            row["Duplicate_Combination_Status"] = (
                duplicate_combination_status
            )
            row["Duplicate_Combination_Issue"] = (
                duplicate_combination_issue
            )

            row["Phone_Status"] = phone_status
            row["Phone_Issue"] = phone_issue

            row["Age_Status"] = age_status
            row["Age_Issue"] = age_issue

            writer.writerow(row)

    print("\nCleaned data exported successfully!")
    print("Total records exported:", total_records)
    print("Output file: cleaned_data.csv")
