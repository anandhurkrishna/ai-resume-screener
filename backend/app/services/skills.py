# Simple skill extraction using keyword matching + spaCy (weak but fast).
import spacy
nlp = spacy.load("en_core_web_sm")

# Start with a seed skill list — expand as needed
SKILL_DB = [
    "python","java","c++","c#","sql","mysql","postgresql","mongodb","redis",
    "fastapi","django","flask","react","vue","angular","docker","kubernetes",
    "aws","azure","gcp","git","linux","pandas","numpy","scikit-learn","tensorflow","pytorch"
]

def extract_skills(text: str):
    text_low = text.lower()
    found = [s for s in SKILL_DB if s in text_low]
    # attempt to get technology-like noun chunks (lightweight)
    doc = nlp(text[:5000])  # limit to speed
    noun_chunks = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 3]
    # combine heuristics
    found_from_chunks = []
    for sk in SKILL_DB:
        for chunk in noun_chunks:
            if sk in chunk.lower():
                found_from_chunks.append(sk)
    skills = list(set(found + found_from_chunks))
    return skills