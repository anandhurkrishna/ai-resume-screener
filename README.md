AI Resume Screener

An AI-powered resume screening tool that intelligently analyzes resumes, extracts key details (like name, email, phone number, skills, and experience), and compares them with a given job description to identify the best-fit candidates.


🚀 Features

Automatic Resume Parsing: Extracts important details using Natural Language Processing (NLP).

Skill Matching: Compares candidate skills with job requirements using similarity algorithms.

FastAPI Backend: Handles file upload, text extraction, and AI-based analysis.

React Frontend: Simple and interactive UI for uploading resumes and viewing match results.

Multi-format Support: Works with PDF, DOCX, and text files.

Deployable on Render: Easily deployable full-stack setup using render.yaml.


🧩 Tech Stack

Frontend: React.js,vite
Backend: FastAPI, Python
AI/NLP: spaCy / scikit-learn / transformers (depending on implementation)
Database: MongoDB
Deployment: Render


⚙ How It Works

1. User uploads a resume (PDF/DOCX).


2. The backend extracts text and uses NLP to identify personal details and skills.


3. The job description is compared with extracted data to compute a match score.


4. The frontend displays the candidate details and key skills.


🧑‍💻 Installation & Setup

1. Clone the Repository

git clone https://github.com/anandhurkrishna/ai-resume-screener.git
cd ai-resume-screener

2. Backend Setup

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

3. Frontend Setup

cd frontend
npm install
npm run dev

Then open http://localhost:5173 in your browser.


🌐 Deployment on Render

The project includes a render.yaml for automatic deployment.

Both FastAPI backend and React frontend can be deployed as separate services under one Render account.


🧑‍🎨 Author

Created by: Anandhu Krishnan R
💼 MCA Student | AI & ML Enthusiast | Full Stack Developer


🏷 License

This project is licensed under the MIT License.