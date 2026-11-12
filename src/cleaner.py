# DAY 8: Clean Phone Numbers using configuration
def clean_phone_numbers(records, config):

    total_customers = 0
    cleaned_count = 0
    missing_count = 0
    invalid_count = 0

    # Read phone rules from configuration
    phone_rules = config["phone"]

    required_digits = phone_rules["required_digits"]
    country_code = phone_rules["country_code"]
    remove_characters = phone_rules["remove_characters"]

    print("\nPHONE NUMBER CLEANING REPORT")
    print("============================")

    for row in records:

        total_customers += 1

        name = (row.get("name") or "").strip()
        original_phone = (row.get("phone") or "").strip()

        if original_phone == "":
            print(name, "- Missing Phone")
            missing_count += 1
            continue

        cleaned_phone = original_phone

        # Remove configured characters
        for character in remove_characters:
            cleaned_phone = cleaned_phone.replace(character, "")

        # Remove configured country code
        if country_code and cleaned_phone.startswith(country_code):
            cleaned_phone = cleaned_phone[len(country_code):]

        # Validate using configured digit count
        if len(cleaned_phone) == required_digits and cleaned_phone.isdigit():
            print(name, "- Original:", original_phone)
            print(name, "- Cleaned:", cleaned_phone)
            cleaned_count += 1
        else:
            print(name, "- Invalid Phone:", original_phone)
            print(
                f"Reason: Phone number must contain exactly {required_digits} digits."
            )
            invalid_count += 1

    print("\nPHONE NUMBER CLEANING SUMMARY")
    print("==============================")
    print("Total Customers:", total_customers)
    print("Successfully Cleaned:", cleaned_count)
    print("Missing Phone Numbers:", missing_count)
    print("Invalid Phone Numbers:", invalid_count)