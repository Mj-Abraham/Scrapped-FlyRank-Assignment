## Target classification
- **Target:** books.toscrape.com — a public sandbox site built for practicing scraping.
- **Scope:** first 3 catalogue pages only, then their 60 linked book pages.
- **robots.txt result:** No robots.txt file found (request returned 404 Not Found).
- **Data collected:** title, price, availability, rating, description.
- I will not reuse this code on another site without checking its rules and terms first.
## How to run
1. Clone this repo
2. Create a virtual environment and activate it
3. `pip install requests beautifulsoup4 pydantic`
4. `cd src && python main.py`

## Record schema
- title (string)
- product_url (URL, canonical identity)
- price_gbp (number)
- price_text (original string)
- availability_text (string)
- rating_text (string or null)
- description (string or null)
- source_page (URL)
- fetched_at (ISO timestamp)

## Politeness rules
- Identifying user-agent on every request
- 10-second timeout per request
- 500ms delay between real requests (cache reads are instant)
- Status code checked before parsing
- All pages cached locally after first fetch

## Sample run report
{
  "started_at": "2026-08-28T17:52:18.744659+00:00",
  "duration_seconds": 2.13,
  "pages_fetched": 60,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1
}

## Limitations
[one honest limitation — e.g. "retry logic is a single retry, not full exponential backoff"]

## Ethics
Use an official API when one exists. Never bypass logins, paywalls, or IP blocks.
Collect only the data needed for the stated purpose.

## Note on the browser question
This assignment needed no browser: the book data is already present in the HTML
the server sends, so a browser would only add cost without adding access to more data.