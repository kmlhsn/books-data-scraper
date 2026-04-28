# 📚 Books Scraper

A professional-grade Python web scraper that collects book data from [books.toscrape.com](https://books.toscrape.com) — a safe, legal practice site designed for scraping.

## 🔍 What It Scrapes
- Book title
- Price (£)
- Star rating (1–5)
- Availability (In stock / Out of stock)
- Direct URL to each book

## 📦 Output
- `output/books.csv` — clean Excel-ready spreadsheet
- `output/books.json` — structured JSON for API use

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the scraper
```bash
python scraper.py
```

### 3. Change number of pages
Inside `scraper.py`, edit this line:
```python
books = scrape(max_pages=5)   # set to 50 for all pages
```

## 🛠️ Tech Stack
| Tool | Purpose |
|---|---|
| `requests` | HTTP requests |
| `BeautifulSoup4` | HTML parsing |
| `pandas` | Data export to CSV |
| `dataclasses` | Clean data modelling |
| `logging` | Professional console output |

## 📁 Project Structure
```
project1_books_scraper/
│
├── scraper.py          ← Main scraper (modular, fully commented)
├── requirements.txt    ← Dependencies
├── output/
│   ├── books.csv       ← Generated after running
│   └── books.json      ← Generated after running
└── README.md
```

## ⚠️ Notes
- A 1-second delay is built in between page requests to be respectful to the server
- This site is publicly designed for scraping practice — 100% legal to use
- Easily extendable to scrape individual book detail pages

## 👤 Author
**Kamal Hasan** — Python & AI Developer
- GitHub: github.com/kmlhsn
- LinkedIn: linkedin.com/in/kmlhsn
- Upwork: upwork.com/kmlhsn
