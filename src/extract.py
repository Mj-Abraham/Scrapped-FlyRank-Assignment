import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from fetcher import fetch


def cache_name_for(url: str) -> str:
    slug = re.sub(r"\W+", "_", url)[-60:]
    return f"cache/book_{slug}.html"


def extract_book(url: str, source_page: str) -> dict:
    html = fetch(url, cache_name_for(url))
    soup = BeautifulSoup(html, "html.parser")

    product = soup.select_one("div.product_main")
    title = product.select_one("h1").get_text(strip=True)
    price_text = product.select_one("p.price_color").get_text(strip=True)
    availability_text = product.select_one("p.availability").get_text(strip=True)

    rating_tag = product.select_one("p.star-rating")
    rating_text = rating_tag["class"][1] if rating_tag else None

    desc_tag = soup.select_one("#product_description ~ p")
    description = desc_tag.get_text(strip=True) if desc_tag else None

    return {
        "title": title,
        "product_url": url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import json
    from discover import discover_book_urls

    urls = discover_book_urls()
    record = extract_book(urls[0], "https://books.toscrape.com/catalogue/page-1.html")
    print(json.dumps(record, indent=2))