
import json


# DAY 10: Generate Configurable Data Quality Report

def generate_quality_report(records, config):

    total_records = len(records)

    # Read rules from configuration
    email_rules = config["email"]
    age_rules = config["age"]
    phone_rules = config["phone"]

    minimum_age = age_rules["minimum"]
    maximum_age = age_rules["maximum"]

    required_digits = phone_rules["required_digits"]
    country_code = phone_rules["country_code"]
    remove_characters = phone_rules["remove_characters"]

    missing_emails = 0
    invalid_emails = 0
    valid_emails = 0
    duplicate_emails = 0

    missing_phones = 0
    invalid_phones = 0
    valid_phones = 0

    missing_ages = 0
    invalid_ages = 0
    valid_ages = 0

    seen_emails = []
    seen_rows = set()
    duplicate_rows = 0

    for row in records:

        # Completely duplicate row detection
        row_values = tuple(
            str(value or "").strip().lower()
            for value in row.values()
        )

        if row_values in seen_rows:
            duplicate_rows += 1
        else:
            seen_rows.add(row_values)

        email = (row.get("email") or "").strip().lower()
        phone = (row.get("phone") or "").strip()
        age = (row.get("age") or "").strip()

        # Email quality
        if email == "":
            missing_emails += 1
        else:
            parts = email.split("@")
            invalid = False

            if email_rules["require_at_symbol"] and "@" not in email:
                invalid = True

            if len(parts) != 2 or parts[0] == "":
                invalid = True

            elif email_rules["require_dot_in_domain"]:
                domain = parts[1]

                if "." not in domain or domain.startswith(".") or domain.endswith("."):
                    invalid = True

            if invalid:
                invalid_emails += 1
            else:
                valid_emails += 1

            if email in seen_emails:
                duplicate_emails += 1
            else:
                seen_emails.append(email)

        # Phone quality
        cleaned_phone = phone

        for character in remove_characters:
            cleaned_phone = cleaned_phone.replace(character, "")

        if country_code and cleaned_phone.startswith(country_code):
            cleaned_phone = cleaned_phone[len(country_code):]

        if phone == "":
            missing_phones += 1
        elif len(cleaned_phone) == required_digits and cleaned_phone.isdigit():
            valid_phones += 1
        else:
            invalid_phones += 1

        # Age quality
        if age == "":
            missing_ages += 1
        else:
            try:
                age_number = int(age)

                if age_number < minimum_age or age_number > maximum_age:
                    invalid_ages += 1
                else:
                    valid_ages += 1

            except ValueError:
                invalid_ages += 1

    # Calculate Data Quality Score
    total_fields = total_records * 3

    valid_fields = (
        valid_emails +
        valid_phones +
        valid_ages
    )

    # Prevent division by zero
    quality_score = (valid_fields / total_fields) * 100 if total_fields > 0 else 0

    # Build the report
    report = f"""
DATA QUALITY REPORT
===================

Total Records: {total_records}

EMAIL QUALITY
-------------
Valid Emails: {valid_emails}
Invalid Emails: {invalid_emails}
Missing Emails: {missing_emails}
Duplicate Email Occurrences: {duplicate_emails}

PHONE QUALITY
-------------
Valid Phones: {valid_phones}
Invalid Phones: {invalid_phones}
Missing Phones: {missing_phones}

AGE QUALITY
-----------
Valid Ages: {valid_ages}
Invalid Ages: {invalid_ages}
Missing Ages: {missing_ages}

DUPLICATE ROW QUALITY
---------------------
Completely Duplicate Rows: {duplicate_rows}

OVERALL DATA QUALITY SCORE
--------------------------
Data Quality Score: {quality_score:.2f}%
"""

    print(report)

    # Save report to a text file
    with open("quality_report.txt", "w", encoding="utf-8") as file:
        file.write(report)

    print("Report saved successfully!")
    print("Output file: quality_report.txt")


# DAY 11: Generate JSON Data Quality Report

def generate_json_report(records, config):

    total_records = len(records)

    # Read rules from configuration
    email_rules = config["email"]
    age_rules = config["age"]
    phone_rules = config["phone"]

    minimum_age = age_rules["minimum"]
    maximum_age = age_rules["maximum"]

    required_digits = phone_rules["required_digits"]
    country_code = phone_rules["country_code"]
    remove_characters = phone_rules["remove_characters"]

    # Email counters
    missing_emails = 0
    invalid_emails = 0
    valid_emails = 0
    duplicate_emails = 0

    # Phone counters
    missing_phones = 0
    invalid_phones = 0
    valid_phones = 0

    # Age counters
    missing_ages = 0
    invalid_ages = 0
    valid_ages = 0

    # Duplicate row counters
    seen_emails = set()
    seen_rows = set()
    duplicate_rows = 0

    for row in records:

        email = (row.get("email") or "").strip().lower()
        phone = (row.get("phone") or "").strip()
        age = (row.get("age") or "").strip()

        # Completely duplicate row detection
        row_values = tuple(
            str(value or "").strip().lower()
            for value in row.values()
        )

        if row_values in seen_rows:
            duplicate_rows += 1
        else:
            seen_rows.add(row_values)

        # Email quality
        if email == "":
            missing_emails += 1
        else:
            parts = email.split("@")
            invalid = False

            if email_rules["require_at_symbol"] and "@" not in email:
                invalid = True

            if len(parts) != 2 or parts[0] == "":
                invalid = True

            elif email_rules["require_dot_in_domain"]:
                domain = parts[1]

                if "." not in domain or domain.startswith(".") or domain.endswith("."):
                    invalid = True

            if invalid:
                invalid_emails += 1
            else:
                valid_emails += 1

            if email in seen_emails:
                duplicate_emails += 1
            else:
                seen_emails.add(email)

        # Phone quality
        cleaned_phone = phone

        for character in remove_characters:
            cleaned_phone = cleaned_phone.replace(character, "")

        if country_code and cleaned_phone.startswith(country_code):
            cleaned_phone = cleaned_phone[len(country_code):]

        if phone == "":
            missing_phones += 1
        elif len(cleaned_phone) == required_digits and cleaned_phone.isdigit():
            valid_phones += 1
        else:
            invalid_phones += 1

        # Age quality
        if age == "":
            missing_ages += 1
        else:
            try:
                age_number = int(age)

                if age_number < minimum_age or age_number > maximum_age:
                    invalid_ages += 1
                else:
                    valid_ages += 1

            except ValueError:
                invalid_ages += 1

    # Calculate Data Quality Score
    total_fields = total_records * 3

    valid_fields = (
        valid_emails +
        valid_phones +
        valid_ages
    )

    # Prevent division by zero
    quality_score = (valid_fields / total_fields) * 100 if total_fields > 0 else 0

    # Create JSON report data
    report_data = {
        "total_records": total_records,
        "data_quality_score": round(quality_score, 2),

        "email_quality": {
            "valid": valid_emails,
            "invalid": invalid_emails,
            "missing": missing_emails,
            "duplicate_occurrences": duplicate_emails
        },

        "phone_quality": {
            "valid": valid_phones,
            "invalid": invalid_phones,
            "missing": missing_phones
        },

        "age_quality": {
            "valid": valid_ages,
            "invalid": invalid_ages,
            "missing": missing_ages
        },

        "duplicate_row_quality": {
            "completely_duplicate_rows": duplicate_rows
        }
    }

    # Save JSON report to a file
    with open("quality_report.json", "w", encoding="utf-8") as file:
        json.dump(report_data, file, indent=4)

    print("JSON report saved successfully!")
    print("Output file: quality_report.json")
