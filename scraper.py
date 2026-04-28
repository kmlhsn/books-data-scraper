"""
========================================================
 📚 Books Scraper — books.toscrape.com
 Author  : Your Name
 Version : 1.0.0
 Purpose : Scrape book titles, prices, ratings & availability
           from books.toscrape.com and export to CSV / JSON.
========================================================
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

# ── Logging ────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────
BASE_URL   = "https://books.toscrape.com/catalogue/"
START_URL  = "https://books.toscrape.com/catalogue/page-1.html"
DELAY      = 1.0          # seconds between requests (be polite!)
OUTPUT_DIR = Path("output")
HEADERS    = {"User-Agent": "Mozilla/5.0 (BooksScraper/1.0)"}

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}


# ── Data Model ─────────────────────────────────────────
@dataclass
class Book:
    title       : str
    price       : float
    rating      : int
    availability: str
    url         : str


# ── Helpers ────────────────────────────────────────────
def fetch_page(url: str) -> Optional[BeautifulSoup]:
    """Fetch a URL and return a BeautifulSoup object, or None on failure."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        log.error(f"Failed to fetch {url}: {e}")
        return None


def parse_price(raw: str) -> float:
    """Convert '£12.34' → 12.34"""
    return float(raw.replace("£", "").replace(",", "").strip())


def parse_books(soup: BeautifulSoup) -> list[Book]:
    """Extract all Book objects from a catalogue page."""
    books = []
    for article in soup.select("article.product_pod"):
        title  = article.h3.a["title"]
        price  = parse_price(article.select_one("p.price_color").text)
        rating = RATING_MAP.get(article.p["class"][1], 0)
        avail  = article.select_one("p.availability").text.strip()
        href   = article.h3.a["href"].replace("../", "")
        url    = BASE_URL + href
        books.append(Book(title, price, rating, avail, url))
    return books


def get_next_page(soup: BeautifulSoup) -> Optional[str]:
    """Return the URL of the next catalogue page, or None if last page."""
    btn = soup.select_one("li.next a")
    if btn:
        return BASE_URL + btn["href"]
    return None


# ── Main Scraper ────────────────────────────────────────
def scrape(max_pages: int = 5) -> list[Book]:
    """
    Scrape up to `max_pages` pages of books.toscrape.com.
    Returns a list of Book dataclass instances.
    """
    all_books: list[Book] = []
    url = START_URL
    page = 1

    while url and page <= max_pages:
        log.info(f"Scraping page {page}: {url}")
        soup = fetch_page(url)
        if not soup:
            break

        books = parse_books(soup)
        all_books.extend(books)
        log.info(f"  → {len(books)} books found (total so far: {len(all_books)})")

        url = get_next_page(soup)
        page += 1
        time.sleep(DELAY)

    log.info(f"Scraping complete. Total books: {len(all_books)}")
    return all_books


# ── Export ──────────────────────────────────────────────
def save_csv(books: list[Book], filename: str = "books.csv") -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    df = pd.DataFrame([asdict(b) for b in books])
    df.to_csv(path, index=False, encoding="utf-8")
    log.info(f"CSV saved → {path}  ({len(df)} rows)")


def save_json(books: list[Book], filename: str = "books.json") -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(b) for b in books], f, indent=2, ensure_ascii=False)
    log.info(f"JSON saved → {path}")


# ── Entry Point ─────────────────────────────────────────
if __name__ == "__main__":
    books = scrape(max_pages=5)   # change to 50 to get all pages
    save_csv(books)
    save_json(books)

    # Quick summary
    df = pd.DataFrame([asdict(b) for b in books])
    print("\n── Summary ──────────────────────────────")
    print(f"Total books  : {len(df)}")
    print(f"Avg price    : £{df['price'].mean():.2f}")
    print(f"Highest rated: {df[df['rating']==5]['title'].count()} five-star books")
    print(f"Cheapest     : {df.loc[df['price'].idxmin(),'title']}  £{df['price'].min()}")
    print(f"Most expensive: {df.loc[df['price'].idxmax(),'title']}  £{df['price'].max()}")
    print("─────────────────────────────────────────\n")
