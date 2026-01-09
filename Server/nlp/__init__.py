"""
Chanakya NLP Layer
==================

Real-time classroom decision-support NLP pipeline for Indian primary school teachers.

This layer processes spoken teacher utterances in any Indian language and produces
deterministic, structured JSON output for the orchestrator.

Architecture:
    Teacher Speech → ASR → NLP Pipeline → Structured JSON → Orchestrator

The NLP pipeline uses:
    - Gemini 2 Flash: Primary model for multilingual understanding, intent extraction,
                      classification, and structured output generation
    - IndicBERT: Optional fine-tuned classifier for high-frequency, latency-critical
                 classification tasks (classroom_state, urgency)

Design Principle: Gemini-First with IndicBERT Fallback
    - Gemini 2 Flash handles ALL multilingual understanding (22+ Indian languages)
    - IndicBERT used ONLY when:
        1. Sub-100ms latency required for specific classification
        2. Offline/edge deployment needed (future)
        3. Deterministic classification audit trail required
"""

from .pipeline import NLPPipeline
from .schemas import (
    TeacherUtterance,
    ClassroomContext,
    NLPOutput,
    ClassroomState,
    TeacherIntent,
    Urgency,
    Topic
)
from .gemini_processor import GeminiProcessor
from .indic_classifier import IndicClassifier

__version__ = "0.1.0"
__all__ = [
    "NLPPipeline",
    "TeacherUtterance",
    "ClassroomContext", 
    "NLPOutput",
    "ClassroomState",
    "TeacherIntent",
    "Urgency",
    "Topic",
    "GeminiProcessor",
    "IndicClassifier"
]
