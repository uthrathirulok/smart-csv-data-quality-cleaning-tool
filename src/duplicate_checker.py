
# DAY 5: Advanced Duplicate Email Detection

def find_duplicate_emails(records):

    seen_emails = set()

    total_records = 0
    unique_count = 0
    duplicate_count = 0
    missing_count = 0
    invalid_count = 0

    print("\nDUPLICATE EMAIL REPORT")
    print("======================")

    for row in records:

        total_records += 1

        name = (row.get("name") or "").strip()
        email = (row.get("email") or "").strip().lower()

        # Skip missing emails
        if email == "":
            missing_count += 1
            continue

        # Basic email format validation
        if email.count("@") != 1:
            invalid_count += 1
            continue

        username, domain = email.split("@")

        if (
            username == ""
            or domain == ""
            or "." not in domain
            or domain.startswith(".")
            or domain.endswith(".")
        ):
            invalid_count += 1
            continue

        # Check duplicate email
        if email in seen_emails:
            print(name, "- Duplicate Email:", email)
            duplicate_count += 1

        else:
            seen_emails.add(email)
            unique_count += 1

    print("\nDUPLICATE SUMMARY")
    print("=================")
    print("Total Records Checked:", total_records)
    print("Unique Valid Emails:", unique_count)
    print("Duplicate Emails Found:", duplicate_count)
    print("Missing Emails:", missing_count)
    print("Invalid Emails Skipped:", invalid_count)


# Find Completely Duplicate Rows

def find_duplicate_rows(records):

    seen_rows = set()
    duplicate_count = 0

    print("\nDUPLICATE ROW REPORT")
    print("====================")

    for row in records:

        row_values = tuple(
            str(value).strip().lower()
            for value in row.values()
        )

        if row_values in seen_rows:
            print("Duplicate Row Found:", row)
            duplicate_count += 1

        else:
            seen_rows.add(row_values)

    print("\nDUPLICATE ROW SUMMARY")
    print("=====================")
    print("Completely Duplicate Rows Found:", duplicate_count)


# Detect Duplicates Using a Combination of Columns

def find_duplicate_combinations(records, config):

    duplicate_rules = config["duplicates"]

    combination_columns = duplicate_rules["combination_columns"]

    if not records:
        print("No records available for duplicate checking.")
        return

    if not combination_columns:
        print("No duplicate combination columns configured.")
        return

    # Check configured columns before processing records
    if not all(
        column in records[0]
        for column in combination_columns
    ):
        print("Error: One or more configured columns are missing.")
        return

    seen_records = {}
    duplicate_count = 0
    skipped_count = 0

    print("\nDUPLICATE COMBINATION REPORT")
    print("============================")

    for row_number, row in enumerate(records, start=1):

        # Normalize values before comparison
        combination = tuple(
            (row.get(column) or "").strip().lower()
            for column in combination_columns
        )

        # Skip records with empty combination values
        if any(value == "" for value in combination):
            skipped_count += 1
            continue

        if combination in seen_records:

            first_row = seen_records[combination]

            print(
                f"Row {row_number} is a duplicate of Row {first_row}"
            )

            print("Matching columns:", combination_columns)

            duplicate_count += 1

        else:
            seen_records[combination] = row_number

    print("\nDUPLICATE COMBINATION SUMMARY")
    print("=============================")
    print("Duplicate Records Found:", duplicate_count)
    print("Records Skipped:", skipped_count)
