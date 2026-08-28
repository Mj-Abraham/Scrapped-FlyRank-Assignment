from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fetcher import fetch

MAX_PAGES = 3  # assignment scope: only the first 3 catalogue pages


def discover_book_urls():
    all_urls = []
    page_url = "https://books.toscrape.com/catalogue/page-1.html"
    page_num = 1

    while page_url and page_num <= MAX_PAGES:
        cache_path = f"cache/catalogue-page-{page_num}.html"
        html = fetch(page_url, cache_path)
        soup = BeautifulSoup(html, "html.parser")

        for h3 in soup.select("article.product_pod h3 a"):
            href = h3["href"]
            absolute = urljoin(page_url, href)
            all_urls.append(absolute)

        next_link = soup.select_one("li.next a")
        if next_link and page_num < MAX_PAGES:
            page_num += 1
            page_url = urljoin(page_url, next_link["href"])
        else:
            page_url = None

    unique_urls = list(dict.fromkeys(all_urls))
    print(f"catalogue_pages={page_num} discovered={len(all_urls)} unique_urls={len(unique_urls)}")
    return unique_urls


if __name__ == "__main__":
    discover_book_urls()