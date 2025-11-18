from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

from schemas import Contact
from database import create_document, get_documents

app = FastAPI(title="New Media API")

# Allow all origins for dev convenience
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "New Media API running"}

@app.get("/test")
def test():
    # Inspect DB status
    try:
        collections = ["contact"]
        docs = {c: len(get_documents(c, limit=1)) for c in collections}
        return {
            "backend": "ok",
            "database": "ok",
            "collections": collections,
            "docs_sampled": docs,
        }
    except Exception as e:
        return {
            "backend": "ok",
            "database": f"error: {e}",
        }

@app.post("/contact")
def submit_contact(payload: Contact):
    try:
        doc_id = create_document("contact", payload.dict(exclude_none=True))
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
