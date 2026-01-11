import asyncio
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

async def test_gemini_json():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment!")
        return
    
    client = genai.Client(api_key=api_key)
    
    prompt = """Validate this activity:

Name: Simple Addition
Description: Adding two small numbers
Duration: 10 minutes
Materials: Pencil, Paper
Grade Level: 1

STEPS:
1. Write two numbers
2. Add them together

LEARNING OUTCOME: Learn basic addition

TIPS: Practice makes perfect
"""
    
    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
        config=types.GenerateContentConfig(
            system_instruction="Return valid JSON only",
            temperature=0.1,
            response_mime_type="application/json"
        )
    )
    
    print("=" * 80)
    print("RAW RESPONSE:")
    print("=" * 80)
    print(response.text)
    print("=" * 80)
    print(f"Length: {len(response.text)}")
    print(f"First 200 chars: {response.text[:200]!r}")

asyncio.run(test_gemini_json())
