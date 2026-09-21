from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
	global _model

	if _model is None:
		_model = SentenceTransformer(MODEL_NAME)

	return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
	"""Generate one embedding vector for each input text."""
	if not texts:
		return []

	embeddings = _get_model().encode(texts, convert_to_numpy=True)
	return embeddings.tolist()


def embed_text(text: str) -> list[float]:
	"""Generate an embedding vector for one input text."""
	return embed_texts([text])[0]
