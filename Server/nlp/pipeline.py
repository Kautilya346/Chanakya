"""
Chanakya NLP Pipeline
=====================

Main orchestration layer for the NLP pipeline.

Pipeline stages:
1. Input validation
2. Preprocessing (optional)
3. Classification (Gemini 2 Flash)
4. Post-processing and validation
5. Output generation

Governance features:
- All outputs validated against fixed taxonomies
- Confidence thresholds enforced
- Audit logging
- Fallback handling
"""

import time
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field

from .schemas import (
    TeacherUtterance,
    ClassroomContext,
    NLPOutput,
    OrchestratorInput,
    ClassroomState,
    TeacherIntent,
    Urgency,
    Topic,
    DetectedLanguage
)
from .gemini_processor import GeminiProcessor
from .indic_classifier import IndicClassifier


# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

logger = logging.getLogger("chanakya.nlp")


# =============================================================================
# AUDIT LOG SCHEMA
# =============================================================================

@dataclass
class NLPAuditLog:
    """
    Audit log for every NLP processing event.
    
    Required for:
    - Government accountability
    - NGO transparency
    - System debugging
    - Model improvement
    """
    
    # Identifiers (required fields first)
    request_id: str
    session_id: Optional[str]
    raw_input: str
    
    # Timestamp with default
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    # Input
    input_language: Optional[str] = None
    
    # Processing
    processing_time_ms: float = 0.0
    model_used: str = ""
    fallback_triggered: bool = False
    fallback_reason: Optional[str] = None
    
    # Output
    detected_language: str = ""
    classroom_state: str = ""
    teacher_intent: str = ""
    urgency: str = ""
    topic: str = ""
    
    # Confidence
    overall_confidence: float = 0.0
    state_confidence: float = 0.0
    intent_confidence: float = 0.0
    
    # Flags
    requires_clarification: bool = False
    low_resource_language: bool = False
    validation_errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "request_id": self.request_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "raw_input": self.raw_input,
            "input_language": self.input_language,
            "processing_time_ms": self.processing_time_ms,
            "model_used": self.model_used,
            "fallback_triggered": self.fallback_triggered,
            "fallback_reason": self.fallback_reason,
            "detected_language": self.detected_language,
            "classroom_state": self.classroom_state,
            "teacher_intent": self.teacher_intent,
            "urgency": self.urgency,
            "topic": self.topic,
            "overall_confidence": self.overall_confidence,
            "state_confidence": self.state_confidence,
            "intent_confidence": self.intent_confidence,
            "requires_clarification": self.requires_clarification,
            "low_resource_language": self.low_resource_language,
            "validation_errors": self.validation_errors
        }


# =============================================================================
# PIPELINE CONFIGURATION
# =============================================================================

@dataclass
class PipelineConfig:
    """Configuration for NLP pipeline."""
    
    # Confidence thresholds
    min_confidence_threshold: float = 0.3
    clarification_threshold: float = 0.5
    
    # Timeout settings (milliseconds)
    max_processing_time_ms: float = 5000.0
    
    # Validation settings
    strict_validation: bool = True
    allow_unknown_values: bool = True
    
    # Audit settings
    enable_audit_logging: bool = True
    log_raw_input: bool = True
    
    # Fallback settings
    enable_indicbert_fallback: bool = False
    indicbert_confidence_threshold: float = 0.7


# =============================================================================
# NLP PIPELINE
# =============================================================================

class NLPPipeline:
    """
    Main NLP pipeline for Chanakya.
    
    Orchestrates:
    1. Input validation and preprocessing
    2. Gemini-based classification
    3. Output validation and post-processing
    4. Audit logging
    
    Usage:
        pipeline = NLPPipeline(gemini_api_key="your-key")
        result = await pipeline.process(utterance, context)
    """
    
    def __init__(
        self,
        gemini_api_key: str,
        config: Optional[PipelineConfig] = None,
        audit_callback: Optional[callable] = None
    ):
        """
        Initialize NLP pipeline.
        
        Args:
            gemini_api_key: API key for Gemini
            config: Pipeline configuration
            audit_callback: Optional callback for audit logs
        """
        self.config = config or PipelineConfig()
        self.gemini = GeminiProcessor(api_key=gemini_api_key)
        self.indic = IndicClassifier()
        self.audit_callback = audit_callback
        
        self._request_counter = 0
    
    async def process(
        self,
        utterance: TeacherUtterance,
        context: Optional[ClassroomContext] = None
    ) -> NLPOutput:
        """
        Process teacher utterance through full pipeline.
        
        Args:
            utterance: Teacher input
            context: Optional classroom context
            
        Returns:
            Validated NLPOutput
        """
        request_id = self._generate_request_id()
        start_time = time.time()
        
        # Initialize audit log
        audit = NLPAuditLog(
            request_id=request_id,
            session_id=utterance.session_id,
            raw_input=utterance.text if self.config.log_raw_input else "[redacted]"
        )
        
        try:
            # Stage 1: Input validation
            validated_input = self._validate_input(utterance)
            
            # Stage 2: Preprocessing
            preprocessed = self._preprocess(validated_input)
            
            # Stage 3: Classification via Gemini
            output = await self.gemini.process(preprocessed, context)
            
            # Stage 4: Post-processing and validation
            validated_output = self._validate_output(output)
            
            # Update audit log
            audit.processing_time_ms = (time.time() - start_time) * 1000
            audit.model_used = output.model_version
            audit.detected_language = output.detected_language.value
            audit.classroom_state = output.classroom_state.value
            audit.teacher_intent = output.teacher_intent.value
            audit.urgency = output.urgency.value
            audit.topic = output.topic.value
            audit.overall_confidence = output.confidence
            audit.state_confidence = output.state_confidence
            audit.intent_confidence = output.intent_confidence
            audit.requires_clarification = output.requires_clarification
            audit.low_resource_language = output.low_resource_language
            
            # Log
            self._log_audit(audit)
            
            return validated_output
            
        except Exception as e:
            # Handle errors gracefully
            logger.error(f"Pipeline error: {e}", exc_info=True)
            
            audit.processing_time_ms = (time.time() - start_time) * 1000
            audit.fallback_triggered = True
            audit.fallback_reason = str(e)
            audit.validation_errors.append(str(e))
            
            self._log_audit(audit)
            
            return self._get_fallback_output(utterance, str(e), request_id)
    
    def process_sync(
        self,
        utterance: TeacherUtterance,
        context: Optional[ClassroomContext] = None
    ) -> NLPOutput:
        """Synchronous version of process()."""
        import asyncio
        return asyncio.run(self.process(utterance, context))
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        self._request_counter += 1
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"nlp-{timestamp}-{self._request_counter:06d}"
    
    def _validate_input(self, utterance: TeacherUtterance) -> TeacherUtterance:
        """
        Validate input utterance.
        
        Checks:
        - Non-empty text
        - Reasonable length
        - No obviously invalid content
        """
        text = utterance.text.strip()
        
        if not text:
            raise ValueError("Empty utterance")
        
        if len(text) > 500:
            # Truncate very long inputs
            text = text[:500]
            logger.warning(f"Truncated long input to 500 chars")
        
        if len(text) < 2:
            raise ValueError("Utterance too short")
        
        return TeacherUtterance(
            text=text,
            timestamp=utterance.timestamp,
            audio_confidence=utterance.audio_confidence,
            session_id=utterance.session_id
        )
    
    def _preprocess(self, utterance: TeacherUtterance) -> TeacherUtterance:
        """
        Preprocess utterance.
        
        Currently minimal - Gemini handles most normalization.
        Future: Could add script normalization, profanity filtering, etc.
        """
        text = utterance.text
        
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove common ASR artifacts
        text = text.replace("[inaudible]", "")
        text = text.replace("[noise]", "")
        text = text.replace("[silence]", "")
        
        return TeacherUtterance(
            text=text,
            timestamp=utterance.timestamp,
            audio_confidence=utterance.audio_confidence,
            session_id=utterance.session_id
        )
    
    def _validate_output(self, output: NLPOutput) -> NLPOutput:
        """
        Validate NLP output.
        
        Ensures:
        - All enum values are valid
        - Confidence scores are reasonable
        - Required fields present
        """
        errors = []
        
        # Validate enum values
        if output.classroom_state not in ClassroomState:
            errors.append(f"Invalid classroom_state: {output.classroom_state}")
        
        if output.teacher_intent not in TeacherIntent:
            errors.append(f"Invalid teacher_intent: {output.teacher_intent}")
        
        if output.urgency not in Urgency:
            errors.append(f"Invalid urgency: {output.urgency}")
        
        if output.topic not in Topic:
            errors.append(f"Invalid topic: {output.topic}")
        
        # Check confidence bounds
        if not 0 <= output.confidence <= 1:
            errors.append(f"Invalid confidence: {output.confidence}")
        
        # Check for clarification requirement
        if output.confidence < self.config.clarification_threshold:
            output.requires_clarification = True
        
        if errors and self.config.strict_validation:
            raise ValueError(f"Validation errors: {errors}")
        
        return output
    
    def _get_fallback_output(
        self,
        utterance: TeacherUtterance,
        error: str,
        request_id: str
    ) -> NLPOutput:
        """Generate fallback output on error."""
        
        return NLPOutput(
            classroom_state=ClassroomState.UNKNOWN,
            teacher_intent=TeacherIntent.UNKNOWN,
            urgency=Urgency.MEDIUM,
            topic=Topic.UNKNOWN,
            detected_language=DetectedLanguage.UNKNOWN,
            secondary_language=None,
            normalized_text=utterance.text,
            english_translation=f"[Error: {error}]",
            student_count_mentioned=None,
            specific_concept=None,
            confidence=0.1,
            state_confidence=0.1,
            intent_confidence=0.1,
            raw_input=utterance.text,
            processing_time_ms=0.0,
            model_version="fallback",
            requires_clarification=True,
            low_resource_language=False,
            fallback_used=True
        )
    
    def _log_audit(self, audit: NLPAuditLog):
        """Log audit record."""
        
        if self.config.enable_audit_logging:
            logger.info(f"NLP Audit: {audit.to_dict()}")
        
        if self.audit_callback:
            try:
                self.audit_callback(audit)
            except Exception as e:
                logger.error(f"Audit callback error: {e}")
    
    def build_orchestrator_input(
        self,
        nlp_output: NLPOutput,
        context: Optional[ClassroomContext] = None
    ) -> OrchestratorInput:
        """
        Build input for the orchestrator.
        
        This is the bridge between NLP and the orchestrator layer.
        """
        return self.gemini.build_orchestrator_input(nlp_output, context)


# =============================================================================
# PIPELINE FACTORY
# =============================================================================

def create_pipeline(
    gemini_api_key: str,
    config: Optional[PipelineConfig] = None,
    audit_callback: Optional[callable] = None
) -> NLPPipeline:
    """
    Factory function to create NLP pipeline.
    
    Args:
        gemini_api_key: API key for Gemini
        config: Optional pipeline configuration
        audit_callback: Optional callback for audit logs
        
    Returns:
        Configured NLPPipeline instance
    """
    return NLPPipeline(
        gemini_api_key=gemini_api_key,
        config=config,
        audit_callback=audit_callback
    )
