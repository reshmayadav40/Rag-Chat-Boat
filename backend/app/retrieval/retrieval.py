from pathlib import Path

import chromadb

from app.ingestion.embedder import embed_text


BACKEND_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BACKEND_DIR / "chroma_db"
COLLECTION_NAME = "rag_documents"


def _get_collection() -> chromadb.Collection:
	client = chromadb.PersistentClient(path=str(CHROMA_DIR))
	return client.get_collection(name=COLLECTION_NAME)


def retrieve_documents(query: str, top_k: int = 3) -> list[dict]:
	"""Return the most similar stored chunks for a user question."""
	if not query or not query.strip():
		raise ValueError("Query cannot be empty")

	if top_k <= 0:
		raise ValueError("top_k must be greater than zero")

	collection = _get_collection()
	result = collection.query(
		query_embeddings=[embed_text(query)],
		n_results=min(top_k, collection.count()),
		include=["documents", "metadatas", "distances"],
	)

	documents = result.get("documents", [[]])[0]
	metadatas = result.get("metadatas", [[]])[0]
	distances = result.get("distances", [[]])[0]

	return [
		{
			"text": text,
			"source": metadata.get("source"),
			"page": metadata.get("page"),
			"distance": distance,
		}
		for text, metadata, distance in zip(documents, metadatas, distances)
	]
