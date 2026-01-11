# Query NCERT Books with RAG System

This guide shows you how to query your NCERT books using the RAG (Retrieval-Augmented Generation) system with Gemini LLM.

## How RAG Works

1. **Query Embedding**: Your question is converted to an embedding using `intfloat/multilingual-e5-base`
2. **Similarity Search**: The system finds the most relevant pages from NCERT books using cosine similarity
3. **Context Retrieval**: Top-k most relevant pages are retrieved
4. **LLM Generation**: Gemini LLM generates an answer based on the retrieved context
5. **Response**: You get an answer with source citations (class, subject, book, page number)

## Basic Usage

### 1. Single Question

```bash
python embedding/query_books.py "What is photosynthesis?"
```

### 2. Interactive Mode (Ask Multiple Questions)

```bash
python embedding/query_books.py --interactive
```

Then type your questions. Type `quit` or `exit` to stop.

## Examples

### Simple Questions

```bash
# Science questions
python embedding/query_books.py "Explain the water cycle"
python embedding/query_books.py "What is gravity?"
python embedding/query_books.py "How do plants make food?"

# History questions
python embedding/query_books.py "Who was Ashoka?"
python embedding/query_books.py "What was the Mauryan Empire?"

# Geography questions
python embedding/query_books.py "What are the different types of rocks?"
python embedding/query_books.py "Explain the structure of the Earth"
```

### Filtered Queries

Filter by **Class**:
```bash
python embedding/query_books.py "What is democracy?" --class "Class 6"
python embedding/query_books.py "Explain cells" --class "Class 7"
```

Filter by **Subject**:
```bash
python embedding/query_books.py "Explain gravity" --subject "Science"
python embedding/query_books.py "What is history?" --subject "History"
```

Filter by **Language**:
```bash
python embedding/query_books.py "What is photosynthesis?" --language "English"
```

**Combine Filters**:
```bash
python embedding/query_books.py "Explain cells" --class "Class 7" --subject "Science"
```

### Advanced Options

**Adjust number of sources** (default: 5):
```bash
python embedding/query_books.py "Your question" --top-k 10
```

**Adjust answer creativity** (temperature: 0.0 = factual, 1.0 = creative):
```bash
# More factual/accurate
python embedding/query_books.py "Your question" --temperature 0.3

# More creative
python embedding/query_books.py "Your question" --temperature 0.9
```

## Using in Python Code

You can also use the RAG orchestrator directly in your Python code:

```python
from embedding.rag_orchestrator import RAGOrchestrator

# Initialize
orchestrator = RAGOrchestrator(
    db_path="embedding/ncert_books.db",
    gemini_api_key="your_key"  # or set GEMINI_API_KEY env var
)

# Query
result = orchestrator.query(
    "What is photosynthesis?",
    top_k=5,
    filters={"class": "Class 7", "subject": "Science"},
    temperature=0.7
)

# Access results
print("Answer:", result['answer'])
print("Sources:", result['sources'])

# Close connection
orchestrator.close()
```

## Response Format

The query returns a dictionary with:

```python
{
    'answer': 'Generated answer from Gemini LLM...',
    'sources': [
        {
            'class': 'Class 7',
            'subject': 'Science',
            'bookname': 'fesc101',
            'language': 'English',
            'page_number': '42',
            'content_preview': 'Preview of the page content...'
        },
        # ... more sources
    ],
    'query': 'Your original question'
}
```

## Tips for Better Results

1. **Be Specific**: More specific questions get better results
   - Good: "What is the process of photosynthesis in plants?"
   - Less good: "photosynthesis"

2. **Use Filters**: If you know the class/subject, use filters for more accurate results

3. **Adjust top-k**: For complex questions, increase `--top-k` to get more context

4. **Temperature**: Use lower temperature (0.3-0.5) for factual questions, higher (0.7-0.9) for creative explanations

## Troubleshooting

### Database not found
```bash
# Make sure you've generated embeddings first
python embedding/generate_embeddings.py
```

### No results found
- Try rephrasing your question
- Remove filters to search all books
- Check if the topic exists in the NCERT books

### API key errors
```bash
# Check your API keys
python embedding/check_api_keys.py
```

## Example Session

```bash
$ python embedding/query_books.py --interactive

============================================================
NCERT Books RAG System - Interactive Mode
============================================================
Type 'quit' or 'exit' to stop

Question: What is photosynthesis?

------------------------------------------------------------
Answer:
------------------------------------------------------------
Photosynthesis is the process by which plants, algae, and some 
bacteria convert light energy into chemical energy stored in 
glucose molecules. This process occurs in the chloroplasts of 
plant cells and involves the conversion of carbon dioxide and 
water into glucose and oxygen, using sunlight as the energy source.

------------------------------------------------------------
Sources:
------------------------------------------------------------
1. Class 7 - Science - fesc101 (English), Page 42
2. Class 6 - Science - fesc102 (English), Page 15
3. Class 7 - Science - fesc103 (English), Page 38

Question: Explain the water cycle

------------------------------------------------------------
Answer:
------------------------------------------------------------
...
```
