from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import google.generativeai as genai
import os 

app = FastAPI()

# Load Gemini API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory PDF processing
def extract_text_from_pdf(file: UploadFile):
    pdf_bytes = BytesIO(file.file.read())
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "".join([page.get_text() for page in doc])
    return text

@app.post("/analyze/")
async def analyze(resume: UploadFile = File(...), job_description: str = Form("")):
    resume_text = extract_text_from_pdf(resume)
    
    model = genai.GenerativeModel("gemini-2.0-flash")

    # 1. Role Matching (Concise with Bullets)
    role_prompt = f"""
    Analyze the following resume and suggest the top 3 most suitable job roles based on skills, experience, and qualifications.

    For each role, include:
    - **Role Title**
    - **One-line Rationale**
    - **Key Skill Matches** (bulleted)
    - **Relevant Experience** (bulleted)

    Respond in a concise, structured format using bullet points.

    Resume:
    {resume_text}
    """
    role_response = model.generate_content(role_prompt)
    # 2. JD Compatibility (Score, Matches & Gaps in Bullets)
    jd_prompt = f"""
    Compare the resume below to the job description and provide a concise, bullet-formatted analysis.

    Include:
    - **Overall Compatibility Score (0–100%)**
    - **Key Matches** (3–5 bullets)
    - **Missing or Weak Areas** (3–5 bullets)

    Use bullet points and keep the language brief and clear.

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    jd_response = model.generate_content(jd_prompt)
    # 3. Interview Questions (Expanded to 8 with Clear Categories)
    question_prompt = f"""
    Generate 8 concise interview questions based on the resume and job description provided.

    Categories:
    - 2 **Behavioral**
    - 2 **Technical**
    - 2 **Situational**
    - 1 **Resume-Based**
    - 1 **Role-Specific**

    Use bullet points and label each question by category. Keep each question short and direct.

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    question_response = model.generate_content(question_prompt)

    return {
        "role_match": role_response.text,
        "jd_analysis": jd_response.text,
        "interview_questions": question_response.text
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
