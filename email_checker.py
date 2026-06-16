import re

def verify_email_domains(job_text):

    emails = re.findall(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        job_text
    )

    results = []

    free_domains = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com"
    ]

    for email in emails:

        domain = email.split("@")[1].lower()

        if domain in free_domains:

            results.append(
                f"⚠️ Free Email Provider Detected: {email}"
            )

        else:

            results.append(
                f"✅ Corporate Email Detected: {email}"
            )

    if len(emails) == 0:

        results.append(
            "No recruiter email found."
        )

    return results