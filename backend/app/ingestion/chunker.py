def chunk_documents(documents: list[dict], chunk_size: int = 500, overlap: int = 50):
	"""Split extracted page documents into overlapping character chunks."""
	if chunk_size <= 0:
		raise ValueError("chunk_size must be greater than zero")

	if overlap < 0 or overlap >= chunk_size:
		raise ValueError("overlap must be non-negative and smaller than chunk_size")

	step = chunk_size - overlap
	chunks = []

	for document in documents:
		text = document.get("text", "").strip()
		metadata = document.get("metadata", {})

		for start in range(0, len(text), step):
			chunk_text = text[start:start + chunk_size]

			if not chunk_text:
				continue

			chunks.append({
				"text": chunk_text,
				"metadata": {
					"source": metadata.get("source"),
					"page": metadata.get("page"),
				},
			})

			if start + chunk_size >= len(text):
				break

	return chunks
