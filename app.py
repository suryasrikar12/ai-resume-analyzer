import streamlit as st
import pdfplumber
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---- Page Config ----
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and paste the job description to get AI-powered feedback!")

# ---- PDF Reader Function ----
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# ---- AI Analyzer Function ----
def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an expert HR consultant and resume coach.

Analyze the resume below against the job description and provide:
1. Match Score (out of 100)
2. Matching Skills found in resume
3. Missing Skills the resume lacks
4. 3 Specific improvement suggestions
5. 2 Improved bullet points the candidate can add

Resume:
{resume_text}

Job Description:
{job_description}

Format your response clearly with headings for each section.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ---- UI Layout ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

with col2:
    st.subheader("📝 Job Description")
    job_description = st.text_area("Paste the job description here", height=200)

# ---- Analyze Button ----
if st.button("🔍 Analyze Resume"):
    if not uploaded_file:
        st.warning("Please upload your resume!")
    elif not job_description.strip():
        st.warning("Please paste the job description!")
    else:
        with st.spinner("Analyzing your resume... please wait ⏳"):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume(resume_text, job_description)

        st.success("Analysis Complete! ✅")
        st.markdown("---")
        st.markdown(result)
