"""
Chanakya NLP Schemas
====================

Fixed taxonomies and Pydantic schemas for deterministic NLP output.

These taxonomies are:
- Finite and closed (no LLM invention)
- Derived from Indian classroom realities
- Validated by CRPs/ARPs/master teachers
- Auditable and governable

CRITICAL: The LLM cannot add new categories. It can only select from these enums.
"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


# =============================================================================
# TAXONOMY: CLASSROOM STATE
# =============================================================================
# What is happening in the classroom RIGHT NOW?
# Based on observations from Indian government primary schools

class ClassroomState(str, Enum):
    """
    Mutually exclusive states of the classroom at the moment of teacher input.
    
    Derived from:
    - Pratham ASER observations
    - DIET classroom documentation
    - CRP field reports
    """
    
    # ATTENTION STATES
    FULL_ATTENTION = "full_attention"           # Students engaged, listening
    PARTIAL_ATTENTION = "partial_attention"     # Some students distracted
    NO_ATTENTION = "no_attention"               # Class has lost focus completely
    
    # ACTIVITY STATES
    INDIVIDUAL_WORK = "individual_work"         # Students working alone (copy, exercise)
    GROUP_WORK = "group_work"                   # Students in groups
    WHOLE_CLASS = "whole_class"                 # Teacher addressing everyone
    TRANSITION = "transition"                   # Moving between activities
    
    # DISRUPTION STATES
    MINOR_DISRUPTION = "minor_disruption"       # 1-2 students off-task
    MAJOR_DISRUPTION = "major_disruption"       # Multiple students, noise, chaos
    CONFLICT = "conflict"                       # Student-student or behavioral issue
    
    # LEARNING STATES
    CONFUSION = "confusion"                     # Students don't understand
    MIXED_LEVELS = "mixed_levels"               # Some get it, some don't
    BOREDOM = "boredom"                         # Students disengaged, topic too easy
    
    # SPECIAL STATES
    MULTIGRADE = "multigrade"                   # Teaching multiple grades simultaneously
    RESOURCE_CRISIS = "resource_crisis"         # Missing materials, space issues
    EXTERNAL_INTERRUPTION = "external_interruption"  # Visitor, announcement, etc.
    
    UNKNOWN = "unknown"                         # Cannot determine


# =============================================================================
# TAXONOMY: TEACHER INTENT
# =============================================================================
# What does the teacher WANT to do or need help with?

class TeacherIntent(str, Enum):
    """
    What the teacher is seeking from the system.
    
    These are ACTION-oriented, not information-oriented.
    Chanakya does not explain; it suggests actions.
    """
    
    # ENGAGEMENT INTENTS
    REGAIN_ATTENTION = "regain_attention"       # "Bachche sun nahi rahe"
    INCREASE_PARTICIPATION = "increase_participation"  # "Koi haath nahi utha raha"
    HANDLE_DISTRACTION = "handle_distraction"   # "Peeche wale baat kar rahe hain"
    
    # COMPREHENSION INTENTS
    SIMPLIFY_CONCEPT = "simplify_concept"       # "Samajh nahi aa raha inko"
    PROVIDE_EXAMPLE = "provide_example"         # "Koi example do"
    CHECK_UNDERSTANDING = "check_understanding" # "Pata nahi samjhe ya nahi"
    
    # DIFFERENTIATION INTENTS
    HELP_STRUGGLING = "help_struggling"         # "Yeh 5 bachche peeche hain"
    CHALLENGE_ADVANCED = "challenge_advanced"   # "Yeh jaldi khatam kar lete hain"
    MANAGE_MULTIGRADE = "manage_multigrade"     # "Do class ek saath"
    
    # BEHAVIOR INTENTS
    HANDLE_CONFLICT = "handle_conflict"         # "Ladai ho rahi hai"
    CALM_CLASS = "calm_class"                   # "Bahut shor hai"
    MOTIVATE_STUDENTS = "motivate_students"     # "Mann nahi lag raha inko"
    
    # ACTIVITY INTENTS
    START_ACTIVITY = "start_activity"           # "Kuch activity karwani hai"
    TRANSITION_ACTIVITY = "transition_activity" # "Ek kaam se doosre pe"
    END_LESSON = "end_lesson"                   # "Kaise band karu"
    
    # RESOURCE INTENTS
    NO_MATERIAL = "no_material"                 # "TLM nahi hai"
    BOARD_ONLY = "board_only"                   # "Sirf board hai"
    
    # ASSESSMENT INTENTS
    QUICK_CHECK = "quick_check"                 # "Jaldi se pata karna hai"
    
    UNKNOWN = "unknown"


# =============================================================================
# TAXONOMY: URGENCY
# =============================================================================
# How quickly does the teacher need a response?

class Urgency(str, Enum):
    """
    Urgency level determines response latency requirements.
    
    CRITICAL: Response within 5 seconds
    HIGH: Response within 15 seconds  
    MEDIUM: Response within 30 seconds
    LOW: Response can wait (rare in live classroom)
    """
    
    CRITICAL = "critical"   # Class falling apart, conflict, immediate need
    HIGH = "high"           # Losing attention, need action soon
    MEDIUM = "medium"       # Planning next step, minor issue
    LOW = "low"             # Reflective question, not urgent
    
    UNKNOWN = "unknown"


# =============================================================================
# TAXONOMY: TOPIC / SUBJECT AREA
# =============================================================================
# What subject/topic is the teacher working on?

class Topic(str, Enum):
    """
    Subject and topic classification for Indian primary curriculum.
    
    Aligned with:
    - NCERT/SCERT curriculum
    - FLN (Foundational Literacy and Numeracy) framework
    - State textbook structures
    """
    
    # FLN - LITERACY
    FLN_PHONICS = "fln_phonics"                 # Letter sounds, akshar
    FLN_WORD_READING = "fln_word_reading"       # Word recognition
    FLN_SENTENCE_READING = "fln_sentence_reading"
    FLN_COMPREHENSION = "fln_comprehension"     # Understanding text
    FLN_WRITING = "fln_writing"                 # Handwriting, copying
    
    # FLN - NUMERACY
    FLN_NUMBER_RECOGNITION = "fln_number_recognition"  # Counting, numerals
    FLN_ADDITION = "fln_addition"
    FLN_SUBTRACTION = "fln_subtraction"
    FLN_MULTIPLICATION = "fln_multiplication"
    FLN_DIVISION = "fln_division"
    FLN_SHAPES = "fln_shapes"                   # Basic geometry
    FLN_MEASUREMENT = "fln_measurement"         # Length, weight, time
    
    # LANGUAGE (beyond FLN)
    LANGUAGE_GRAMMAR = "language_grammar"
    LANGUAGE_VOCABULARY = "language_vocabulary"
    LANGUAGE_COMPOSITION = "language_composition"
    LANGUAGE_POETRY = "language_poetry"
    LANGUAGE_STORY = "language_story"
    
    # MATHEMATICS (beyond FLN)
    MATH_FRACTIONS = "math_fractions"
    MATH_DECIMALS = "math_decimals"
    MATH_WORD_PROBLEMS = "math_word_problems"
    MATH_GEOMETRY = "math_geometry"
    MATH_DATA = "math_data"                     # Tables, graphs
    
    # EVS (Environmental Studies)
    EVS_FAMILY = "evs_family"
    EVS_COMMUNITY = "evs_community"
    EVS_NATURE = "evs_nature"
    EVS_HEALTH = "evs_health"
    EVS_TRANSPORT = "evs_transport"
    EVS_WATER = "evs_water"
    EVS_FOOD = "evs_food"
    
    # GENERAL
    GENERAL_CLASSROOM = "general_classroom"     # Not subject-specific
    
    UNKNOWN = "unknown"


# =============================================================================
# TAXONOMY: DETECTED LANGUAGE
# =============================================================================

class DetectedLanguage(str, Enum):
    """
    Indian languages supported by Chanakya.
    
    Includes ISO 639-1/639-3 codes where available.
    Code-mixed inputs will have primary + secondary language.
    """
    
    HINDI = "hi"
    BENGALI = "bn"
    MARATHI = "mr"
    TAMIL = "ta"
    TELUGU = "te"
    KANNADA = "kn"
    MALAYALAM = "ml"
    GUJARATI = "gu"
    ODIA = "or"
    PUNJABI = "pa"
    ASSAMESE = "as"
    URDU = "ur"
    MAITHILI = "mai"
    SANTALI = "sat"
    KASHMIRI = "ks"
    NEPALI = "ne"
    KONKANI = "kok"
    SINDHI = "sd"
    DOGRI = "doi"
    MANIPURI = "mni"
    BODO = "brx"
    ENGLISH = "en"              # For code-mixing
    
    CODE_MIXED = "code_mixed"   # Multiple languages detected
    UNKNOWN = "unknown"


# =============================================================================
# INPUT SCHEMAS
# =============================================================================

class TeacherUtterance(BaseModel):
    """
    Raw input from teacher (post-ASR).
    
    This is what the NLP pipeline receives.
    """
    
    text: str = Field(
        ...,
        description="Raw transcribed text from teacher speech",
        min_length=1,
        max_length=500
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the utterance was captured"
    )
    
    audio_confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="ASR confidence score if available"
    )
    
    # Optional context from previous turns
    session_id: Optional[str] = Field(
        default=None,
        description="Session identifier for context tracking"
    )


class ClassroomContext(BaseModel):
    """
    Optional contextual information about the classroom.
    
    Provided by teacher profile or session setup.
    Not required for NLP processing but improves accuracy.
    """
    
    grade: Optional[int] = Field(
        default=None,
        ge=1,
        le=8,
        description="Class/grade level (1-8 for primary)"
    )
    
    subject: Optional[str] = Field(
        default=None,
        description="Current subject being taught"
    )
    
    student_count: Optional[int] = Field(
        default=None,
        ge=1,
        le=100,
        description="Number of students in class"
    )
    
    is_multigrade: Optional[bool] = Field(
        default=None,
        description="Whether multiple grades in same room"
    )
    
    teacher_language: Optional[DetectedLanguage] = Field(
        default=None,
        description="Teacher's preferred language"
    )
    
    state: Optional[str] = Field(
        default=None,
        description="Indian state (for curriculum alignment)"
    )
    
    school_type: Optional[str] = Field(
        default=None,
        description="Government/private/aided"
    )


# =============================================================================
# OUTPUT SCHEMAS
# =============================================================================

class NLPOutput(BaseModel):
    """
    Structured output from NLP pipeline.
    
    This is the deterministic JSON that goes to the orchestrator.
    ALL fields are from fixed taxonomies - no LLM invention allowed.
    
    The orchestrator uses this to:
    1. Route to appropriate tools
    2. Query the RAG knowledge base
    3. Generate constrained responses
    """
    
    # === CLASSIFICATION OUTPUTS ===
    
    classroom_state: ClassroomState = Field(
        ...,
        description="Current state of the classroom"
    )
    
    teacher_intent: TeacherIntent = Field(
        ...,
        description="What the teacher needs help with"
    )
    
    urgency: Urgency = Field(
        ...,
        description="How quickly response is needed"
    )
    
    topic: Topic = Field(
        ...,
        description="Subject/topic being taught"
    )
    
    # === LANGUAGE OUTPUTS ===
    
    detected_language: DetectedLanguage = Field(
        ...,
        description="Primary language of input"
    )
    
    secondary_language: Optional[DetectedLanguage] = Field(
        default=None,
        description="Secondary language if code-mixed"
    )
    
    # === NORMALIZED TEXT ===
    
    normalized_text: str = Field(
        ...,
        description="Cleaned, normalized version of input"
    )
    
    english_translation: str = Field(
        ...,
        description="English translation for logging/audit"
    )
    
    # === EXTRACTED ENTITIES ===
    
    student_count_mentioned: Optional[int] = Field(
        default=None,
        description="If teacher mentioned specific number of students"
    )
    
    specific_concept: Optional[str] = Field(
        default=None,
        description="Specific concept mentioned (e.g., 'carrying in addition')"
    )
    
    # === CONFIDENCE SCORES ===
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall confidence in classification"
    )
    
    state_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in classroom_state"
    )
    
    intent_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in teacher_intent"
    )
    
    # === AUDIT FIELDS ===
    
    raw_input: str = Field(
        ...,
        description="Original input text (for audit)"
    )
    
    processing_time_ms: float = Field(
        ...,
        description="Time taken to process (for monitoring)"
    )
    
    model_version: str = Field(
        ...,
        description="Version of NLP pipeline used"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When processing completed"
    )
    
    # === FLAGS ===
    
    requires_clarification: bool = Field(
        default=False,
        description="Whether input was too ambiguous"
    )
    
    low_resource_language: bool = Field(
        default=False,
        description="Whether language has weak NLP support"
    )
    
    fallback_used: bool = Field(
        default=False,
        description="Whether fallback strategy was used"
    )


# =============================================================================
# ORCHESTRATOR ROUTING SCHEMA
# =============================================================================

class OrchestratorInput(BaseModel):
    """
    What the orchestrator receives from NLP layer.
    
    Includes NLP output plus routing hints.
    """
    
    nlp_output: NLPOutput
    
    classroom_context: Optional[ClassroomContext] = None
    
    # Routing hints
    suggested_tools: List[str] = Field(
        default_factory=list,
        description="Tools that should be invoked based on intent"
    )
    
    rag_query: str = Field(
        ...,
        description="Optimized query for RAG retrieval"
    )
    
    rag_filters: dict = Field(
        default_factory=dict,
        description="Filters for RAG (topic, urgency, etc.)"
    )
