
import streamlit as st
import pandas as pd
import json


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart CSV Data Cleaner",
    page_icon="🧹",
    layout="wide"
)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🧹 Data Cleaner")

menu = st.sidebar.radio(
    "Choose an operation:",
    [
        "Dashboard",
        "Upload & Preview",
        "Missing Values",
        "Duplicate Emails",
        "Email Validation",
        "Age Validation",
        "Phone Cleaning",
        "Data Quality Score",
        "Download Reports"
    ]
)


# --------------------------------------------------
# CSV FILE UPLOAD
# --------------------------------------------------

st.sidebar.subheader("📂 Upload CSV")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

df = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

    except Exception as error:
        st.error(f"Unable to read CSV file: {error}")


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def check_email(email):

    if pd.isna(email) or str(email).strip() == "":
        return "Missing"

    email = str(email).strip()

    if email.count("@") != 1:
        return "Invalid"

    username, domain = email.split("@")

    if not username or not domain:
        return "Invalid"

    if "." not in domain:
        return "Invalid"

    if domain.startswith(".") or domain.endswith("."):
        return "Invalid"

    return "Valid"


def check_age(age):

    if pd.isna(age) or str(age).strip() == "":
        return "Missing"

    try:
        age = int(age)

        if 0 <= age <= 120:
            return "Valid"

        return "Invalid"

    except (ValueError, TypeError):
        return "Invalid"


def clean_phone(phone):

    if pd.isna(phone) or str(phone).strip() == "":
        return "Missing"

    phone = str(phone).strip()

    phone = phone.replace("+91", "")
    phone = phone.replace("-", "")
    phone = phone.replace(" ", "")

    return phone


# --------------------------------------------------
# PREPARE DATA AND VALIDATION RESULTS
# --------------------------------------------------

if df is not None:

    if "email" in df.columns:
        df["Email Status"] = df["email"].apply(check_email)

    if "age" in df.columns:
        df["Age Status"] = df["age"].apply(check_age)

    if "phone" in df.columns:
        df["Cleaned Phone"] = df["phone"].apply(clean_phone)


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if menu == "Dashboard":

    st.title("🧹 Smart CSV Data Quality & Cleaning Tool")

    st.write(
        "Welcome! Use this dashboard to analyze, "
        "validate, and clean your CSV data."
    )

    st.success("Your data cleaning dashboard is ready!")

    st.subheader("Available Features")

    col1, col2, col3 = st.columns(3)

    col1.info("📂 CSV Upload")
    col2.info("🔍 Data Validation")
    col3.info("📊 Quality Score")

    st.markdown("---")

    if df is not None:

        st.subheader("Uploaded Dataset Overview")

        col1, col2 = st.columns(2)

        col1.metric("Total Records", len(df))
        col2.metric("Total Columns", len(df.columns))

    else:
        st.info("Upload a CSV file using the sidebar to get started.")


# --------------------------------------------------
# UPLOAD AND PREVIEW PAGE
# --------------------------------------------------

elif menu == "Upload & Preview":

    st.title("📂 Upload & Preview CSV")

    if df is not None:

        st.success("CSV file uploaded successfully!")

        st.write("File name:", uploaded_file.name)

        st.subheader("📋 CSV Data Preview")

        st.dataframe(df)

    else:
        st.info("Please upload a CSV file using the sidebar.")


# --------------------------------------------------
# MISSING VALUES PAGE
# --------------------------------------------------

elif menu == "Missing Values":

    st.title("🔍 Missing Value Analysis")

    if df is not None:

        missing_values = df.isnull().sum()

        missing_table = (
            missing_values
            .reset_index()
        )

        missing_table.columns = [
            "Column",
            "Missing Count"
        ]

        st.dataframe(
            missing_table,
            use_container_width=True
        )

        total_missing = int(missing_values.sum())

        st.metric(
            "Total Missing Values",
            total_missing
        )

    else:
        st.info("Please upload a CSV file first.")


# --------------------------------------------------
# DUPLICATE EMAIL PAGE
# --------------------------------------------------

elif menu == "Duplicate Emails":

    st.title("🔁 Duplicate Email Detection")

    if df is not None:

        if "email" in df.columns:

            valid_email_mask = (
                df["email"].notna()
                & (df["email"].astype(str).str.strip() != "")
            )

            normalized_emails = (
                df.loc[valid_email_mask, "email"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            duplicate_mask = normalized_emails.duplicated(
                keep=False
            )

            duplicate_indexes = normalized_emails[
                duplicate_mask
            ].index

            duplicate_emails = df.loc[
                duplicate_indexes,
                [col for col in ["name", "email"] if col in df.columns]
            ]

            if not duplicate_emails.empty:

                st.subheader("Duplicate Email Records")

                st.dataframe(
                    duplicate_emails,
                    use_container_width=True
                )

                st.metric(
                    "Duplicate Email Records",
                    len(duplicate_emails)
                )

            else:
                st.success("No duplicate email addresses found!")

        else:
            st.warning("The uploaded CSV does not contain an email column.")

    else:
        st.info("Please upload a CSV file first.")


# --------------------------------------------------
# EMAIL VALIDATION PAGE
# --------------------------------------------------

elif menu == "Email Validation":

    st.title("📧 Email Validation")

    if df is not None:

        if "email" in df.columns:

            result_columns = [
                col for col in ["name", "email", "Email Status"]
                if col in df.columns
            ]

            st.dataframe(
                df[result_columns],
                use_container_width=True
            )

            valid_count = (
                df["Email Status"] == "Valid"
            ).sum()

            invalid_count = (
                df["Email Status"] == "Invalid"
            ).sum()

            missing_count = (
                df["Email Status"] == "Missing"
            ).sum()

            col1, col2, col3 = st.columns(3)

            col1.metric("Valid Emails", int(valid_count))
            col2.metric("Invalid Emails", int(invalid_count))
            col3.metric("Missing Emails", int(missing_count))

        else:
            st.warning("Email column not found.")

    else:
        st.info("Please upload a CSV file first.")


# --------------------------------------------------
# AGE VALIDATION PAGE
# --------------------------------------------------

elif menu == "Age Validation":

    st.title("🎂 Age Validation")

    if df is not None:

        if "age" in df.columns:

            result_columns = [
                col for col in ["name", "age", "Age Status"]
                if col in df.columns
            ]

            st.dataframe(
                df[result_columns],
                use_container_width=True
            )

            valid_count = (
                df["Age Status"] == "Valid"
            ).sum()

            invalid_count = (
                df["Age Status"] == "Invalid"
            ).sum()

            missing_count = (
                df["Age Status"] == "Missing"
            ).sum()

            col1, col2, col3 = st.columns(3)

            col1.metric("Valid Ages", int(valid_count))
            col2.metric("Invalid Ages", int(invalid_count))
            col3.metric("Missing Ages", int(missing_count))

        else:
            st.warning("Age column not found.")

    else:
        st.info("Please upload a CSV file first.")


# --------------------------------------------------
# PHONE CLEANING PAGE
# --------------------------------------------------

elif menu == "Phone Cleaning":

    st.title("📱 Phone Number Cleaning")

    if df is not None:

        if "phone" in df.columns:

            result_columns = [
                col for col in ["name", "phone", "Cleaned Phone"]
                if col in df.columns
            ]

            st.dataframe(
                df[result_columns],
                use_container_width=True
            )

        else:
            st.warning("Phone column not found.")

    else:
        st.info("Please upload a CSV file first.")


# --------------------------------------------------
# DATA QUALITY SCORE PAGE
# --------------------------------------------------

elif menu == "Data Quality Score":

    st.title("📊 Overall Data Quality Score")

    if df is not None:

        fields_to_check = [
            ("Email Status", "Valid"),
            ("Age Status", "Valid"),
            ("Cleaned Phone", None)
        ]

        total_fields = len(df) * len(fields_to_check)

        valid_fields = 0

        if "Email Status" in df.columns:

            valid_fields += (
                df["Email Status"] == "Valid"
            ).sum()

        if "Age Status" in df.columns:

            valid_fields += (
                df["Age Status"] == "Valid"
            ).sum()

        if "Cleaned Phone" in df.columns:

            valid_fields += (
                df["Cleaned Phone"] != "Missing"
            ).sum()

        if total_fields > 0:

            quality_score = (
                valid_fields / total_fields
            ) * 100

        else:
            quality_score = 0

        st.metric(
            "Data Quality Score",
            f"{quality_score:.2f}%"
        )

        st.progress(
            float(quality_score / 100)
        )

        st.write(
            f"Valid fields: {int(valid_fields)} / {total_fields}"
        )

    else:
        st.info("Please upload a CSV file first.")


# --------------------------------------------------
# DOWNLOAD REPORTS PAGE
# --------------------------------------------------

elif menu == "Download Reports":

    st.title("📄 Download Data Quality Reports")

    if df is not None:

        total_records = len(df)

        valid_email_count = (
            int((df["Email Status"] == "Valid").sum())
            if "Email Status" in df.columns else 0
        )

        invalid_email_count = (
            int((df["Email Status"] == "Invalid").sum())
            if "Email Status" in df.columns else 0
        )

        missing_email_count = (
            int((df["Email Status"] == "Missing").sum())
            if "Email Status" in df.columns else 0
        )

        valid_age_count = (
            int((df["Age Status"] == "Valid").sum())
            if "Age Status" in df.columns else 0
        )

        invalid_age_count = (
            int((df["Age Status"] == "Invalid").sum())
            if "Age Status" in df.columns else 0
        )

        missing_age_count = (
            int((df["Age Status"] == "Missing").sum())
            if "Age Status" in df.columns else 0
        )

        valid_phone_count = (
            int((df["Cleaned Phone"] != "Missing").sum())
            if "Cleaned Phone" in df.columns else 0
        )

        total_fields = total_records * 3

        valid_fields = (
            valid_email_count
            + valid_age_count
            + valid_phone_count
        )

        quality_score = (
            valid_fields / total_fields * 100
            if total_fields > 0 else 0
        )

        report_data = {
            "total_records": int(total_records),
            "email_quality": {
                "valid": valid_email_count,
                "invalid": invalid_email_count,
                "missing": missing_email_count
            },
            "age_quality": {
                "valid": valid_age_count,
                "invalid": invalid_age_count,
                "missing": missing_age_count
            },
            "phone_quality": {
                "non_missing": valid_phone_count
            },
            "data_quality_score": round(
                quality_score, 2
            )
        }

        json_report = json.dumps(
            report_data,
            indent=4
        )

        txt_report = f"""
DATA QUALITY REPORT
-------------------

Total Records: {total_records}

EMAIL QUALITY
Valid: {valid_email_count}
Invalid: {invalid_email_count}
Missing: {missing_email_count}

AGE QUALITY
Valid: {valid_age_count}
Invalid: {invalid_age_count}
Missing: {missing_age_count}

PHONE QUALITY
Non-missing: {valid_phone_count}

DATA QUALITY SCORE
{quality_score:.2f}%
"""

        csv_file = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Cleaned CSV",
            data=csv_file,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "📄 Download TXT Report",
                data=txt_report,
                file_name="quality_report.txt",
                mime="text/plain"
            )

        with col2:

            st.download_button(
                "📄 Download JSON Report",
                data=json_report,
                file_name="quality_report.json",
                mime="application/json"
            )

    else:
        st.info("Please upload a CSV file first.")
