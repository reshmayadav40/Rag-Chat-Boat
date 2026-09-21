import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.llm.generator import LLMConfigurationError, generate_answer
from app.retrieval.retrieval import retrieve_documents


logger = logging.getLogger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
	question: str


class Source(BaseModel):
	source: str
	page: int


class ChatResponse(BaseModel):
	answer: str
	sources: list[Source]


@router.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
	question = request.question.strip()
	if not question:
		raise HTTPException(status_code=400, detail="Question cannot be empty")

	try:
		retrieved_documents = retrieve_documents(question)
	except Exception as error:
		logger.exception("Document retrieval failed: %s", error)
		raise HTTPException(
			status_code=500,
			detail="Unable to retrieve documents right now.",
		) from error

	try:
		answer = generate_answer(question, retrieved_documents)
	except (LLMConfigurationError, RuntimeError) as error:
		logger.exception("Answer generation failed: %s", error)
		raise HTTPException(
			status_code=502,
			detail="Unable to generate an answer right now.",
		) from error
	except Exception as error:
		logger.exception("Unexpected answer generation failure: %s", error)
		raise HTTPException(
			status_code=500,
			detail="An unexpected error occurred.",
		) from error

	sources = []
	seen_sources = set()
	for document in retrieved_documents:
		source_key = (document.get("source"), document.get("page"))
		if source_key in seen_sources:
			continue
		seen_sources.add(source_key)
		sources.append(
			Source(
				source=document["source"],
				page=document["page"],
			)
		)

	return ChatResponse(answer=answer, sources=sources)
