import re

# Simulate what Gemini might be returning based on the error
test_cases = [
    '{"hallucination_score": 0.85, realism_score: 0.9}',  # Mixed quoted/unquoted
    '{hallucination_score: 0.85, "realism_score": 0.9}',  # Mixed unquoted/quoted
    '{ hallucination_score : 0.85 , "realism_score" : 0.9 }',  # Spaces
]

def fix_json(text):
    """Fix common JSON issues"""
    # Remove markdown
    text = re.sub(r'```(?:json)?\s*|\s*```', '', text)
    
    # Extract JSON object
    json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
    if json_match:
        text = json_match.group()
    
    # Fix unquoted keys: Look for pattern like 'word:' (not in quotes)
    # Match: start of string OR { OR , followed by optional whitespace, then word, then optional whitespace, then :
    text = re.sub(r'([,\{]\s*)(\w+)(\s*):', r'\1"\2"\3:', text)
    
    # Remove trailing commas
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    
    return text

print("Testing JSON fixes:\n")
for i, test in enumerate(test_cases, 1):
    print(f"Test {i}: {test}")
    fixed = fix_json(test)
    print(f"Fixed: {fixed}")
    try:
        import json
        result = json.loads(fixed)
        print(f"✓ Valid JSON: {result}\n")
    except Exception as e:
        print(f"✗ Still invalid: {e}\n")
