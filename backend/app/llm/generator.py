import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


FALLBACK_ANSWER = "I couldn't find this information in the provided documents."
SYSTEM_PROMPT = f"""You are a document question-answering assistant.

Answer the user's question using ONLY the provided context.

If the answer is not present in the context, say exactly:
{FALLBACK_ANSWER}

Do not use outside knowledge.
Keep the answer concise and clear."""

APP_DIR = Path(__file__).resolve().parents[1]
load_dotenv(APP_DIR / ".env")


class LLMConfigurationError(RuntimeError):
	"""Raised when the configured LLM provider cannot be used."""


def _build_context(retrieved_documents: list[dict]) -> str:
	context_parts = []
	for document in retrieved_documents:
		source = document.get("source", "unknown")
		page = document.get("page", "unknown")
		text = document.get("text", "").strip()
		context_parts.append(f"[Source: {source}, Page: {page}]\n{text}")

	return "\n\n".join(context_parts)


def _call_gemini_provider(question: str, context: str) -> str:
	api_key = os.getenv("GEMINI_API_KEY")
	model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

	missing = [
		name
		for name, value in (("GEMINI_API_KEY", api_key), ("GEMINI_MODEL", model))
		if not value
	]
	if missing:
		names = ", ".join(missing)
		raise LLMConfigurationError(
			f"Missing LLM configuration: {names}. "
			"Set these variables in backend/app/.env or Render environment variables."
		)

	try:
		client = genai.Client(api_key=api_key)
		response = client.models.generate_content(
			model=model,
			contents=f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion:\n{question}",
		)
	except Exception as error:
		raise RuntimeError(f"LLM provider request failed: {error}") from error

	answer = (response.text or "").strip()

	if not answer:
		raise RuntimeError("LLM provider returned an empty answer")

	return answer


def generate_answer(question: str, retrieved_documents: list[dict]) -> str:
	"""Generate a grounded answer from retrieved document chunks."""
	if not question or not question.strip():
		raise ValueError("Question cannot be empty")

	if not isinstance(retrieved_documents, list) or not retrieved_documents:
		raise ValueError("Retrieved documents cannot be empty")

	context = _build_context(retrieved_documents)
	return _call_gemini_provider(question.strip(), context)
