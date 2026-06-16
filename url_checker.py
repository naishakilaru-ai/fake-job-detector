import re

def analyze_urls(job_text):

    urls = re.findall(
        r'https?://[^\s]+',
        job_text
    )

    findings = []

    suspicious_domains = [
        "bit.ly",
        "tinyurl.com",
        "t.me",
        "telegram.me",
        "shorturl"
    ]

    for url in urls:

        if any(domain in url.lower()
               for domain in suspicious_domains):

            findings.append(
                f"⚠️ Suspicious URL Found: {url}"
            )

        else:

            findings.append(
                f"✅ URL Found: {url}"
            )

    if len(urls) == 0:

        findings.append(
            "No URLs detected in job description."
        )

    return findings