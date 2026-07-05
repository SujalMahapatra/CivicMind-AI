"""
CivicMind AI - RAG Agent

RAG = Retrieval Augmented Generation

PURPOSE:
---------
Instead of relying only on Gemini's training knowledge,
the RAG Agent retrieves relevant information from a local
knowledge base and supplies that context to Gemini.

WORKFLOW:
----------
User Question
      ↓
Embedding Generation
      ↓
Vector Search (ChromaDB)
      ↓
Retrieve Relevant Context
      ↓
Gemini
      ↓
Answer + Source

WHY RAG?
---------
Without RAG:
    Gemini answers from its training data.

With RAG:
    Gemini answers from our knowledge base.

This improves:
- Accuracy
- Explainability
- Domain-specific knowledge
- Source attribution
"""

from pathlib import Path
from typing import List

import chromadb
from sentence_transformers import SentenceTransformer

from services.gemini_service import (
    gemini_service,
    GeminiService
)

from .schemas import (
    RAGRequest,
    RAGResponse
)


class RAGAgent:
    """
    Retrieval-Augmented Generation Agent.

    Responsible for:

    1. Loading knowledge documents
    2. Creating embeddings
    3. Storing vectors in ChromaDB
    4. Retrieving relevant context
    5. Generating answers using Gemini
    """

    COLLECTION_NAME = "civicmind_knowledge"

    def __init__(self) -> None:
        """
        Initialize embedding model and vector database.
        """

        # ==========================================================
        # PATHS
        # ==========================================================

        backend_dir = Path(__file__).resolve().parents[2]

        self.knowledge_base_path = (
            backend_dir / "knowledge_base"
        )

        self.vector_db_path = (
            backend_dir / "vector_db"
        )

        # ==========================================================
        # EMBEDDING MODEL
        # ==========================================================

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # ==========================================================
        # CHROMADB
        # ==========================================================

        self.client = chromadb.PersistentClient(
            path=str(self.vector_db_path)
        )

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

        # ==========================================================
        # INDEX DOCUMENTS
        # ==========================================================

        self._initialize_knowledge_base()

    # ==============================================================
    # KNOWLEDGE BASE SETUP
    # ==============================================================

    def _initialize_knowledge_base(self) -> None:
        """
        Index knowledge base documents.

        To avoid duplicate insertion, documents are added
        only when the collection is empty.
        """

        existing_count = self.collection.count()

        if existing_count > 0:
            return

        txt_files = list(
            self.knowledge_base_path.glob("*.txt")
        )

        document_id = 0

        for file_path in txt_files:

            content = file_path.read_text(
                encoding="utf-8"
            )

            chunks = self._chunk_text(content)

            for chunk in chunks:

                embedding = (
                    self.embedding_model.encode(chunk)
                    .tolist()
                )

                self.collection.add(
                    ids=[f"doc_{document_id}"],
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[
                        {
                            "source": file_path.name
                        }
                    ]
                )

                document_id += 1

    # ==============================================================
    # CHUNKING
    # ==============================================================

    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 500
    ) -> List[str]:
        """
        Split large text into smaller chunks.

        Simple fixed-size chunking for hackathon version.
        """

        chunks = []

        for i in range(
            0,
            len(text),
            chunk_size
        ):
            chunks.append(
                text[i:i + chunk_size]
            )

        return chunks

    # ==============================================================
    # RETRIEVAL
    # ==============================================================

    def retrieve_context(
        self,
        question: str,
        top_k: int = 3
    ) -> tuple[str, str]:
        """
        Retrieve most relevant chunks.

        Returns:
            context_text
            source_files
        """

        query_embedding = (
            self.embedding_model.encode(question)
            .tolist()
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context = "\n\n".join(documents)

        sources = list(
            {
                item["source"]
                for item in metadatas
            }
        )

        return context, ", ".join(sources)

    # ==============================================================
    # PROMPT BUILDING
    # ==============================================================

    def _build_prompt(
        self,
        context: str,
        question: str
    ) -> str:
        """
        Create RAG prompt.
        """

        return f"""
You are an expert community intelligence assistant.

Use ONLY the provided context.

If the answer cannot be found in the context,
say:

"The requested information is not available in the knowledge base."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    # ==============================================================
    # QUESTION ANSWERING
    # ==============================================================

    def answer_question(
        self,
        request: RAGRequest
    ) -> RAGResponse:
        """
        Main RAG workflow.

        Question
            ↓
        Retrieval
            ↓
        Prompt Construction
            ↓
        Gemini
            ↓
        Response
        """

        if not request.question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        context, sources = self.retrieve_context(
            request.question
        )

        prompt = self._build_prompt(
            context=context,
            question=request.question
        )

        answer = gemini_service.generate_text(
            prompt=prompt
        )

        return RAGResponse(
            question=request.question,
            answer=answer,
            source=sources
        )


# ==============================================================
# SHARED INSTANCE
# ==============================================================

rag_agent = RAGAgent()