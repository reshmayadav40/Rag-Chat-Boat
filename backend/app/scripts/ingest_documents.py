from pathlib import Path

import chromadb

from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import embed_texts
from app.ingestion.pdf_loader import load_pdf


BACKEND_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BACKEND_DIR / "data"
CHROMA_DIR = BACKEND_DIR / "chroma_db"
COLLECTION_NAME = "rag_documents"
PDF_NAMES = ("react.pdf", "nodejs.pdf", "mongodb.pdf")


def get_collection() -> chromadb.Collection:
	"""Create a persistent Chroma collection, replacing only an empty placeholder file."""
	if CHROMA_DIR.exists() and not CHROMA_DIR.is_dir():
		if CHROMA_DIR.stat().st_size != 0:
			raise RuntimeError(
				f"Cannot use {CHROMA_DIR}: it is a non-empty file, not a directory."
			)
		CHROMA_DIR.unlink()

	CHROMA_DIR.mkdir(parents=True, exist_ok=True)
	client = chromadb.PersistentClient(path=str(CHROMA_DIR))
	return client.get_or_create_collection(name=COLLECTION_NAME)


def ingest_pdf(collection: chromadb.Collection, pdf_path: Path) -> tuple[int, int]:
	print(f"Loading: {pdf_path.name}")
	pages = load_pdf(str(pdf_path))
	chunks = chunk_documents(pages, chunk_size=500, overlap=50)

	ids = [
		f"{chunk['metadata']['source']}-page-{chunk['metadata']['page']}-chunk-{index}"
		for index, chunk in enumerate(chunks)
	]
	existing_ids = set(collection.get(ids=ids, include=[]).get("ids", []))
	new_chunks = [
		(chunk_id, chunk)
		for chunk_id, chunk in zip(ids, chunks)
		if chunk_id not in existing_ids
	]

	new_embeddings = embed_texts([chunk["text"] for _, chunk in new_chunks])
	if new_chunks:
		collection.add(
			ids=[chunk_id for chunk_id, _ in new_chunks],
			documents=[chunk["text"] for _, chunk in new_chunks],
			embeddings=new_embeddings,
			metadatas=[chunk["metadata"] for _, chunk in new_chunks],
		)

	print(f"Pages: {len(pages)}")
	print(f"Chunks: {len(chunks)}")
	print(f"Embeddings: {len(new_embeddings)}")
	print(f"Stored: {len(new_chunks)}")
	return len(chunks), len(new_chunks)


def main() -> None:
	collection = get_collection()
	total_chunks = 0

	for pdf_name in PDF_NAMES:
		chunks, _ = ingest_pdf(collection, DATA_DIR / pdf_name)
		total_chunks += chunks

	print("ChromaDB ingestion completed.")
	print(f"Collection: {COLLECTION_NAME}")
	print(f"Total documents/chunks: {collection.count()}")


if __name__ == "__main__":
	main()
