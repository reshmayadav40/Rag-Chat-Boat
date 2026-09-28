import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


APP_DIR = Path(__file__).resolve().parents[1]
load_dotenv(APP_DIR / ".env")

MODEL_NAME = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
_client: genai.Client | None = None


def _get_client() -> genai.Client:
	global _client

	if _client is None:
		api_key = os.getenv("GEMINI_API_KEY")
		if not api_key:
			raise RuntimeError("GEMINI_API_KEY is required for embeddings")
		_client = genai.Client(api_key=api_key)

	return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
	"""Generate one embedding vector for each input text."""
	if not texts:
		return []

	response = _get_client().models.embed_content(model=MODEL_NAME, contents=texts)
	return [embedding.values for embedding in response.embeddings]


def embed_text(text: str) -> list[float]:
	"""Generate an embedding vector for one input text."""
	return embed_texts([text])[0]
