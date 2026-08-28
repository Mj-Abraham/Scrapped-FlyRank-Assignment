import json
import time
from datetime import datetime, timezone

from discover import discover_book_urls
from extract import extract_book
from normalize import normalize


def run():
    start = time.time()
    started_at = datetime.now(timezone.utc).isoformat()

    urls = discover_book_urls()

    seen = set()
    valid_records = []
    error_records = []
    failed_pages = 0
    pages_fetched = 0

    for url in urls:
        try:
            raw = extract_book(url, source_page="https://books.toscrape.com/catalogue/page-1.html")
            pages_fetched += 1
        except Exception as e:
            print(f"FAILED     {url}  ({e})")
            failed_pages += 1
            continue

        record, error = normalize(raw)
        if error:
            error_records.append(error)
            continue

        if record["product_url"] in seen:
            continue
        seen.add(record["product_url"])
        valid_records.append(record)

    import os
    os.makedirs("output", exist_ok=True)

    with open("output/books.json", "w") as f:
        json.dump(valid_records, f, indent=2)
    with open("output/errors.json", "w") as f:
        json.dump(error_records, f, indent=2)

    report = {
        "started_at": started_at,
        "duration_seconds": round(time.time() - start, 2),
        "pages_fetched": pages_fetched,
        "valid_records": len(valid_records),
        "invalid_records": len(error_records),
        "failed_pages": failed_pages,
    }
    with open("output/run-report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()