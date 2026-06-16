from flask import Flask, render_template, request, send_file
import joblib
import sqlite3
import PyPDF2
from docx import Document

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from rules import analyze_job, detect_scam_patterns

from fraud_categories import detect_fraud_category

from url_checker import analyze_urls

from email_checker import verify_email_domains

app = Flask(__name__)

latest_report = {}

# Load trained model
model = joblib.load("model/fake_job_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    global latest_report

    job_text = request.form.get("job_text", "")

    uploaded_file = request.files.get("job_file")

    if uploaded_file:
        print("Uploaded file:", uploaded_file.filename)

        if uploaded_file.filename.lower().endswith(".pdf"):

            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            extracted_text = ""

            for page in pdf_reader.pages:
                extracted_text += page.extract_text() or ""

            job_text = extracted_text

        elif uploaded_file.filename.lower().endswith(".docx"):

            print("DOCX detected")

            doc = Document(uploaded_file)

            job_text = "\n".join(
                paragraph.text
                for paragraph in doc.paragraphs
        )

        print("Extracted text:")
        print(job_text)

    if not job_text.strip():
        return render_template(
            "index.html",
            prediction="Please enter a job description or upload a PDF."
        )

    # ML Prediction
    prediction = model.predict([job_text])[0]

    # Probability Scores
    probability = model.predict_proba([job_text])[0]

    genuine_prob = round(probability[0] * 100, 2)
    fake_prob = round(probability[1] * 100, 2)

    # Explainable AI
    reasons = analyze_job(job_text)
    scam_patterns = detect_scam_patterns(job_text)
    fraud_categories = detect_fraud_category(job_text)
    url_results = analyze_urls(job_text)
    email_results = verify_email_domains(job_text)

    # Risk Score

    risk_score = round(fake_prob)

    for pattern, score in scam_patterns:
        risk_score += score

    # Fraud Category Risk

    for category in fraud_categories:

        if "Identity Theft" in category:
            risk_score += 35

        elif "Advance Fee Scam" in category:
            risk_score += 40

        elif "Phishing Scam" in category:
            risk_score += 30

        elif "Fake Recruiter" in category:
            risk_score += 25

    # URL Risk

    for item in url_results:

        if "Suspicious URL Found" in item:
            risk_score += 20

    risk_score = min(risk_score, 100)

    # Email Risk

    for item in email_results:

        if "Free Email Provider" in item:
            risk_score += 15

    # Confidence Score
    confidence = round(max(fake_prob, genuine_prob), 2)

    if confidence >= 90:
        confidence_level = "Very High"
    elif confidence >= 75:
        confidence_level = "High"
    elif confidence >= 60:
        confidence_level = "Medium"
    else:
        confidence_level = "Low"


    # Final Verdict
    if risk_score >= 80:
        result = "🚨 Highly Likely Fake Job Posting"

    elif risk_score >= 55:
        result = "⚠️ Suspicious Job Posting"

    elif risk_score >= 35:
        result = "🟡 Needs Manual Review"

    else:
        result = "✅ Genuine Job Posting"


    if len(reasons) == 0:
        reasons.append(
            "No major suspicious indicators were detected."
        )

    # Save Scan History
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO history
        (job_text, verdict, fake_prob, genuine_prob)
        VALUES (?, ?, ?, ?)
        """,
        (
            job_text,
            result,
            fake_prob,
            genuine_prob
        )
    )

    conn.commit()
    conn.close()

    # Quick Analytics

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM history")
    total_scans = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE verdict LIKE '%Genuine%'
    """)
    genuine_jobs = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE verdict LIKE '%Manual%'
    """)
    review_jobs = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE verdict LIKE '%Suspicious%'
        OR verdict LIKE '%Fake%'
    """)
    fake_jobs = cursor.fetchone()[0]

    conn.close()


    latest_report = {
        "verdict": result,
        "fake_prob": fake_prob,
        "genuine_prob": genuine_prob,
        "risk_score": risk_score,
        "confidence": confidence,
        "confidence_level": confidence_level,
        "reasons": reasons
    }

    return render_template(
    "index.html",
    prediction=result,
    fake_prob=fake_prob,
    genuine_prob=genuine_prob,
    confidence=confidence,
    confidence_level=confidence_level,
    risk_score=risk_score,
    scam_patterns=scam_patterns,
    reasons=reasons,

    total_scans=total_scans,
    genuine_jobs=genuine_jobs,
    review_jobs=review_jobs,
    fake_jobs=fake_jobs,
    fraud_categories=fraud_categories,
    url_results=url_results,
    email_results=email_results
    )


@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    # Total Scans
    cursor.execute(
        "SELECT COUNT(*) FROM history"
    )
    total_scans = cursor.fetchone()[0]

    # Genuine Jobs
    cursor.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE verdict LIKE '%Genuine%'
    """)
    genuine_jobs = cursor.fetchone()[0]

    # Manual Review Jobs
    cursor.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE verdict LIKE '%Manual%'
    """)
    review_jobs = cursor.fetchone()[0]

    # Suspicious / Fake Jobs
    cursor.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE verdict LIKE '%Suspicious%'
        OR verdict LIKE '%Fake%'
    """)
    fake_jobs = cursor.fetchone()[0]

    # Average Risk Score
    cursor.execute("""
        SELECT AVG(fake_prob)
        FROM history
    """)

    avg_risk = cursor.fetchone()[0]

    if avg_risk is None:
        avg_risk = 0

    # Recent History
    cursor.execute("""
        SELECT *
        FROM history
        ORDER BY id DESC
        LIMIT 10
    """)

    history = cursor.fetchall()

    conn.close()

    return render_template(
    "dashboard.html",
    total_scans=total_scans,
    genuine_jobs=genuine_jobs,
    review_jobs=review_jobs,
    fake_jobs=fake_jobs,
    avg_risk=round(avg_risk, 2),
    history=history
)

@app.route("/download_report")
def download_report():

    global latest_report

    pdf_file = "Fake_Job_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Fake Job Detector Analysis Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Verdict: {latest_report['verdict']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Fake Probability: {latest_report['fake_prob']}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Genuine Probability: {latest_report['genuine_prob']}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Score: {latest_report['risk_score']}/100",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Confidence Score: {latest_report['confidence']}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Confidence Level: {latest_report['confidence_level']}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "AI Analysis Reasons",
            styles["Heading2"]
        )
    )

    for reason in latest_report["reasons"]:
        content.append(
            Paragraph(
                f"• {reason}",
                styles["Normal"]
            )
        )

    doc.build(content)

    return send_file(
        pdf_file,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)