# 🛡 AI Job Shield – Fake Job Detector

## Overview

AI Job Shield is a Machine Learning-powered web application designed to identify potentially fraudulent job postings. The system analyzes job descriptions using a trained ML model combined with rule-based fraud detection techniques to provide users with risk insights and scam indicators.

The project aims to help job seekers identify suspicious recruitment activities such as advance fee scams, phishing attempts, fake recruiters, and identity theft schemes.

---

## Features

###  Machine Learning Classification

* Classifies job postings as Genuine or Potentially Fraudulent.
* Provides Fake Probability and Genuine Probability scores.

###  Risk & Confidence Analysis

* Generates Risk Score (0–100).
* Displays Confidence Score and Confidence Level.

###  Explainable AI

* Highlights suspicious indicators detected in the job description.
* Improves transparency of model predictions.

###  Fraud Category Detection

Detects common recruitment scam categories:

* Advance Fee Scam
* Identity Theft
* Fake Recruiter
* Phishing Scam

###  URL Analysis

* Identifies suspicious URLs.
* Detects shortened links such as bit.ly and tinyurl.

###  Email Verification

* Verifies recruitment email domains.
* Flags free email providers used in suspicious job postings.

###  Document Upload Support

* Upload and analyze PDF job descriptions.
* Upload and analyze DOCX job descriptions.

###  Analytics Dashboard

* Total Scans
* Genuine Jobs
* Suspicious Jobs
* Manual Review Cases
* Historical Analysis Data

###  Professional PDF Report

* Generates downloadable analysis reports.
* Includes verdict, risk score, confidence score, and AI explanations.

---

## Tech Stack

### Backend

* Python
* Flask

### Machine Learning

* Scikit-Learn
* Joblib

### Database

* SQLite

### Frontend

* HTML
* CSS
* JavaScript

### Document Processing

* PyPDF2
* python-docx

### Reporting

* ReportLab

### Deployment

* Render

---

## Project Workflow

1. User enters a job description or uploads a PDF/DOCX file.
2. Text is extracted and processed.
3. Machine Learning model predicts authenticity.
4. Rule-based analysis detects scam indicators.
5. Fraud categories, URLs, and email domains are analyzed.
6. Risk score and confidence score are calculated.
7. Results are displayed on the dashboard.
8. User can download a professional PDF report.

---

## Future Improvements

The current version primarily detects fraud based on textual indicators, machine learning predictions, suspicious URLs, email domains, and scam patterns.

Potential future enhancements include:

* Real-time company legitimacy verification
* Advanced NLP-based semantic analysis
* Large Language Model (LLM) integration
* Recruitment website reputation checking
* Domain age verification
* Enhanced phishing detection

---

## Installation

```bash
git clone https://github.com/your-username/fake-job-detector.git
cd fake-job-detector

pip install -r requirements.txt

python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Deployment

The application is deployed on Render.

Live Demo:
(https://fake-job-detector-nw30.onrender.com/))

---

## Author

Naisha Kilaru

Aspiring AI/ML Engineer | Python Developer 

---

## Disclaimer

This project is intended for educational and demonstration purposes. Predictions are based on machine learning models and rule-based analysis and should not be considered a definitive assessment of job authenticity.
