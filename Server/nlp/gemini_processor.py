"""
Gemini 2 Flash Processor
========================

Primary NLP processing using Gemini 2 Flash.

This module handles:
1. Multilingual understanding (all 22+ Indian languages)
2. Language detection and code-mixing identification
3. Intent classification using constrained output
4. Classroom state classification
5. Entity extraction
6. Normalization and translation

CRITICAL DESIGN DECISIONS:
--------------------------

1. STRUCTURED OUTPUT ONLY
   - Gemini is constrained to output valid JSON matching our schemas
   - Enum values are enforced via schema constraints
   - No free-form text generation for classifications

2. NO PEDAGOGY GENERATION
   - Gemini does NOT generate teaching advice
   - It only classifies, extracts, and structures
   - Pedagogy comes from RAG knowledge base

3. PROMPT ENGINEERING FOR INDIAN CONTEXT
   - Prompts include Indian classroom examples
   - Code-mixing patterns explicitly handled
   - Regional language variations considered

4. CONFIDENCE-BASED FALLBACK
   - If confidence < threshold, use fallback strategies
   - Low-resource languages trigger alternative paths
"""

import json
import time
from typing import Optional, Tuple, Dict, Any
from datetime import datetime
from google import genai
from google.genai import types

from .schemas import (
    TeacherUtterance,
    ClassroomContext,
    NLPOutput,
    ClassroomState,
    TeacherIntent,
    Urgency,
    Topic,
    DetectedLanguage,
    OrchestratorInput
)


# =============================================================================
# CONFIGURATION
# =============================================================================

class GeminiConfig:
    """Configuration for Gemini processor."""
    
    MODEL_NAME = "gemini-2.0-flash"
    
    # Temperature = 0 for deterministic classification
    TEMPERATURE = 0.0
    
    # Maximum tokens for NLP output (keep small - we want structured JSON only)
    MAX_OUTPUT_TOKENS = 1024
    
    # Confidence thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.85
    MEDIUM_CONFIDENCE_THRESHOLD = 0.65
    LOW_CONFIDENCE_THRESHOLD = 0.45
    
    # Low-resource language list (weaker NLP support)
    LOW_RESOURCE_LANGUAGES = [
        DetectedLanguage.SANTALI,
        DetectedLanguage.KASHMIRI,
        DetectedLanguage.KONKANI,
        DetectedLanguage.SINDHI,
        DetectedLanguage.DOGRI,
        DetectedLanguage.MANIPURI,
        DetectedLanguage.BODO,
        DetectedLanguage.MAITHILI
    ]
    
    # Safety settings - permissive for educational content
    SAFETY_SETTINGS = [
        types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="BLOCK_ONLY_HIGH"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT", 
            threshold="BLOCK_ONLY_HIGH"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="BLOCK_ONLY_HIGH"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="BLOCK_ONLY_HIGH"
        ),
    ]


# =============================================================================
# SYSTEM PROMPT
# =============================================================================

SYSTEM_PROMPT = """You are the NLP classification layer for Chanakya, a real-time classroom support system for Indian primary school teachers.

YOUR ROLE:
- Analyze short spoken utterances from teachers during live classroom moments
- Classify the classroom state, teacher intent, urgency, and topic
- Handle ALL Indian languages including code-mixed speech
- Output ONLY structured JSON matching the exact schema provided

YOU MUST NOT:
- Generate teaching advice or pedagogy
- Add categories not in the provided enums
- Produce explanations or conversational responses
- Hallucinate confidence scores

INDIAN CLASSROOM CONTEXT:
- Teachers speak informally, often mixing Hindi/English or regional language/English
- Utterances are short (5-30 words), spoken under stress
- Grammar may be broken or informal
- Teachers describe problems, not solutions
- Common patterns:
  * "Bachche sun nahi rahe hain" (Kids aren't listening)
  * "Yeh samajh nahi aa raha inko" (They're not understanding this)
  * "Peeche wale shor macha rahe hain" (Back benchers are making noise)
  * "इनको जोड़ सिखाना है लेकिन carry समझ नहीं आ रहा" (Need to teach addition but they don't get carry)

LANGUAGE HANDLING:
- Detect the primary language from: hi, bn, mr, ta, te, kn, ml, gu, or, pa, as, ur, mai, sat, ks, ne, kok, sd, doi, mni, brx, en
- If code-mixed (e.g., Hindi-English), set detected_language to primary and secondary_language to secondary
- If language unclear, use context clues and set lower confidence
- Always provide English translation for audit logs

CONFIDENCE SCORING:
- 0.9-1.0: Clear, unambiguous input with strong signals
- 0.7-0.89: Confident but some inference required
- 0.5-0.69: Multiple interpretations possible
- 0.3-0.49: Significant ambiguity, may need clarification
- 0.0-0.29: Cannot reliably classify, requires_clarification = true

OUTPUT REQUIREMENTS:
- Return ONLY valid JSON matching the schema
- All enum values must be from the provided lists
- No additional fields or commentary
- If uncertain, prefer "unknown" enum values over guessing"""


# =============================================================================
# CLASSIFICATION PROMPT TEMPLATE
# =============================================================================

CLASSIFICATION_PROMPT = """Analyze this teacher utterance from an Indian primary school classroom:

INPUT TEXT: "{input_text}"

{context_section}

AVAILABLE CLASSIFICATIONS:

classroom_state (pick ONE):
- full_attention: Students engaged, listening
- partial_attention: Some students distracted  
- no_attention: Class has lost focus completely
- individual_work: Students working alone
- group_work: Students in groups
- whole_class: Teacher addressing everyone
- transition: Moving between activities
- minor_disruption: 1-2 students off-task
- major_disruption: Multiple students, noise, chaos
- conflict: Student-student or behavioral issue
- confusion: Students don't understand
- mixed_levels: Some get it, some don't
- boredom: Students disengaged, topic too easy
- multigrade: Teaching multiple grades simultaneously
- resource_crisis: Missing materials, space issues
- external_interruption: Visitor, announcement, etc.
- unknown: Cannot determine

teacher_intent (pick ONE):
- regain_attention: Need to get class focus back
- increase_participation: Want more students involved
- handle_distraction: Deal with specific distracting students
- simplify_concept: Make topic easier to understand
- provide_example: Need a concrete example
- check_understanding: Verify if students understood
- help_struggling: Support students falling behind
- challenge_advanced: Give more work to fast students
- manage_multigrade: Handle multiple grades at once
- handle_conflict: Address student conflicts
- calm_class: Reduce noise/chaos
- motivate_students: Increase engagement/interest
- start_activity: Begin a new activity
- transition_activity: Move between activities
- end_lesson: Close the lesson
- no_material: No teaching materials available
- board_only: Only chalkboard available
- quick_check: Fast assessment needed
- unknown: Cannot determine

urgency (pick ONE):
- critical: Immediate response needed (5 sec) - class falling apart, conflict
- high: Quick response needed (15 sec) - losing attention
- medium: Standard response (30 sec) - planning, minor issues
- low: Can wait - reflective question
- unknown: Cannot determine

topic (pick ONE from these categories):
FLN Literacy: fln_phonics, fln_word_reading, fln_sentence_reading, fln_comprehension, fln_writing
FLN Numeracy: fln_number_recognition, fln_addition, fln_subtraction, fln_multiplication, fln_division, fln_shapes, fln_measurement
Language: language_grammar, language_vocabulary, language_composition, language_poetry, language_story
Mathematics: math_fractions, math_decimals, math_word_problems, math_geometry, math_data
EVS: evs_family, evs_community, evs_nature, evs_health, evs_transport, evs_water, evs_food
General: general_classroom (not subject-specific)
unknown: Cannot determine

detected_language codes:
hi=Hindi, bn=Bengali, mr=Marathi, ta=Tamil, te=Telugu, kn=Kannada, ml=Malayalam, 
gu=Gujarati, or=Odia, pa=Punjabi, as=Assamese, ur=Urdu, mai=Maithili, sat=Santali,
ks=Kashmiri, ne=Nepali, kok=Konkani, sd=Sindhi, doi=Dogri, mni=Manipuri, brx=Bodo,
en=English, code_mixed=Multiple languages, unknown=Cannot detect

RESPOND WITH EXACTLY THIS JSON STRUCTURE:
{{
    "classroom_state": "<enum_value>",
    "teacher_intent": "<enum_value>",
    "urgency": "<enum_value>",
    "topic": "<enum_value>",
    "detected_language": "<language_code>",
    "secondary_language": "<language_code or null>",
    "normalized_text": "<cleaned version of input>",
    "english_translation": "<English translation>",
    "student_count_mentioned": <number or null>,
    "specific_concept": "<concept string or null>",
    "confidence": <0.0-1.0>,
    "state_confidence": <0.0-1.0>,
    "intent_confidence": <0.0-1.0>,
    "requires_clarification": <true/false>
}}

IMPORTANT: Return ONLY the JSON object, no additional text."""


# =============================================================================
# GEMINI PROCESSOR CLASS
# =============================================================================

class GeminiProcessor:
    """
    Main Gemini 2 Flash processor for NLP classification.
    
    Usage:
        processor = GeminiProcessor(api_key="your-key")
        output = await processor.process(utterance, context)
    """
    
    def __init__(self, api_key: str, config: Optional[GeminiConfig] = None):
        """
        Initialize Gemini processor.
        
        Args:
            api_key: Google AI API key
            config: Optional custom configuration
        """
        self.config = config or GeminiConfig()
        
        # Configure Gemini client with new API
        self.client = genai.Client(api_key=api_key)
        
        self.model_version = f"gemini-2.0-flash-chanakya-v0.1"
    
    async def process(
        self,
        utterance: TeacherUtterance,
        context: Optional[ClassroomContext] = None
    ) -> NLPOutput:
        """
        Process teacher utterance and return structured classification.
        
        Args:
            utterance: Raw teacher input
            context: Optional classroom context
            
        Returns:
            NLPOutput with all classifications
        """
        start_time = time.time()
        
        # Build prompt
        prompt = self._build_prompt(utterance.text, context)
        
        # Call Gemini
        try:
            response = await self._call_gemini(prompt)
            parsed = self._parse_response(response)
            
        except Exception as e:
            # Fallback on error
            parsed = self._get_fallback_output(utterance.text, str(e))
        
        # Build final output
        processing_time_ms = (time.time() - start_time) * 1000
        
        output = NLPOutput(
            classroom_state=ClassroomState(parsed.get("classroom_state", "unknown")),
            teacher_intent=TeacherIntent(parsed.get("teacher_intent", "unknown")),
            urgency=Urgency(parsed.get("urgency", "unknown")),
            topic=Topic(parsed.get("topic", "unknown")),
            detected_language=DetectedLanguage(parsed.get("detected_language", "unknown")),
            secondary_language=DetectedLanguage(parsed["secondary_language"]) if parsed.get("secondary_language") else None,
            normalized_text=parsed.get("normalized_text", utterance.text),
            english_translation=parsed.get("english_translation", ""),
            student_count_mentioned=parsed.get("student_count_mentioned"),
            specific_concept=parsed.get("specific_concept"),
            confidence=parsed.get("confidence", 0.5),
            state_confidence=parsed.get("state_confidence", 0.5),
            intent_confidence=parsed.get("intent_confidence", 0.5),
            raw_input=utterance.text,
            processing_time_ms=processing_time_ms,
            model_version=self.model_version,
            requires_clarification=parsed.get("requires_clarification", False),
            low_resource_language=self._is_low_resource(parsed.get("detected_language")),
            fallback_used=parsed.get("fallback_used", False)
        )
        
        return output
    
    def process_sync(
        self,
        utterance: TeacherUtterance,
        context: Optional[ClassroomContext] = None
    ) -> NLPOutput:
        """
        Synchronous version of process().
        
        For environments where async is not available.
        """
        import asyncio
        return asyncio.run(self.process(utterance, context))
    
    def _build_prompt(
        self,
        input_text: str,
        context: Optional[ClassroomContext]
    ) -> str:
        """Build the classification prompt with context."""
        
        context_section = ""
        if context:
            context_parts = []
            if context.grade:
                context_parts.append(f"Grade: {context.grade}")
            if context.subject:
                context_parts.append(f"Subject: {context.subject}")
            if context.student_count:
                context_parts.append(f"Students: {context.student_count}")
            if context.is_multigrade:
                context_parts.append("Multigrade classroom: Yes")
            if context.teacher_language:
                context_parts.append(f"Teacher's language: {context.teacher_language.value}")
            if context.state:
                context_parts.append(f"State: {context.state}")
            
            if context_parts:
                context_section = "CLASSROOM CONTEXT:\n" + "\n".join(context_parts)
        
        return CLASSIFICATION_PROMPT.format(
            input_text=input_text,
            context_section=context_section
        )
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API and return response text."""
        
        response = await self.client.aio.models.generate_content(
            model=self.config.MODEL_NAME,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part(text=prompt)]
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=self.config.TEMPERATURE,
                max_output_tokens=self.config.MAX_OUTPUT_TOKENS,
                response_mime_type="application/json",
                safety_settings=self.config.SAFETY_SETTINGS
            )
        )
        return response.text
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from Gemini."""
        
        # Clean response (remove markdown code blocks if present)
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from Gemini: {e}")
    
    def _is_low_resource(self, language_code: Optional[str]) -> bool:
        """Check if language is low-resource."""
        
        if not language_code:
            return False
        
        try:
            lang = DetectedLanguage(language_code)
            return lang in self.config.LOW_RESOURCE_LANGUAGES
        except ValueError:
            return True  # Unknown language = low resource
    
    def _get_fallback_output(self, input_text: str, error: str) -> Dict[str, Any]:
        """Return fallback output on error."""
        
        return {
            "classroom_state": "unknown",
            "teacher_intent": "unknown",
            "urgency": "medium",
            "topic": "unknown",
            "detected_language": "unknown",
            "secondary_language": None,
            "normalized_text": input_text,
            "english_translation": f"[Processing error: {error}]",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.1,
            "state_confidence": 0.1,
            "intent_confidence": 0.1,
            "requires_clarification": True,
            "fallback_used": True
        }
    
    def build_orchestrator_input(
        self,
        nlp_output: NLPOutput,
        context: Optional[ClassroomContext] = None
    ) -> OrchestratorInput:
        """
        Build input for the orchestrator including routing hints.
        
        This bridges NLP output to the orchestrator layer.
        """
        
        # Determine suggested tools based on intent
        suggested_tools = self._get_suggested_tools(nlp_output)
        
        # Build RAG query
        rag_query = self._build_rag_query(nlp_output)
        
        # Build RAG filters
        rag_filters = {
            "topic": nlp_output.topic.value,
            "urgency": nlp_output.urgency.value,
            "classroom_state": nlp_output.classroom_state.value,
            "intent": nlp_output.teacher_intent.value
        }
        
        return OrchestratorInput(
            nlp_output=nlp_output,
            classroom_context=context,
            suggested_tools=suggested_tools,
            rag_query=rag_query,
            rag_filters=rag_filters
        )
    
    def _get_suggested_tools(self, nlp_output: NLPOutput) -> list:
        """Map intent to suggested tools."""
        
        # Tool routing based on teacher intent
        intent_to_tools = {
            TeacherIntent.REGAIN_ATTENTION: ["attention_strategy", "quick_activity"],
            TeacherIntent.INCREASE_PARTICIPATION: ["participation_technique", "grouping_strategy"],
            TeacherIntent.HANDLE_DISTRACTION: ["behavior_redirect", "seating_change"],
            TeacherIntent.SIMPLIFY_CONCEPT: ["concept_breakdown", "analogy_finder"],
            TeacherIntent.PROVIDE_EXAMPLE: ["example_generator", "local_context"],
            TeacherIntent.CHECK_UNDERSTANDING: ["quick_assessment", "formative_check"],
            TeacherIntent.HELP_STRUGGLING: ["remediation_activity", "peer_support"],
            TeacherIntent.CHALLENGE_ADVANCED: ["extension_activity", "peer_teaching"],
            TeacherIntent.MANAGE_MULTIGRADE: ["multigrade_strategy", "independent_work"],
            TeacherIntent.HANDLE_CONFLICT: ["conflict_resolution", "calm_technique"],
            TeacherIntent.CALM_CLASS: ["attention_getter", "transition_routine"],
            TeacherIntent.MOTIVATE_STUDENTS: ["motivation_technique", "reward_system"],
            TeacherIntent.START_ACTIVITY: ["activity_starter", "engagement_hook"],
            TeacherIntent.TRANSITION_ACTIVITY: ["transition_routine", "cleanup_signal"],
            TeacherIntent.END_LESSON: ["closure_technique", "summary_method"],
            TeacherIntent.NO_MATERIAL: ["no_material_activity", "body_kinesthetic"],
            TeacherIntent.BOARD_ONLY: ["board_activity", "visual_technique"],
            TeacherIntent.QUICK_CHECK: ["quick_assessment", "thumb_check"]
        }
        
        return intent_to_tools.get(nlp_output.teacher_intent, ["general_strategy"])
    
    def _build_rag_query(self, nlp_output: NLPOutput) -> str:
        """Build optimized query for RAG retrieval."""
        
        # Combine key elements for semantic search
        query_parts = []
        
        # Add intent in natural language
        intent_phrases = {
            TeacherIntent.REGAIN_ATTENTION: "get students attention back classroom management",
            TeacherIntent.INCREASE_PARTICIPATION: "increase student participation engagement",
            TeacherIntent.HANDLE_DISTRACTION: "handle distracted students behavior management",
            TeacherIntent.SIMPLIFY_CONCEPT: "simplify concept easier explanation",
            TeacherIntent.PROVIDE_EXAMPLE: "concrete example illustration",
            TeacherIntent.CHECK_UNDERSTANDING: "check understanding formative assessment",
            TeacherIntent.HELP_STRUGGLING: "help struggling students remediation",
            TeacherIntent.CHALLENGE_ADVANCED: "challenge advanced students extension",
            TeacherIntent.MANAGE_MULTIGRADE: "multigrade classroom management",
            TeacherIntent.HANDLE_CONFLICT: "student conflict resolution",
            TeacherIntent.CALM_CLASS: "calm noisy classroom control",
            TeacherIntent.MOTIVATE_STUDENTS: "motivate unmotivated students engagement",
            TeacherIntent.START_ACTIVITY: "start new activity engagement hook",
            TeacherIntent.TRANSITION_ACTIVITY: "transition between activities routine",
            TeacherIntent.END_LESSON: "end lesson closure summary",
            TeacherIntent.NO_MATERIAL: "teaching without materials resources",
            TeacherIntent.BOARD_ONLY: "board only teaching activities",
            TeacherIntent.QUICK_CHECK: "quick assessment check understanding"
        }
        
        if nlp_output.teacher_intent in intent_phrases:
            query_parts.append(intent_phrases[nlp_output.teacher_intent])
        
        # Add topic context
        if nlp_output.topic != Topic.UNKNOWN:
            query_parts.append(nlp_output.topic.value.replace("_", " "))
        
        # Add specific concept if extracted
        if nlp_output.specific_concept:
            query_parts.append(nlp_output.specific_concept)
        
        return " ".join(query_parts)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_processor(api_key: str) -> GeminiProcessor:
    """Factory function to create GeminiProcessor."""
    return GeminiProcessor(api_key=api_key)
