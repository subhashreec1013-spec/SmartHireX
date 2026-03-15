# semantic_matching.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load small fast model (good balance speed + accuracy)
model = SentenceTransformer('all-MiniLM-L6-v2')


def semantic_similarity(job_desc, resumes):
    """
    Compute semantic similarity using BERT embeddings
    """

    documents = [job_desc] + resumes

    embeddings = model.encode(documents)

    jd_embedding = embeddings[0]
    resume_embeddings = embeddings[1:]

    scores = []

    for emb in resume_embeddings:
        sim = cosine_similarity([jd_embedding], [emb])[0][0]
        scores.append(sim)

    return scores