from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once (may take time on first run)
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def embed_text(text: str):
    # optionally truncate very long text or chunk and average; for simplicity we encode the whole text
    vec = model.encode([text], convert_to_numpy=True)[0]
    return vec  # numpy array

def cosine_similarity(a, b):
    # a, b are numpy arrays
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    return float(np.dot(a,b)/denom)