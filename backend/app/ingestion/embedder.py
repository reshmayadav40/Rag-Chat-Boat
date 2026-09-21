import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


APP_DIR = Path(__file__).resolve().parents[1]
load_dotenv(APP_DIR / ".env")

MODEL_NAME = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
_client: OpenAI | None = None


def _get_client() -> OpenAI:
	global _client

	if _client is None:
		api_key = os.getenv("OPENAI_API_KEY")
		base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
		if not api_key:
			raise RuntimeError("OPENAI_API_KEY is required for embeddings")
		_client = OpenAI(api_key=api_key, base_url=base_url)

	return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
	"""Generate one embedding vector for each input text."""
	if not texts:
		return []

	response = _get_client().embeddings.create(model=MODEL_NAME, input=texts)
	return [item.embedding for item in response.data]


def embed_text(text: str) -> list[float]:
	"""Generate an embedding vector for one input text."""
	return embed_texts([text])[0]
