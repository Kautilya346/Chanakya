# NCERT Books Downloader

A Python-based web scraper to download all NCERT textbooks (PDFs) from the official NCERT website (`https://ncert.nic.in/textbook.php`). The script automatically downloads books for all classes, subjects, and languages, organizing them in a structured directory format.

## Features

- **Comprehensive Coverage**: Downloads books for all classes (I-XII) and all available subjects
- **Multi-language Support**: Downloads books in all available languages (English, Hindi, Urdu)
- **Organized Storage**: Automatically organizes books by `Class/Subject/Language`
- **Resume Capability**: Can resume interrupted downloads from the last checkpoint
- **Error Handling**: Robust error handling with retries and detailed logging
- **Rate Limiting**: Respectful delays between downloads to avoid overwhelming the server
- **Progress Tracking**: Real-time progress updates and detailed logging

## Requirements

- Python 3.7 or higher
- Internet connection
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone or download this repository

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

### Basic Usage

Simply run the script to download all NCERT books:

```bash
python download_ncert_books.py
```

### Command Line Options

- `--no-resume`: Start fresh, ignoring any previous progress
  ```bash
  python download_ncert_books.py --no-resume
  ```

- `--delay SECONDS`: Set custom delay between downloads (default: 1.5 seconds)
  ```bash
  python download_ncert_books.py --delay 2.0
  ```

### Examples

Download all books with default settings:
```bash
python download_ncert_books.py
```

Start fresh download (ignore previous progress):
```bash
python download_ncert_books.py --no-resume
```

Download with longer delays (more respectful to server):
```bash
python download_ncert_books.py --delay 3.0
```

## Directory Structure

Downloaded books are organized in the following structure:

```
books/
├── Class_1/
│   ├── Mathematics/
│   │   ├── English/
│   │   │   └── Mathematics_English.pdf
│   │   ├── Hindi/
│   │   │   └── Mathematics_Hindi.pdf
│   │   └── Urdu/
│   │       └── Mathematics_Urdu.pdf
│   └── Science/
│       ├── English/
│       └── Hindi/
├── Class_2/
│   └── ...
└── ...
```

## Progress Tracking

The script maintains progress in two ways:

1. **Progress State File** (`progress_state.json`): Tracks which books have been successfully downloaded, allowing the script to resume from where it left off.

2. **Download Log** (`download_log.txt`): Detailed log file containing:
   - Timestamp of each operation
   - Success/failure status
   - Error messages (if any)
   - Download statistics

## How It Works

1. **Browser Automation**: Uses Playwright to navigate the NCERT website and interact with dynamic dropdowns
2. **Book Discovery**: Systematically iterates through all classes, subjects, and books
3. **Link Extraction**: Extracts download links for all available language versions
4. **PDF Download**: Downloads PDF files using the `requests` library
5. **Validation**: Verifies downloaded files are valid PDFs
6. **Organization**: Saves files in organized directory structure

## Configuration

You can modify the following constants in `download_ncert_books.py`:

- `DOWNLOAD_DELAY`: Delay between downloads (default: 1.5 seconds)
- `MAX_RETRIES`: Maximum retry attempts for failed downloads (default: 3)
- `TIMEOUT`: Timeout for browser operations in milliseconds (default: 30000)
- `BOOKS_DIR`: Directory name for downloaded books (default: "books")

## Error Handling

The script includes comprehensive error handling:

- **Network Errors**: Automatic retries with exponential backoff
- **Timeout Errors**: Configurable timeouts for all operations
- **Invalid Files**: Validation to ensure downloaded files are valid PDFs
- **Missing Books**: Gracefully skips books that are not available
- **Resume on Failure**: Can resume interrupted downloads

## Logging

All operations are logged to both:
- Console (real-time output)
- `download_log.txt` file (detailed log)

Log levels include:
- **INFO**: General progress information
- **WARNING**: Non-critical issues (e.g., book not available in a language)
- **ERROR**: Critical errors that prevent downloads

## Notes

- The script respects the NCERT website by including delays between requests
- Some books may not be available in all languages
- The download process may take several hours depending on:
  - Number of books available
  - Internet connection speed
  - Server response times
- The script can be safely interrupted and resumed later

## Troubleshooting

### Playwright Installation Issues

If you encounter issues with Playwright:

```bash
# Reinstall Playwright
pip uninstall playwright
pip install playwright
playwright install chromium
```

### Download Failures

If downloads fail:

1. Check your internet connection
2. Verify the NCERT website is accessible
3. Check `download_log.txt` for specific error messages
4. Try running with `--no-resume` to start fresh
5. Increase the delay with `--delay` option

### Missing Books

Some books may not be available in all languages. This is normal and the script will log warnings for missing books.

## License

This script is provided as-is for educational purposes. Please respect the NCERT website's terms of service and use responsibly.

## Disclaimer

This tool is for personal/educational use only. Please ensure you comply with NCERT's terms of service and copyright policies when using downloaded materials.
