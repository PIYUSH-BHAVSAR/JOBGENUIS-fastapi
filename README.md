# 🎯 AI Resume Analyzer – Smart Career Intelligence

An AI-powered resume analyzer built with **FastAPI** and **Google Gemini 2.0 Flash**. It helps recruiters and job seekers analyze resumes, get smart job role recommendations, and generate tailored interview questions — all from a single API.

---

## 🚀 Features

- 📄 PDF Resume Parsing  
- 🎯 Smart Job Role Recommendations  
- 📊 Resume-JD Compatibility Score  
- 🎤 Interview Question Generation  
- ⚡ FastAPI backend with async support  
- 🧠 Powered by Google Gemini 2.0 (Flash)

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn, Python 3.8+  
- **AI:** Google Generative AI (Gemini)  
- **PDF Parsing:** PyMuPDF (fitz)  
- **API Docs:** Swagger UI (`/docs`)

---

## ⚡ Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/PIYUSH-BHAVSAR/resume-analyzer.git
cd resume-analyzer
pip install -r requirements.txt
```

### 2. Set Environment Variable

```bash
export GOOGLE_API_KEY=your_api_key
```

### 3. Run the App

```bash
uvicorn app:app --reload
```

- API Docs → `http://localhost:8000/docs`

---

## 🔍 API Endpoint

### `POST /analyze/`

**Inputs:**

- `resume`: PDF file  
- `job_description`: (optional) text string

**Returns:**

- Top 3 job roles with reasoning  
- Resume-JD match score  
- 8 AI-generated interview questions

---

## 📁 File Structure

```
resume-analyzer/
├── app.py
├── requirements.txt
├── README.md
└── .env.example
```

---

## 📌 Demo & Deployment

- 🔗 [Live Demo](#) – Coming soon  
- ☁️ Supports Render, Railway, Docker, and Heroku deployment  
- 🛡️ Environment variable: `GOOGLE_API_KEY`

---

## 👨‍💻 Author

**Piyush Bhavsar**  
📍 SITRC, Nashik  
🔗 [GitHub](https://github.com/PIYUSH-BHAVSAR) | [LinkedIn](https://www.linkedin.com/in/piyush-bhavsar)

---

> ⭐ Star this repo if you find it useful!
