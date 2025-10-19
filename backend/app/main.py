from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import docx
import re
from keybert import KeyBERT
import spacy

app = FastAPI(title="AI Resume Screener – Smart Filtered")

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load NLP models
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

# 🎯 Curated tech keyword list
TECH_TERMS = [
    "python", "java", "javascript", "typescript", "react", "redux", "node", "node.js",
    "express", "mongodb", "mysql", "postgresql", "html", "css", "tailwind", "next.js",
    "vite", "webpack", "docker", "kubernetes", "aws", "azure", "git", "github",
    "flask", "django", "rest api", "fastapi", "machine learning", "deep learning",
    "nlp", "tensorflow", "pytorch", "data science", "sql", "nosql", "firebase",
    "linux", "bash", "c++", "c#", "devops", "pandas", "numpy", "scikit-learn",
    "opencv", "powerbi", "tableau", "spark", "hadoop"
]

def extract_name(text: str):
    """Extract candidate name with NLP + precise rule handling."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    TECH_WORDS = [t.lower() for t in TECH_TERMS]

    # --- Step 1: Look for "Name: ..." line ---
    for line in lines:
        match = re.match(r"(?i)^name\s*[:\-]\s*([A-Za-z\s\.]+)$", line)
        if match:
            candidate = match.group(1).strip()
            # Stop if next line starts with "Role", "Email", "Contact", etc.
            if len(candidate.split()) <= 4 and not any(
                w in candidate.lower() for w in ["resume", "developer", "role", "projects", "profile", "engineer"]
            ):
                return candidate

    # --- Step 2: Use PERSON entity from spaCy ---
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            candidate = ent.text.strip()
            if (
                2 <= len(candidate) <= 40
                and len(candidate.split()) <= 3
                and candidate.lower() not in TECH_WORDS
                and not any(x in candidate.lower() for x in ["resume", "developer", "projects", "role", "profile", "engineer"])
            ):
                return candidate

    # --- Step 3: Top-line fallback (first few lines) ---
    for line in lines[:6]:
        if re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+){0,2}$", line):
            if line.lower() not in TECH_WORDS and not any(
                bad in line.lower() for bad in ["resume", "developer", "projects", "role", "profile", "engineer"]
            ):
                return line.strip()

    return "Unknown"

def extract_text(file: UploadFile):
    """Extract text from PDF or DOCX."""
    text = ""
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def extract_info(text: str):
    """Extract structured resume info."""
    name = extract_name(text)
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", text)
    phone = re.search(r"\+?\d[\d \-]{8,12}\d", text)

    # AI-based keyword extraction
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=40)
    keybert_skills = [kw[0].lower().strip() for kw in keywords]

    # NLP noun chunk fallback
    doc = nlp(text)
    noun_chunks = [chunk.text.lower().strip() for chunk in doc.noun_chunks]
    combined = list(set(keybert_skills + noun_chunks))

    # Smart filtering using TECH_TERMS
    detected_skills = []
    for skill in TECH_TERMS:
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE):
            detected_skills.append(skill)
        elif any(skill in kw for kw in combined):
            detected_skills.append(skill)

    unique_skills = sorted(set(detected_skills))
    cleaned_skills = [s.title() for s in unique_skills]

    return {
        "name": name,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "skills": cleaned_skills
    }

@app.post("/api/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text(file)
    info = extract_info(text)
    return {"filename": file.filename,"info":info}