from pydantic import BaseModel, Field
from pydantic import ConfigDict

model_config: ConfigDict = ConfigDict(
    json_schema_extra={
        "example": {
            "immediate_actions": "Issue air quality alerts. Recommend N95 masks. Postpone outdoor events.",
            "preventive_actions": "Increase public transit subsidies. Establish car-free zones. Plant green buffers.",
            "long_term_actions": "Transition to electric buses. Build urban forests. Implement congestion pricing.",
            "model_used": "gemini-2.5-flash"
        }
    }
)
 
 
class RAGRequest(BaseModel):
    """
    Request model for RAG-based question answering.
    
    The RAG (Retrieval-Augmented Generation) request model captures
    a user's question that should be answered using the knowledge base.
    
    Attributes:
        question: The user's question about community intelligence topics
        
    Usage:
        >>> request = RAGRequest(question="What are air quality guidelines?")
    """
    
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Question to answer using the knowledge base"
    )
    
    model_config: ConfigDict = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "What are WHO air quality guidelines?"
            }
        }
    )
 
 
class RAGResponse(BaseModel):
    """
    Response model for RAG-based question answering.
    
    Contains the answer generated from retrieved knowledge base context
    along with source attribution for transparency.
    
    Attributes:
        question: Original user question
        answer: Generated answer from retrieved context
        source: Source file(s) from knowledge base
    """
    
    question: str = Field(
        ...,
        description="Original user question"
    )
    
    answer: str = Field(
        ...,
        description="Answer generated from retrieved knowledge base context"
    )
    
    source: str = Field(
        ...,
        description="Source file(s) from knowledge base used to generate answer"
    )
    
    model_config: ConfigDict = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "What are WHO air quality guidelines?",
                "answer": "WHO guidelines recommend PM2.5 annual mean not exceeding 5 μg/m³.",
                "source": "who_air_quality.txt"
            }
        }
    )
 
