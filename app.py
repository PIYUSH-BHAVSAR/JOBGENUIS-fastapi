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


def extract_text_from_pdf(file: UploadFile):
    doc = fitz.open(stream=file.file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.post("/analyze/")
async def analyze(resume: UploadFile = File(...), job_description: str = Form("")):
    try:
        resume_text = extract_text_from_pdf(resume)

        model = genai.GenerativeModel("gemini-2.0-flash")

        # 1. Role Matching
        role_prompt = f"""
        Analyze the following resume and suggest the top 3 most suitable job roles...

        Resume:
        {resume_text}
        """
        role_response = model.generate_content(role_prompt)

        # 2. JD Compatibility
        jd_prompt = f"""
        Compare the resume below to the job description...

        Resume:
        {resume_text}

        Job Description:
        {job_description}
        """
        jd_response = model.generate_content(jd_prompt)

        # 3. Interview Questions
        question_prompt = f"""
        Generate 8 concise interview questions...

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
    finally:
        # Explicitly close the uploaded file stream (important for cleanup in production)
            resume.file.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
