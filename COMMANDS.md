# NCERT Books RAG System - Commands Guide

## Setup Commands

### 1. Navigate to project directory
```bash
cd "/Users/shyamal/Desktop/code/NCERT Books"
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Edit the `.env` file and add your API keys:
```bash
# Edit .env file
nano .env
# or
vim .env
# or open in your editor
```

Make sure `.env` contains:
```
LLAMA_CLOUD_API_KEY=your_llama_parse_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

## Main Commands

### 4. Generate embeddings for all PDFs (Process all books)
```bash
python embedding/generate_embeddings.py
```

**Options:**
```bash
# Process specific number of files (for testing)
python embedding/generate_embeddings.py --max-files 10

# Use different books directory
python embedding/generate_embeddings.py --books-dir "books"

# Reprocess all files (don't skip existing)
python embedding/generate_embeddings.py --no-skip-existing

# Use custom database path
python embedding/generate_embeddings.py --db-path "embedding/custom.db"
```

### 5. Query the books (Single question)
```bash
python embedding/query_books.py "What is photosynthesis?"
```

**Options:**
```bash
# Interactive mode (ask multiple questions)
python embedding/query_books.py --interactive

# Filter by class
python embedding/query_books.py "What is democracy?" --class "Class 6"

# Filter by subject
python embedding/query_books.py "Explain gravity" --subject "Science"

# Filter by language
python embedding/query_books.py "What is history?" --language "English"

# Combine filters
python embedding/query_books.py "Explain cells" --class "Class 7" --subject "Science"

# Adjust number of sources retrieved
python embedding/query_books.py "Your question" --top-k 10

# Adjust temperature for more creative/accurate answers
python embedding/query_books.py "Your question" --temperature 0.5
```

## Complete Workflow

### Full setup and run:
```bash
# 1. Navigate to project
cd "/Users/shyamal/Desktop/code/NCERT Books"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up .env file (edit with your API keys)
# Make sure .env has LLAMA_CLOUD_API_KEY and GEMINI_API_KEY

# 4. Generate embeddings (this will take time for all PDFs)
python embedding/generate_embeddings.py

# 5. Query the books
python embedding/query_books.py "Your question here"
```

## Quick Test Commands

### Test with a few files first:
```bash
# Process only 5 files to test
python embedding/generate_embeddings.py --max-files 5

# Then query
python embedding/query_books.py "Test question"
```

### Interactive query mode:
```bash
python embedding/query_books.py --interactive
# Then type your questions, type 'quit' to exit
```

## Troubleshooting

### If you get import errors:
```bash
# Make sure you're in the project root directory
cd "/Users/shyamal/Desktop/code/NCERT Books"

# Install dependencies again
pip install -r requirements.txt
```

### If API key errors:
```bash
# Check .env file exists and has correct keys
cat .env

# Or set environment variables directly
export LLAMA_CLOUD_API_KEY="your_key"
export GEMINI_API_KEY="your_key"
```

### Check database:
```bash
# Check if database was created
ls -lh embedding/ncert_books.db

# Check database size (should grow as you process files)
du -h embedding/ncert_books.db
```
