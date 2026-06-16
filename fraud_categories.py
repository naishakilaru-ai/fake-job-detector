def detect_fraud_category(job_text):

    text = job_text.lower()

    categories = []

    # Salary Scam
    salary_words = [
        "earn $5000",
        "earn $10000",
        "guaranteed income",
        "weekly income",
        "quick money"
    ]

    if any(word in text for word in salary_words):
        categories.append("💰 Salary Scam")

    # Advance Fee Fraud
    fee_words = [
        "registration fee",
        "pay fee",
        "security deposit",
        "processing fee",
        "training fee"
    ]

    if any(word in text for word in fee_words):
        categories.append("💳 Advance Fee Fraud")

    # Data Collection Scam
    data_words = [
        "aadhaar",
        "pan card",
        "bank details",
        "credit card",
        "otp"
    ]

    if any(word in text for word in data_words):
        categories.append("🕵️ Data Collection Scam")

    # MLM
    mlm_words = [
        "multi level marketing",
        "referral income",
        "downline",
        "network marketing"
    ]

    if any(word in text for word in mlm_words):
        categories.append("📈 MLM / Pyramid Scheme")

    # Fake Recruiter
    recruiter_words = [
        "gmail.com",
        "yahoo.com",
        "telegram",
        "whatsapp only"
    ]

    if any(word in text for word in recruiter_words):
        categories.append("👤 Fake Recruiter")

    # Work From Home Scam
    wfh_words = [
        "work from home",
        "no experience required",
        "easy typing job",
        "part time income"
    ]

    if any(word in text for word in wfh_words):
        categories.append("🏠 Work From Home Scam")

    if len(categories) == 0:
        categories.append("✅ No Specific Fraud Category Detected")

    return categories