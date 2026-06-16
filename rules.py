def analyze_job(text):

    reasons = []
    text = text.lower()

    # 🔴 Keyword-based checks
    if "urgent" in text:
        reasons.append("⚠ Mentions urgent hiring")

    if "work from home" in text:
        reasons.append("⚠ Remote offer without verification")

    if "$" in text and "experience" not in text:
        reasons.append("⚠ Salary mentioned without requirements")

    # 🔴 Suspicious phrases
    suspicious_phrases = [
        "urgent hiring",
        "quick money",
        "earn money",
        "easy income",
        "no experience",
        "work from home",
        "immediate joining",
        "guaranteed income",
        "limited vacancies",
        "apply now"
    ]

    for phrase in suspicious_phrases:
        if phrase in text:
            reasons.append(f"⚠ Contains suspicious phrase: {phrase}")

    # 🔴 Contact-based checks
    if "gmail.com" in text:
        reasons.append("⚠ Uses personal Gmail address")

    if "yahoo.com" in text:
        reasons.append("⚠ Uses personal Yahoo email")

    if "whatsapp" in text:
        reasons.append("⚠ Contains WhatsApp contact information")

    # 🔴 Length check
    if len(text.split()) < 50:
        reasons.append("⚠ Job description is unusually short")

    # If nothing found
    if not reasons:
        reasons.append("✅ No strong suspicious signals detected")

    return reasons

def detect_scam_patterns(job_text):

    patterns = []

    text = job_text.lower()

    if any(word in text for word in [
        "registration fee",
        "processing fee",
        "training fee",
        "pay fee"
    ]):
        patterns.append(("💳 Payment Request", 40))

    if any(word in text for word in [
        "telegram",
        "whatsapp only",
        "contact on telegram"
    ]):
        patterns.append(("📱 Suspicious Contact Method", 25))

    if any(word in text for word in [
        "$5000 per week",
        "$10000 per month",
        "guaranteed income",
        "earn money fast"
    ]):
        patterns.append(("💰 Unrealistic Salary Promise", 20))

    if any(word in text for word in [
        "immediate joining",
        "urgent hiring",
        "limited slots"
    ]):
        patterns.append(("⚠️ Urgency Pressure", 15))

    if any(word in text for word in [
        "bank account",
        "aadhaar",
        "social security",
        "passport copy"
    ]):
        patterns.append(("🪪 Sensitive Personal Information Request", 35))

    return patterns