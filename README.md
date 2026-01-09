# Chanakya

> Real-time classroom decision-support system for Indian primary school teachers

## Overview

Chanakya addresses the "implementation gap" in teacher training by providing just-in-time pedagogical support during live classroom moments. It is NOT a chatbot, tutor, or lesson planner — it is a decision-support system that helps teachers implement training in real-time.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CHANAKYA SYSTEM ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐    ┌────────────────────────────────────────────────────────┐
│   TEACHER    │    │                     NLP LAYER                          │
│   (Speech)   │───▶│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐   │
│              │    │  │  Language   │  │   Intent    │  │  Classroom   │   │
│  "Bachche    │    │  │  Detection  │─▶│  Detection  │─▶│    State     │   │
│   sun nahi   │    │  │             │  │             │  │Classification│   │
│   rahe"      │    │  └─────────────┘  └─────────────┘  └──────────────┘   │
└──────────────┘    │         │                │                │            │
                    │         ▼                ▼                ▼            │
                    │  ┌─────────────────────────────────────────────────┐   │
                    │  │              GEMINI 2 FLASH                      │   │
                    │  │  • Multilingual understanding (22+ languages)   │   │
                    │  │  • Code-mixing handling                         │   │
                    │  │  • Structured JSON output                       │   │
                    │  │  • NO pedagogy generation                       │   │
                    │  └─────────────────────────────────────────────────┘   │
                    │                          │                             │
                    │                          ▼                             │
                    │  ┌─────────────────────────────────────────────────┐   │
                    │  │              STRUCTURED OUTPUT                   │   │
                    │  │  {                                               │   │
                    │  │    "classroom_state": "no_attention",           │   │
                    │  │    "teacher_intent": "regain_attention",        │   │
                    │  │    "urgency": "high",                           │   │
                    │  │    "topic": "fln_addition",                     │   │
                    │  │    "confidence": 0.92                           │   │
                    │  │  }                                               │   │
                    │  └─────────────────────────────────────────────────┘   │
                    └────────────────────────────────────────────────────────┘
                                               │
                                               ▼
                    ┌────────────────────────────────────────────────────────┐
                    │                    ORCHESTRATOR                        │
                    │  • Routes to appropriate tools based on intent         │
                    │  • Queries RAG knowledge base                          │
                    │  • Enforces single-action constraint                   │
                    │  • Validates resource availability                     │
                    └────────────────────────────────────────────────────────┘
                                               │
                                               ▼
                    ┌────────────────────────────────────────────────────────┐
                    │              RAG KNOWLEDGE BASE                        │
                    │  • CRP/ARP strategies                                  │
                    │  • DIET/SCERT compressed material                      │
                    │  • NGO playbooks (Pratham, APF)                        │
                    │  • Master teacher techniques                           │
                    └────────────────────────────────────────────────────────┘
                                               │
                                               ▼
                    ┌────────────────────────────────────────────────────────┐
                    │                SPOKEN OUTPUT                           │
                    │  ONE atomic, actionable instruction                    │
                    │  In teacher's language                                 │
                    │  Using only available resources                        │
                    │  Within 10-30 seconds                                  │
                    └────────────────────────────────────────────────────────┘
```

## NLP Layer Design

### What the NLP Layer Does

| Component | Function | Output |
|-----------|----------|--------|
| Language Detection | Identify primary language from 22+ Indian languages | `detected_language: "hi"` |
| Code-Mix Handling | Detect mixed language input (Hindi-English, etc.) | `secondary_language: "en"` |
| Intent Detection | Classify what teacher needs help with | `teacher_intent: "regain_attention"` |
| State Classification | Determine current classroom situation | `classroom_state: "no_attention"` |
| Urgency Detection | Assess how quickly response is needed | `urgency: "high"` |
| Topic Tagging | Identify subject/curriculum area | `topic: "fln_addition"` |
| Normalization | Clean and structure noisy speech input | `normalized_text: "..."` |

### What the LLM Does (Gemini 2 Flash)

✅ **ALLOWED:**
- Multilingual text understanding
- Language detection and code-mixing identification
- Classification into fixed taxonomies
- Entity extraction (numbers, concepts)
- Text normalization and translation
- Structured JSON generation

❌ **NOT ALLOWED:**
- Generating teaching advice or pedagogy
- Creating new categories outside taxonomies
- Producing conversational responses
- Making resource assumptions
- Multi-step action generation

### What IndicBERT Does (Optional)

IndicBERT is reserved for future use when:
- Sub-100ms latency is required
- Offline/edge deployment is needed
- High-volume production scaling
- Deterministic audit trail required

For v0.1, Gemini 2 Flash handles all NLP tasks.

## Fixed Taxonomies

### Classroom States
```
full_attention, partial_attention, no_attention
individual_work, group_work, whole_class, transition
minor_disruption, major_disruption, conflict
confusion, mixed_levels, boredom
multigrade, resource_crisis, external_interruption
```

### Teacher Intents
```
regain_attention, increase_participation, handle_distraction
simplify_concept, provide_example, check_understanding
help_struggling, challenge_advanced, manage_multigrade
handle_conflict, calm_class, motivate_students
start_activity, transition_activity, end_lesson
no_material, board_only, quick_check
```

### Urgency Levels
```
critical  - Response within 5 seconds (class falling apart)
high      - Response within 15 seconds (losing attention)
medium    - Response within 30 seconds (planning next step)
low       - Response can wait (reflective question)
```

### Supported Languages
```
Hindi, Bengali, Marathi, Tamil, Telugu, Kannada, Malayalam
Gujarati, Odia, Punjabi, Assamese, Urdu, Maithili, Santali
Kashmiri, Nepali, Konkani, Sindhi, Dogri, Manipuri, Bodo
```

## Example Inputs and Outputs

### Hindi Input
```
Input: "Bachche sun nahi rahe hain bilkul bhi"

Output:
{
  "classroom_state": "no_attention",
  "teacher_intent": "regain_attention",
  "urgency": "high",
  "topic": "general_classroom",
  "detected_language": "hi",
  "normalized_text": "बच्चे सुन नहीं रहे हैं बिल्कुल भी",
  "english_translation": "Children are not listening at all",
  "confidence": 0.92
}
```

### Code-Mixed Hindi-English
```
Input: "Inko addition samajh nahi aa raha, carry wala part"

Output:
{
  "classroom_state": "confusion",
  "teacher_intent": "simplify_concept",
  "urgency": "medium",
  "topic": "fln_addition",
  "detected_language": "hi",
  "secondary_language": "en",
  "specific_concept": "carrying in addition",
  "confidence": 0.88
}
```

### Tamil Input
```
Input: "Class-ல ரொம்ப சத்தம், யாரும் கேக்கல"

Output:
{
  "classroom_state": "major_disruption",
  "teacher_intent": "calm_class",
  "urgency": "critical",
  "topic": "general_classroom",
  "detected_language": "ta",
  "english_translation": "Too much noise in class, no one is listening",
  "confidence": 0.90
}
```

### Bengali Input
```
Input: "পেছনের বাচ্চারা কথা বলছে, পড়াতে পারছি না"

Output:
{
  "classroom_state": "minor_disruption",
  "teacher_intent": "handle_distraction",
  "urgency": "high",
  "detected_language": "bn",
  "english_translation": "Children at the back are talking, I cannot teach",
  "confidence": 0.88
}
```

## Governance & Safety

### Preventing Hallucination
1. **Fixed taxonomies**: LLM can only select from predefined enum values
2. **JSON schema enforcement**: Output validated against Pydantic schemas
3. **RAG-only pedagogy**: Teaching strategies retrieved, not generated
4. **Confidence thresholds**: Low confidence triggers clarification requests

### Enforcing Constraints
1. **Single action only**: Multi-step responses rejected
2. **No abstract advice**: Outputs must be immediately actionable
3. **No new resources**: Assumes only chalk, board, students, voice
4. **Language appropriate**: Response in teacher's detected language

### Audit Logging
Every NLP processing event logs:
- Raw input (optionally redacted)
- All classification outputs
- Confidence scores
- Processing time
- Model version
- Fallback triggers
- Validation errors

### Explainability
System generates explanations for:
- **CRPs**: Hindi explanation of situation and teacher need
- **Administrators**: Classification summary with confidence
- **Technical**: Full debug information

## Project Structure

```
Chanakya/
├── README.md
├── Client/                    # Future: Mobile/Web interface
└── Server/
    ├── requirements.txt
    ├── test_nlp.py           # Test runner
    └── nlp/
        ├── __init__.py
        ├── schemas.py        # Pydantic schemas and taxonomies
        ├── gemini_processor.py  # Gemini 2 Flash integration
        ├── indic_classifier.py  # IndicBERT (optional, stub)
        ├── pipeline.py       # Main NLP pipeline
        ├── governance.py     # Safety and constraint enforcement
        └── examples.py       # Test cases in multiple languages
```

## Quick Start

```bash
# Install dependencies
cd Server
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY="your-api-key"

# Run tests
python test_nlp.py
```

## Low-Resource Language Strategy

For languages with weaker NLP support (Santali, Kashmiri, Dogri, etc.):

1. **Gemini's multilingual training** covers most Indian languages
2. **Romanized input** accepted and normalized
3. **Confidence scoring** indicates reliability
4. **Fallback to similar language** patterns when needed
5. **Future**: Collect training data for IndicBERT fine-tuning

## Design Constraints

This system is designed for:
- ✅ Indian government primary schools
- ✅ High student-teacher ratios (40-60 students)
- ✅ Multi-grade classrooms
- ✅ Limited resources (chalk, board only)
- ✅ Informal, code-mixed speech
- ✅ 10-30 second response requirement

This system is NOT designed for:
- ❌ Western classroom norms
- ❌ Technology-rich environments
- ❌ Written text input
- ❌ Lesson planning
- ❌ Student assessment
- ❌ Teacher evaluation

## License

[TBD]

## Acknowledgments

Built for Indian teachers, with input from:
- CRPs and ARPs from government schools
- DIET and SCERT educators
- NGO partners (Pratham, Azim Premji Foundation)