"""
Example Test Cases
==================

Comprehensive test cases showing expected NLP outputs for various
Indian language inputs and classroom scenarios.

These examples serve as:
1. Test cases for validation
2. Documentation of expected behavior
3. Training examples for fine-tuning
4. Acceptance criteria for government/NGO review
"""

from datetime import datetime, timezone
from typing import Dict, Any, List

# =============================================================================
# HINDI EXAMPLES
# =============================================================================

HINDI_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "hi_001",
        "description": "Class not paying attention - common scenario",
        "input": {
            "text": "Bachche sun nahi rahe hain bilkul bhi",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "no_attention",
            "teacher_intent": "regain_attention",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "hi",
            "secondary_language": None,
            "normalized_text": "बच्चे सुन नहीं रहे हैं बिल्कुल भी",
            "english_translation": "Children are not listening at all",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.92
        }
    },
    {
        "id": "hi_002",
        "description": "Code-mixed Hindi-English - concept difficulty",
        "input": {
            "text": "Inko addition samajh nahi aa raha, carry wala part",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "fln_addition",
            "detected_language": "hi",
            "secondary_language": "en",
            "normalized_text": "इनको addition समझ नहीं आ रहा, carry वाला part",
            "english_translation": "They are not understanding addition, the carry part",
            "student_count_mentioned": None,
            "specific_concept": "carrying in addition",
            "confidence": 0.88
        }
    },
    {
        "id": "hi_003",
        "description": "Major disruption - urgent",
        "input": {
            "text": "Bahut shor ho raha hai, kuch bhi nahi sun pa rahi main",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "major_disruption",
            "teacher_intent": "calm_class",
            "urgency": "critical",
            "topic": "general_classroom",
            "detected_language": "hi",
            "secondary_language": None,
            "normalized_text": "बहुत शोर हो रहा है, कुछ भी नहीं सुन पा रही मैं",
            "english_translation": "There is too much noise, I cannot hear anything",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.95
        }
    },
    {
        "id": "hi_004",
        "description": "Mixed levels in class",
        "input": {
            "text": "Kuch bachche aa gaye, baaki abhi bhi nahi samjhe",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "mixed_levels",
            "teacher_intent": "help_struggling",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "hi",
            "secondary_language": None,
            "normalized_text": "कुछ बच्चे आ गए, बाकी अभी भी नहीं समझे",
            "english_translation": "Some children got it, others still haven't understood",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.85
        }
    },
    {
        "id": "hi_005",
        "description": "Specific students distracted",
        "input": {
            "text": "Peeche wale 4 bachche baat kar rahe hain",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "minor_disruption",
            "teacher_intent": "handle_distraction",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "hi",
            "secondary_language": None,
            "normalized_text": "पीछे वाले 4 बच्चे बात कर रहे हैं",
            "english_translation": "4 children at the back are talking",
            "student_count_mentioned": 4,
            "specific_concept": None,
            "confidence": 0.91
        }
    },
    {
        "id": "hi_006",
        "description": "No participation",
        "input": {
            "text": "Koi haath nahi utha raha, sab chup hain",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "partial_attention",
            "teacher_intent": "increase_participation",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "hi",
            "secondary_language": None,
            "normalized_text": "कोई हाथ नहीं उठा रहा, सब चुप हैं",
            "english_translation": "No one is raising their hand, everyone is quiet",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.87
        }
    },
    {
        "id": "hi_007",
        "description": "Multigrade classroom",
        "input": {
            "text": "Class 2 aur class 3 dono ek saath, kya karu?",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "multigrade",
            "teacher_intent": "manage_multigrade",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "hi",
            "secondary_language": "en",
            "normalized_text": "Class 2 और class 3 दोनों एक साथ, क्या करूं?",
            "english_translation": "Class 2 and class 3 both together, what should I do?",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.93
        }
    },
    {
        "id": "hi_008",
        "description": "No materials available",
        "input": {
            "text": "TLM nahi hai aaj, sirf board se kaise padhau?",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "resource_crisis",
            "teacher_intent": "board_only",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "hi",
            "secondary_language": "en",
            "normalized_text": "TLM नहीं है आज, सिर्फ board से कैसे पढ़ाऊं?",
            "english_translation": "No TLM today, how do I teach with just the board?",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.89
        }
    }
]


# =============================================================================
# TAMIL EXAMPLES
# =============================================================================

TAMIL_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "ta_001",
        "description": "Students not understanding - Tamil",
        "input": {
            "text": "புரியல இவங்களுக்கு, மறுபடியும் சொல்லணுமா?",
            "language_hint": "ta"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "ta",
            "secondary_language": None,
            "normalized_text": "புரியல இவங்களுக்கு, மறுபடியும் சொல்லணுமா?",
            "english_translation": "They're not understanding, should I explain again?",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.86
        }
    },
    {
        "id": "ta_002",
        "description": "Noisy classroom - Tamil",
        "input": {
            "text": "Class-ல ரொம்ப சத்தம், யாரும் கேக்கல",
            "language_hint": "ta"
        },
        "expected_output": {
            "classroom_state": "major_disruption",
            "teacher_intent": "calm_class",
            "urgency": "critical",
            "topic": "general_classroom",
            "detected_language": "ta",
            "secondary_language": "en",
            "normalized_text": "Class-ல ரொம்ப சத்தம், யாரும் கேக்கல",
            "english_translation": "Too much noise in class, no one is listening",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.90
        }
    },
    {
        "id": "ta_003",
        "description": "Math concept difficulty - Tamil",
        "input": {
            "text": "கழிதல் புரியுது, ஆனா கடன் வாங்குறது புரியல",
            "language_hint": "ta"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "fln_subtraction",
            "detected_language": "ta",
            "secondary_language": None,
            "normalized_text": "கழிதல் புரியுது, ஆனா கடன் வாங்குறது புரியல",
            "english_translation": "They understand subtraction, but not borrowing",
            "student_count_mentioned": None,
            "specific_concept": "borrowing in subtraction",
            "confidence": 0.84
        }
    }
]


# =============================================================================
# BENGALI EXAMPLES
# =============================================================================

BENGALI_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "bn_001",
        "description": "Students talking - Bengali",
        "input": {
            "text": "পেছনের বাচ্চারা কথা বলছে, পড়াতে পারছি না",
            "language_hint": "bn"
        },
        "expected_output": {
            "classroom_state": "minor_disruption",
            "teacher_intent": "handle_distraction",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "bn",
            "secondary_language": None,
            "normalized_text": "পেছনের বাচ্চারা কথা বলছে, পড়াতে পারছি না",
            "english_translation": "Children at the back are talking, I cannot teach",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.88
        }
    },
    {
        "id": "bn_002",
        "description": "Mixed levels - Bengali",
        "input": {
            "text": "কিছু বাচ্চা বুঝেছে, বাকিরা এখনো বসে আছে",
            "language_hint": "bn"
        },
        "expected_output": {
            "classroom_state": "mixed_levels",
            "teacher_intent": "help_struggling",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "bn",
            "secondary_language": None,
            "normalized_text": "কিছু বাচ্চা বুঝেছে, বাকিরা এখনো বসে আছে",
            "english_translation": "Some children understood, others are still sitting",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.85
        }
    },
    {
        "id": "bn_003",
        "description": "Reading difficulty - Bengali",
        "input": {
            "text": "ওরা অক্ষর চিনছে কিন্তু শব্দ পড়তে পারছে না",
            "language_hint": "bn"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "fln_word_reading",
            "detected_language": "bn",
            "secondary_language": None,
            "normalized_text": "ওরা অক্ষর চিনছে কিন্তু শব্দ পড়তে পারছে না",
            "english_translation": "They recognize letters but cannot read words",
            "student_count_mentioned": None,
            "specific_concept": "letter to word transition",
            "confidence": 0.87
        }
    }
]


# =============================================================================
# MARATHI EXAMPLES
# =============================================================================

MARATHI_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "mr_001",
        "description": "Class not focused - Marathi",
        "input": {
            "text": "मुलं लक्ष देत नाहीत, काय करू?",
            "language_hint": "mr"
        },
        "expected_output": {
            "classroom_state": "no_attention",
            "teacher_intent": "regain_attention",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "mr",
            "secondary_language": None,
            "normalized_text": "मुलं लक्ष देत नाहीत, काय करू?",
            "english_translation": "Children are not paying attention, what should I do?",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.91
        }
    },
    {
        "id": "mr_002",
        "description": "Multiplication difficulty - Marathi",
        "input": {
            "text": "गुणाकार येत नाही, पाढे पण पाठ नाहीत",
            "language_hint": "mr"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "fln_multiplication",
            "detected_language": "mr",
            "secondary_language": None,
            "normalized_text": "गुणाकार येत नाही, पाढे पण पाठ नाहीत",
            "english_translation": "They cannot do multiplication, tables also not memorized",
            "student_count_mentioned": None,
            "specific_concept": "multiplication tables",
            "confidence": 0.86
        }
    },
    {
        "id": "mr_003",
        "description": "Student conflict - Marathi",
        "input": {
            "text": "दोन मुलं भांडत आहेत, थांबत नाहीत",
            "language_hint": "mr"
        },
        "expected_output": {
            "classroom_state": "conflict",
            "teacher_intent": "handle_conflict",
            "urgency": "critical",
            "topic": "general_classroom",
            "detected_language": "mr",
            "secondary_language": None,
            "normalized_text": "दोन मुलं भांडत आहेत, थांबत नाहीत",
            "english_translation": "Two children are fighting, not stopping",
            "student_count_mentioned": 2,
            "specific_concept": None,
            "confidence": 0.93
        }
    }
]


# =============================================================================
# TELUGU EXAMPLES
# =============================================================================

TELUGU_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "te_001",
        "description": "Not understanding - Telugu",
        "input": {
            "text": "వాళ్ళకి అర్థం కావడం లేదు, ఏం చేయాలి?",
            "language_hint": "te"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "te",
            "secondary_language": None,
            "normalized_text": "వాళ్ళకి అర్థం కావడం లేదు, ఏం చేయాలి?",
            "english_translation": "They are not understanding, what should I do?",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.87
        }
    },
    {
        "id": "te_002",
        "description": "Classroom chaos - Telugu",
        "input": {
            "text": "క్లాస్‌లో చాలా గొడవ, ఎవరూ వినడం లేదు",
            "language_hint": "te"
        },
        "expected_output": {
            "classroom_state": "major_disruption",
            "teacher_intent": "calm_class",
            "urgency": "critical",
            "topic": "general_classroom",
            "detected_language": "te",
            "secondary_language": None,
            "normalized_text": "క్లాస్‌లో చాలా గొడవ, ఎవరూ వినడం లేదు",
            "english_translation": "Too much disturbance in class, no one is listening",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.91
        }
    }
]


# =============================================================================
# KANNADA EXAMPLES
# =============================================================================

KANNADA_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "kn_001",
        "description": "Attention problem - Kannada",
        "input": {
            "text": "ಮಕ್ಕಳು ಗಮನ ಕೊಡುತ್ತಿಲ್ಲ, ಏನು ಮಾಡಲಿ?",
            "language_hint": "kn"
        },
        "expected_output": {
            "classroom_state": "no_attention",
            "teacher_intent": "regain_attention",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "kn",
            "secondary_language": None,
            "normalized_text": "ಮಕ್ಕಳು ಗಮನ ಕೊಡುತ್ತಿಲ್ಲ, ಏನು ಮಾಡಲಿ?",
            "english_translation": "Children are not paying attention, what should I do?",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.88
        }
    },
    {
        "id": "kn_002",
        "description": "Phonics difficulty - Kannada",
        "input": {
            "text": "ಅಕ್ಷರಗಳ ಧ್ವನಿ ಸರಿಯಾಗಿ ಹೇಳುತ್ತಿಲ್ಲ",
            "language_hint": "kn"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "fln_phonics",
            "detected_language": "kn",
            "secondary_language": None,
            "normalized_text": "ಅಕ್ಷರಗಳ ಧ್ವನಿ ಸರಿಯಾಗಿ ಹೇಳುತ್ತಿಲ್ಲ",
            "english_translation": "Not saying letter sounds correctly",
            "student_count_mentioned": None,
            "specific_concept": "letter sounds/phonics",
            "confidence": 0.85
        }
    }
]


# =============================================================================
# GUJARATI EXAMPLES  
# =============================================================================

GUJARATI_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "gu_001",
        "description": "Distraction - Gujarati",
        "input": {
            "text": "પાછળના છોકરાઓ વાત કરે છે, ધ્યાન નથી આપતા",
            "language_hint": "gu"
        },
        "expected_output": {
            "classroom_state": "minor_disruption",
            "teacher_intent": "handle_distraction",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "gu",
            "secondary_language": None,
            "normalized_text": "પાછળના છોકરાઓ વાત કરે છે, ધ્યાન નથી આપતા",
            "english_translation": "Children at the back are talking, not paying attention",
            "student_count_mentioned": None,
            "specific_concept": None,
            "confidence": 0.87
        }
    },
    {
        "id": "gu_002",
        "description": "Number recognition - Gujarati",
        "input": {
            "text": "અંકો ઓળખે છે પણ ગણતરી નથી આવડતી",
            "language_hint": "gu"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "fln_number_recognition",
            "detected_language": "gu",
            "secondary_language": None,
            "normalized_text": "અંકો ઓળખે છે પણ ગણતરી નથી આવડતી",
            "english_translation": "They recognize numerals but cannot count",
            "student_count_mentioned": None,
            "specific_concept": "counting vs number recognition",
            "confidence": 0.84
        }
    }
]


# =============================================================================
# EDGE CASES AND DIFFICULT INPUTS
# =============================================================================

EDGE_CASES: List[Dict[str, Any]] = [
    {
        "id": "edge_001",
        "description": "Very short input",
        "input": {
            "text": "Shor",
            "language_hint": None
        },
        "expected_output": {
            "classroom_state": "major_disruption",
            "teacher_intent": "calm_class",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "hi",
            "confidence": 0.65,
            "requires_clarification": False
        }
    },
    {
        "id": "edge_002",
        "description": "Heavily code-mixed",
        "input": {
            "text": "Yaar, class mein bahut disturbance hai, bacche focus nahi kar rahe, attention span zero hai",
            "language_hint": None
        },
        "expected_output": {
            "classroom_state": "major_disruption",
            "teacher_intent": "regain_attention",
            "urgency": "critical",
            "topic": "general_classroom",
            "detected_language": "hi",
            "secondary_language": "en",
            "confidence": 0.88
        }
    },
    {
        "id": "edge_003",
        "description": "Romanized Hindi",
        "input": {
            "text": "bachche samajh nahi pa rahe, kya karu",
            "language_hint": None
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "hi",
            "normalized_text": "बच्चे समझ नहीं पा रहे, क्या करूं",
            "confidence": 0.82
        }
    },
    {
        "id": "edge_004",
        "description": "Grammar errors",
        "input": {
            "text": "bachche ko samajh nahi aa raha wo sab topic",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "hi",
            "confidence": 0.78
        }
    },
    {
        "id": "edge_005",
        "description": "Multiple issues mentioned",
        "input": {
            "text": "Kuch bachche samjhe, kuch nahi, aur shor bhi ho raha",
            "language_hint": "hi"
        },
        "expected_output": {
            # System should prioritize most urgent issue
            "classroom_state": "major_disruption",  # Noise is more urgent
            "teacher_intent": "calm_class",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "hi",
            "confidence": 0.75
        }
    },
    {
        "id": "edge_006",
        "description": "Ambiguous input",
        "input": {
            "text": "Kya karu ab?",
            "language_hint": "hi"
        },
        "expected_output": {
            "classroom_state": "unknown",
            "teacher_intent": "unknown",
            "urgency": "medium",
            "topic": "unknown",
            "detected_language": "hi",
            "confidence": 0.35,
            "requires_clarification": True
        }
    }
]


# =============================================================================
# LOW-RESOURCE LANGUAGE EXAMPLES
# =============================================================================

LOW_RESOURCE_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "lr_001",
        "description": "Odia input",
        "input": {
            "text": "ପିଲାମାନେ ଶୁଣୁନାହାଁନ୍ତି",
            "language_hint": "or"
        },
        "expected_output": {
            "classroom_state": "no_attention",
            "teacher_intent": "regain_attention",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "or",
            "english_translation": "Children are not listening",
            "low_resource_language": True,
            "confidence": 0.75
        }
    },
    {
        "id": "lr_002",
        "description": "Assamese input",
        "input": {
            "text": "ল'ৰা-ছোৱালীবোৰে মন দিয়া নাই",
            "language_hint": "as"
        },
        "expected_output": {
            "classroom_state": "no_attention",
            "teacher_intent": "regain_attention",
            "urgency": "high",
            "topic": "general_classroom",
            "detected_language": "as",
            "english_translation": "Children are not paying attention",
            "low_resource_language": True,
            "confidence": 0.72
        }
    },
    {
        "id": "lr_003",
        "description": "Punjabi input",
        "input": {
            "text": "ਬੱਚੇ ਸਮਝ ਨਹੀਂ ਰਹੇ, ਕੀ ਕਰਾਂ?",
            "language_hint": "pa"
        },
        "expected_output": {
            "classroom_state": "confusion",
            "teacher_intent": "simplify_concept",
            "urgency": "medium",
            "topic": "general_classroom",
            "detected_language": "pa",
            "english_translation": "Children are not understanding, what should I do?",
            "confidence": 0.80
        }
    }
]


# =============================================================================
# ALL EXAMPLES COMBINED
# =============================================================================

ALL_EXAMPLES: List[Dict[str, Any]] = (
    HINDI_EXAMPLES +
    TAMIL_EXAMPLES +
    BENGALI_EXAMPLES +
    MARATHI_EXAMPLES +
    TELUGU_EXAMPLES +
    KANNADA_EXAMPLES +
    GUJARATI_EXAMPLES +
    EDGE_CASES +
    LOW_RESOURCE_EXAMPLES
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_examples_by_language(language_code: str) -> List[Dict[str, Any]]:
    """Get all examples for a specific language."""
    return [
        ex for ex in ALL_EXAMPLES 
        if ex.get("input", {}).get("language_hint") == language_code or
           ex.get("expected_output", {}).get("detected_language") == language_code
    ]


def get_examples_by_intent(intent: str) -> List[Dict[str, Any]]:
    """Get all examples for a specific teacher intent."""
    return [
        ex for ex in ALL_EXAMPLES 
        if ex.get("expected_output", {}).get("teacher_intent") == intent
    ]


def get_examples_by_state(state: str) -> List[Dict[str, Any]]:
    """Get all examples for a specific classroom state."""
    return [
        ex for ex in ALL_EXAMPLES 
        if ex.get("expected_output", {}).get("classroom_state") == state
    ]


def get_high_confidence_examples() -> List[Dict[str, Any]]:
    """Get examples with high expected confidence."""
    return [
        ex for ex in ALL_EXAMPLES 
        if ex.get("expected_output", {}).get("confidence", 0) >= 0.85
    ]


def get_low_confidence_examples() -> List[Dict[str, Any]]:
    """Get examples expected to have low confidence."""
    return [
        ex for ex in ALL_EXAMPLES 
        if ex.get("expected_output", {}).get("confidence", 1) < 0.7
    ]
