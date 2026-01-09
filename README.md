# Chanakya

> Real-time classroom decision-support system for Indian primary school teachers

## Overview

Chanakya addresses the "implementation gap" in teacher training by providing just-in-time pedagogical support during live classroom moments.

## NLP Layer (Simplified)

The NLP layer simply converts teacher utterances in **any Indian language** to clear **English understanding** using **Gemini 2.5 Flash**.

### Supported Languages
- Hindi, Bengali, Marathi, Tamil, Telugu, Kannada, Malayalam
- Gujarati, Odia, Punjabi, Assamese, Urdu
- Code-mixed speech (Hindi-English, etc.)

### How It Works

```
Teacher (any language) → Gemini 2.5 Flash → English understanding
```

**Input:** `"Bachche sun nahi rahe hain"`  
**Output:** `"The children are not listening"`

**Input:** `"இந்த பாடம் புரியவில்லை அவர்களுக்கு"`  
**Output:** `"They are not understanding this lesson"`

**Input:** `"Addition ka carry samajh nahi aa raha inko"`  
**Output:** `"They are not understanding the carry concept in addition"`

### Usage

```python
from nlp.pipeline import NLPPipeline
from nlp.schemas import TeacherUtterance

# Initialize
pipeline = NLPPipeline(gemini_api_key="your-key")

# Process
utterance = TeacherUtterance(text="Bachche sun nahi rahe hain")
result = pipeline.process_sync(utterance)

print(result.english_understanding)  # "The children are not listening"
print(result.detected_language)      # "hi"
print(result.confidence)             # 0.95
```

### Output Schema

```python
class NLPOutput:
    english_understanding: str   # Clear English version
    detected_language: str       # Language code (hi, ta, bn, etc.)
    raw_input: str              # Original input
    confidence: float           # 0.0 to 1.0
    processing_time_ms: float   # Processing time
    error: Optional[str]        # Error if any
```

## Project Structure

```
Chanakya/
├── README.md
├── Client/                    # Future: Mobile/Web interface
└── Server/
    ├── requirements.txt
    ├── .env                   # Your API key (not in git)
    ├── .env.example           # Template
    ├── test_nlp.py           # Test runner
    └── nlp/
        ├── __init__.py
        ├── schemas.py        # Simple input/output schemas
        ├── gemini_processor.py  # Gemini 2.5 Flash integration
        └── pipeline.py       # Main pipeline
```

## Quick Start

```bash
# Setup
cd Server
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt

# Configure
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Test
python test_nlp.py
```

## License

[TBD]
