"""
CivicMind AI - RAG Router

This module exposes HTTP endpoints for the RAG Agent.

RAG = Retrieval Augmented Generation

## PURPOSE:

Allows users to ask questions against the CivicMind
knowledge base.

## WORKFLOW:

Question
↓
RAG Agent
↓
Vector Search (ChromaDB)
↓
Retrieved Context
↓
Gemini
↓
Answer + Sources

## ENDPOINT:

POST /rag/ask
"""

from fastapi import APIRouter, HTTPException, status

from agents.rag.rag_agent import rag_agent

from agents.rag.schemas import (
RAGRequest,
RAGResponse
)

# ==========================================================

# ROUTER INITIALIZATION

# ==========================================================

router = APIRouter(
prefix="/rag",
tags=["RAG"]
)

# ==========================================================

# QUESTION ANSWERING ENDPOINT

# ==========================================================

@router.post(
"/ask",
response_model=RAGResponse,
status_code=status.HTTP_200_OK,
summary="Ask a question using RAG",
description=(
"Retrieve relevant information from the knowledge "
"base and generate an answer using Gemini."
)
)
async def ask_question(
    request: RAGRequest
    ) -> RAGResponse:
    """
    Answer a question using Retrieval-Augmented Generation.

    ```
    Example Request:

    {
        "question": "What AQI level is considered unhealthy?"
    }

    Example Response:

    {
        "question": "What AQI level is considered unhealthy?",
        "answer": "...",
        "source": "who_air_quality.txt"
    }
    """

    try:
        return rag_agent.answer_question(
            request=request
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

