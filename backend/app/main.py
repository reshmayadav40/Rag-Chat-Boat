import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router


app = FastAPI(title="RAG Chatbot API")

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
allowed_origins = [frontend_url]
for development_origin in ("http://localhost:5173", "http://127.0.0.1:5173"):
	if development_origin not in allowed_origins:
		allowed_origins.append(development_origin)

app.add_middleware(
	CORSMiddleware,
	allow_origins=allowed_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
	return {"message": "RAG Chatbot API is running"}
