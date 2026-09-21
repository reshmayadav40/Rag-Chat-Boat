import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


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


def _call_openai_compatible_provider(question: str, context: str) -> str:
	api_key = os.getenv("OPENAI_API_KEY")
	model = os.getenv("OPENAI_MODEL")
	base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")

	missing = [
		name
		for name, value in (("OPENAI_API_KEY", api_key), ("OPENAI_MODEL", model))
		if not value
	]
	if missing:
		names = ", ".join(missing)
		raise LLMConfigurationError(
			f"Missing LLM configuration: {names}. "
			"Set these variables in backend/app/.env."
		)

	try:
		client = OpenAI(api_key=api_key, base_url=base_url)
		response = client.chat.completions.create(
			model=model,
			messages=[
				{"role": "system", "content": SYSTEM_PROMPT},
				{
					"role": "user",
					"content": f"Context:\n{context}\n\nQuestion:\n{question}",
				},
			],
		)
	except Exception as error:
		raise RuntimeError(f"LLM provider request failed: {error}") from error

	try:
		answer = response.choices[0].message.content.strip()
	except (KeyError, IndexError, TypeError, AttributeError) as error:
		raise RuntimeError("LLM provider returned an unexpected response format") from error

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
	return _call_openai_compatible_provider(question.strip(), context)
