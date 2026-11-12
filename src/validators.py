
# Validate Email Addresses using configuration

# Validate Email Addresses using configuration
def validate_emails(records, config):

    valid_emails = 0
    invalid_emails = 0
    missing_emails = 0

    email_rules = config["email"]

    print("\nEMAIL VALIDATION REPORT")
    print("=======================")

    for row in records:

        name = (row.get("name") or "").strip()
        email = (row.get("email") or "").strip().lower()

        if email == "":
            print(name, "- Missing Email")
            print("Reason: Email field is empty.")
            missing_emails += 1
            continue

        reason = None

        if "@" not in email:

            if email_rules["require_at_symbol"]:
                reason = "Missing @ symbol."

            elif email_rules["require_dot_in_domain"]:
                reason = "Cannot check domain because @ is missing."

        elif email.count("@") > 1:
            reason = "Email contains more than one @ symbol."

        else:
            parts = email.split("@")

            if parts[0] == "":
                reason = "Email username is missing."

            elif parts[1] == "":
                reason = "Email domain is missing."

            elif email_rules["require_dot_in_domain"]:
                domain = parts[1]

                if "." not in domain:
                    reason = "Domain is missing a dot."

                elif domain.startswith(".") or domain.endswith("."):
                    reason = "Domain has an incorrect dot position."

        if reason:
            print(name, "- Invalid Email:", email)
            print("Reason:", reason)
            invalid_emails += 1

        else:
            print(name, "- Valid Email")
            valid_emails += 1

    print("\nEMAIL VALIDATION SUMMARY")
    print("========================")
    print("Valid Emails:", valid_emails)
    print("Invalid Emails:", invalid_emails)
    print("Missing Emails:", missing_emails)


# Validate Customer Ages using configuration
def validate_ages(records, config):

    valid_ages = 0
    invalid_ages = 0
    missing_ages = 0

    age_rules = config["age"]

    minimum_age = age_rules["minimum"]
    maximum_age = age_rules["maximum"]

    print("\nAGE VALIDATION REPORT")
    print("=====================")

    for row in records:

        name = (row.get("name") or "").strip()
        age = (row.get("age") or "").strip()

        if age == "":
            print(name, "- Missing Age")
            missing_ages += 1
            continue

        try:
            age = int(age)

            if age < minimum_age or age > maximum_age:
                print(name, "- Invalid Age:", age)
                print(
                    f"Reason: Age must be between {minimum_age} and {maximum_age}."
                )
                invalid_ages += 1
            else:
                print(name, "- Valid Age:", age)
                valid_ages += 1

        except ValueError:
            print(name, "- Invalid Age: Not a number")
            invalid_ages += 1

    print("\nAGE VALIDATION SUMMARY")
    print("======================")
    print("Valid Ages:", valid_ages)
    print("Invalid Ages:", invalid_ages)
    print("Missing Ages:", missing_ages)
