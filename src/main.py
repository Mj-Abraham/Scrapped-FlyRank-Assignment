from fetcher import fetch

if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/page-1.html"
    fetch(url, "cache/catalogue-page-1.html")