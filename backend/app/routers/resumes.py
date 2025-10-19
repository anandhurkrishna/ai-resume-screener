from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.parser import parse_resume_bytes
from app.services.embeddings import embed_text, cosine_similarity
from app.services.skills import extract_skills
from app.models import UploadResponse, MatchRequest
from app.db import db
import datetime
import numpy as np
from bson import ObjectId

router = APIRouter()

@router.post("/upload_resume", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    text = await parse_resume_bytes(contents, file.filename)
    if not text:
        raise HTTPException(status_code=400, detail="Could not parse resume text.")
    skills = extract_skills(text)
    # create embedding (optionally truncate to first N chars for speed)
    emb = embed_text(text[:20000])  # keep a safe max length
    doc = {
        "filename": file.filename,
        "text": text,
        "skills": skills,
        "embedding": emb.tolist(),   # store as list of floats
        "uploaded_at": datetime.datetime.utcnow()
    }
    res = await db.resumes.insert_one(doc)
    return {"id": str(res.inserted_id)}

@router.post("/match_job")
async def match_job(req: MatchRequest):
    job_emb = embed_text(req.job_description)
    # get resumes that have embeddings
    cursor = db.resumes.find({"embedding": {"$exists": True}})
    resumes = await cursor.to_list(length=None)
    results = []
    for r in resumes:
        emb = np.array(r["embedding"])
        score = cosine_similarity(job_emb, emb)
        results.append({
            "id": str(r["_id"]),
            "filename": r.get("filename"),
            "score": score,
            "skills": r.get("skills", [])
        })
    # sort
    results.sort(key=lambda x: x["score"], reverse=True)
    return {"matches": results[: req.top_k ]}

@router.get("/resume/{resume_id}")
async def get_resume(resume_id: str):
    try:
        oid = ObjectId(resume_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")
    doc = await db.resumes.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc