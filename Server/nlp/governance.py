"""
Governance and Safety Controls
==============================

Safety layer to prevent:
1. Hallucination of pedagogy by LLM
2. Multi-action or abstract advice
3. Resource assumptions
4. Ungovernable outputs

This module enforces Chanakya's core constraints at the NLP layer.
"""

from typing import Optional, List, Dict, Any, Set
from dataclasses import dataclass
from enum import Enum
import re

from .schemas import (
    NLPOutput,
    ClassroomState,
    TeacherIntent,
    Urgency,
    Topic,
    OrchestratorInput
)


# =============================================================================
# GOVERNANCE RULES
# =============================================================================

class GovernanceRule(str, Enum):
    """Governance rules enforced by Chanakya."""
    
    # Output constraints
    SINGLE_ACTION_ONLY = "single_action_only"
    NO_ABSTRACT_ADVICE = "no_abstract_advice"
    NO_NEW_RESOURCES = "no_new_resources"
    NO_PEDAGOGY_GENERATION = "no_pedagogy_generation"
    
    # Safety constraints
    NO_HARMFUL_CONTENT = "no_harmful_content"
    NO_STUDENT_IDENTIFICATION = "no_student_identification"
    NO_PERSONAL_DATA = "no_personal_data"
    
    # Compliance constraints
    TAXONOMY_ONLY = "taxonomy_only"
    CONFIDENCE_MINIMUM = "confidence_minimum"
    AUDIT_REQUIRED = "audit_required"


# =============================================================================
# VIOLATION TYPES
# =============================================================================

@dataclass
class GovernanceViolation:
    """Record of a governance violation."""
    
    rule: GovernanceRule
    severity: str  # "warning", "error", "critical"
    message: str
    field: Optional[str] = None
    value: Optional[str] = None


# =============================================================================
# GOVERNANCE VALIDATOR
# =============================================================================

class GovernanceValidator:
    """
    Validates NLP outputs against governance rules.
    
    Ensures:
    - All outputs use fixed taxonomies
    - No pedagogy is generated (only retrieved)
    - Confidence thresholds are met
    - Audit requirements satisfied
    """
    
    def __init__(
        self,
        min_confidence: float = 0.3,
        strict_mode: bool = True
    ):
        self.min_confidence = min_confidence
        self.strict_mode = strict_mode
        
        # Blocked patterns in text fields
        self._blocked_patterns = [
            # Personal information
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{10}\b',  # Phone numbers
            r'\b\d{12}\b',  # Aadhaar-like numbers
            
            # Student names (common Indian name patterns)
            # Note: This is a heuristic, not perfect
            r'\b(student named|bachche ka naam|uska naam)\s+\w+',
        ]
        
        # Abstract advice indicators (in outputs that slip through)
        self._abstract_indicators = [
            "you should consider",
            "it would be good to",
            "try to think about",
            "in general",
            "usually",
            "depending on",
            "it depends",
            "aap sochiye",
            "generally speaking"
        ]
    
    def validate(self, output: NLPOutput) -> List[GovernanceViolation]:
        """
        Validate NLP output against all governance rules.
        
        Args:
            output: NLP output to validate
            
        Returns:
            List of violations (empty if valid)
        """
        violations = []
        
        # Rule: Taxonomy only
        violations.extend(self._check_taxonomy_compliance(output))
        
        # Rule: Confidence minimum
        violations.extend(self._check_confidence(output))
        
        # Rule: No personal data
        violations.extend(self._check_personal_data(output))
        
        # Rule: No abstract advice (check normalized text)
        violations.extend(self._check_abstract_content(output))
        
        return violations
    
    def _check_taxonomy_compliance(
        self,
        output: NLPOutput
    ) -> List[GovernanceViolation]:
        """Check that all classifications use valid enum values."""
        
        violations = []
        
        # Check each enum field
        try:
            ClassroomState(output.classroom_state)
        except ValueError:
            violations.append(GovernanceViolation(
                rule=GovernanceRule.TAXONOMY_ONLY,
                severity="error",
                message=f"Invalid classroom_state: {output.classroom_state}",
                field="classroom_state",
                value=str(output.classroom_state)
            ))
        
        try:
            TeacherIntent(output.teacher_intent)
        except ValueError:
            violations.append(GovernanceViolation(
                rule=GovernanceRule.TAXONOMY_ONLY,
                severity="error",
                message=f"Invalid teacher_intent: {output.teacher_intent}",
                field="teacher_intent",
                value=str(output.teacher_intent)
            ))
        
        try:
            Urgency(output.urgency)
        except ValueError:
            violations.append(GovernanceViolation(
                rule=GovernanceRule.TAXONOMY_ONLY,
                severity="error",
                message=f"Invalid urgency: {output.urgency}",
                field="urgency",
                value=str(output.urgency)
            ))
        
        try:
            Topic(output.topic)
        except ValueError:
            violations.append(GovernanceViolation(
                rule=GovernanceRule.TAXONOMY_ONLY,
                severity="error",
                message=f"Invalid topic: {output.topic}",
                field="topic",
                value=str(output.topic)
            ))
        
        return violations
    
    def _check_confidence(
        self,
        output: NLPOutput
    ) -> List[GovernanceViolation]:
        """Check confidence thresholds."""
        
        violations = []
        
        if output.confidence < self.min_confidence:
            violations.append(GovernanceViolation(
                rule=GovernanceRule.CONFIDENCE_MINIMUM,
                severity="warning",
                message=f"Confidence {output.confidence} below threshold {self.min_confidence}",
                field="confidence",
                value=str(output.confidence)
            ))
        
        return violations
    
    def _check_personal_data(
        self,
        output: NLPOutput
    ) -> List[GovernanceViolation]:
        """Check for personal data in text fields."""
        
        violations = []
        
        text_fields = [
            ("normalized_text", output.normalized_text),
            ("english_translation", output.english_translation),
            ("specific_concept", output.specific_concept or "")
        ]
        
        for field_name, field_value in text_fields:
            for pattern in self._blocked_patterns:
                if re.search(pattern, field_value, re.IGNORECASE):
                    violations.append(GovernanceViolation(
                        rule=GovernanceRule.NO_PERSONAL_DATA,
                        severity="critical",
                        message=f"Potential personal data in {field_name}",
                        field=field_name,
                        value="[redacted]"
                    ))
                    break
        
        return violations
    
    def _check_abstract_content(
        self,
        output: NLPOutput
    ) -> List[GovernanceViolation]:
        """Check for abstract advice indicators that might slip through."""
        
        violations = []
        
        text = (output.normalized_text + " " + output.english_translation).lower()
        
        for indicator in self._abstract_indicators:
            if indicator.lower() in text:
                violations.append(GovernanceViolation(
                    rule=GovernanceRule.NO_ABSTRACT_ADVICE,
                    severity="warning",
                    message=f"Abstract content indicator found: '{indicator}'",
                    field="text_content",
                    value=indicator
                ))
        
        return violations
    
    def is_valid(self, output: NLPOutput) -> bool:
        """Quick check if output is valid."""
        violations = self.validate(output)
        
        if self.strict_mode:
            return len(violations) == 0
        else:
            # Allow warnings in non-strict mode
            return not any(v.severity in ["error", "critical"] for v in violations)


# =============================================================================
# OUTPUT CONSTRAINT ENFORCER
# =============================================================================

class OutputConstraintEnforcer:
    """
    Enforces constraints on what the system can output.
    
    Used by the orchestrator to ensure final responses:
    1. Are single, atomic actions
    2. Use only available resources
    3. Come from RAG, not LLM generation
    """
    
    # Resources that are ALWAYS available in Indian government schools
    ALWAYS_AVAILABLE_RESOURCES = {
        "voice",           # Teacher can speak
        "body",            # Teacher body language, gestures
        "students",        # Students themselves
        "chalkboard",      # Most schools have this
        "chalk",           # Usually available
        "floor",           # Always available
        "hands",           # Clapping, showing
        "eyes",            # Eye contact
    }
    
    # Resources that MAY be available
    OPTIONAL_RESOURCES = {
        "textbook",
        "notebook",
        "pencil",
        "slate",
        "stones",          # For counting
        "sticks",          # For counting
        "leaves",          # Nature materials
        "water",
        "rope",
    }
    
    # Resources that should NEVER be assumed
    NEVER_ASSUME_RESOURCES = {
        "projector",
        "computer",
        "tablet",
        "smartphone",
        "printer",
        "worksheet",       # Printed materials
        "flashcards",      # Pre-made materials
        "manipulatives",   # Commercial math tools
        "internet",
    }
    
    def __init__(self):
        self._action_count_pattern = re.compile(
            r'(first|second|third|then|next|after that|finally|1\.|2\.|3\.)',
            re.IGNORECASE
        )
    
    def check_single_action(self, response_text: str) -> bool:
        """
        Check if response contains only ONE action.
        
        Returns True if single action, False if multiple actions detected.
        """
        # Check for multi-step indicators
        matches = self._action_count_pattern.findall(response_text)
        return len(matches) <= 1
    
    def check_resource_constraint(
        self,
        response_text: str,
        available_resources: Optional[Set[str]] = None
    ) -> List[str]:
        """
        Check if response assumes unavailable resources.
        
        Returns list of problematic resource assumptions.
        """
        if available_resources is None:
            available_resources = self.ALWAYS_AVAILABLE_RESOURCES
        
        problems = []
        text_lower = response_text.lower()
        
        for resource in self.NEVER_ASSUME_RESOURCES:
            if resource in text_lower:
                problems.append(resource)
        
        return problems
    
    def validate_rag_response(
        self,
        response: Dict[str, Any],
        nlp_output: NLPOutput
    ) -> Dict[str, Any]:
        """
        Validate that a RAG-retrieved response is appropriate.
        
        Args:
            response: Response from RAG system
            nlp_output: NLP classification output
            
        Returns:
            Validated response or error dict
        """
        result = {
            "valid": True,
            "response": response,
            "violations": []
        }
        
        # Check source is RAG, not LLM
        if response.get("source") == "llm_generated":
            result["valid"] = False
            result["violations"].append("Response was LLM-generated, not RAG-retrieved")
        
        # Check single action
        if "text" in response:
            if not self.check_single_action(response["text"]):
                result["valid"] = False
                result["violations"].append("Response contains multiple actions")
            
            # Check resources
            resource_problems = self.check_resource_constraint(response["text"])
            if resource_problems:
                result["valid"] = False
                result["violations"].append(
                    f"Response assumes unavailable resources: {resource_problems}"
                )
        
        return result


# =============================================================================
# EXPLAINABILITY MODULE
# =============================================================================

class ExplainabilityGenerator:
    """
    Generates explanations for CRPs, administrators, and auditors.
    
    Provides:
    - Why a classification was made
    - What signals were used
    - Confidence breakdown
    - Audit trail
    """
    
    def generate_explanation(
        self,
        nlp_output: NLPOutput,
        for_audience: str = "crp"  # "crp", "admin", "technical"
    ) -> Dict[str, Any]:
        """
        Generate human-readable explanation.
        
        Args:
            nlp_output: The NLP output to explain
            for_audience: Target audience for explanation
            
        Returns:
            Explanation dict
        """
        
        if for_audience == "crp":
            return self._explain_for_crp(nlp_output)
        elif for_audience == "admin":
            return self._explain_for_admin(nlp_output)
        else:
            return self._explain_technical(nlp_output)
    
    def _explain_for_crp(self, output: NLPOutput) -> Dict[str, Any]:
        """
        CRP-friendly explanation.
        
        CRPs need to understand:
        - What situation was detected
        - What the teacher might be struggling with
        - Why this strategy was suggested
        """
        
        state_explanations = {
            ClassroomState.MAJOR_DISRUPTION: "Kaksha mein bahut shor ya avsthaa kharaab hai",
            ClassroomState.NO_ATTENTION: "Bachche dhyaan nahi de rahe",
            ClassroomState.CONFUSION: "Bachche samajh nahi pa rahe",
            ClassroomState.MIXED_LEVELS: "Kuch bachche samajh rahe hain, kuch nahi",
            ClassroomState.MULTIGRADE: "Do ya zyada kaksha ek saath padh rahi hai"
        }
        
        intent_explanations = {
            TeacherIntent.REGAIN_ATTENTION: "Teacher ko bachcho ka dhyaan wapas lana hai",
            TeacherIntent.SIMPLIFY_CONCEPT: "Concept ko aasaan banana hai",
            TeacherIntent.CALM_CLASS: "Kaksha ko shaant karna hai",
            TeacherIntent.HANDLE_DISTRACTION: "Distracted bachcho ko sambhalna hai"
        }
        
        return {
            "summary_hi": state_explanations.get(
                output.classroom_state,
                "Kaksha ki sthiti samajh li gayi"
            ),
            "teacher_need_hi": intent_explanations.get(
                output.teacher_intent,
                "Teacher ki zaroorat samjhi gayi"
            ),
            "confidence_level": "Uchch" if output.confidence > 0.8 else "Madhyam" if output.confidence > 0.5 else "Kam",
            "urgency_hi": {
                Urgency.CRITICAL: "Bahut urgent",
                Urgency.HIGH: "Jaldi karna hai",
                Urgency.MEDIUM: "Samay hai",
                Urgency.LOW: "Koi jaldi nahi"
            }.get(output.urgency, "Samay hai")
        }
    
    def _explain_for_admin(self, output: NLPOutput) -> Dict[str, Any]:
        """Administrator-level explanation."""
        
        return {
            "detected_situation": output.classroom_state.value,
            "teacher_need": output.teacher_intent.value,
            "subject_area": output.topic.value,
            "urgency_level": output.urgency.value,
            "language": output.detected_language.value,
            "confidence_score": output.confidence,
            "processing_time_ms": output.processing_time_ms,
            "requires_review": output.requires_clarification or output.confidence < 0.5
        }
    
    def _explain_technical(self, output: NLPOutput) -> Dict[str, Any]:
        """Full technical explanation for debugging."""
        
        return {
            "input": {
                "raw": output.raw_input,
                "normalized": output.normalized_text,
                "translated": output.english_translation
            },
            "classifications": {
                "classroom_state": {
                    "value": output.classroom_state.value,
                    "confidence": output.state_confidence
                },
                "teacher_intent": {
                    "value": output.teacher_intent.value,
                    "confidence": output.intent_confidence
                },
                "urgency": output.urgency.value,
                "topic": output.topic.value
            },
            "language": {
                "primary": output.detected_language.value,
                "secondary": output.secondary_language.value if output.secondary_language else None,
                "low_resource": output.low_resource_language
            },
            "entities": {
                "student_count": output.student_count_mentioned,
                "concept": output.specific_concept
            },
            "metadata": {
                "overall_confidence": output.confidence,
                "processing_time_ms": output.processing_time_ms,
                "model_version": output.model_version,
                "timestamp": output.timestamp.isoformat(),
                "fallback_used": output.fallback_used,
                "requires_clarification": output.requires_clarification
            }
        }
