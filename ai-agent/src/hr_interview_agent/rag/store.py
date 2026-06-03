"""PDF Q&A ingestion and Chroma vector retrieval."""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from hr_interview_agent.config import settings

COLLECTION = "hr_qa_guides"


def _embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(api_key=settings.openai_api_key)


def get_vector_store() -> Chroma:
    Path(settings.chroma_persist_dir).mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=COLLECTION,
        embedding_function=_embeddings(),
        persist_directory=settings.chroma_persist_dir,
    )


def ingest_pdf(file_path: str, document_id: str) -> int:
    """Load PDF, chunk, and upsert into Chroma. Returns chunk count."""
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    for doc in pages:
        doc.metadata["document_id"] = document_id

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(pages)
    if not chunks:
        return 0

    store = get_vector_store()
    store.add_documents(chunks, ids=[f"{document_id}_{i}" for i in range(len(chunks))])
    return len(chunks)


def retrieve_context(query: str, k: int = 5) -> str:
    store = get_vector_store()
    docs = store.similarity_search(query, k=k)
    if not docs:
        return "No reference Q&A material loaded. Score using general HR interview criteria."
    parts = []
    for i, doc in enumerate(docs, 1):
        src = doc.metadata.get("source", "guide")
        parts.append(f"[{i}] ({src})\n{doc.page_content}")
    return "\n\n".join(parts)
