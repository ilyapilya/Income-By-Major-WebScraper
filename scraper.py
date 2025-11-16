import time, json, re, requests
from bs4 import BeautifulSoup as bs

BASE_URL = "https://example.com/salaries?page={page}"  # <- change this
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CollegeIncomeScraper/1.0)"
}

def fetch_page_html(page: int) -> str | None:
    url = BASE_URL.format(page=page)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()  # raises on 4xx/5xx
        return resp.text
    except requests.RequestException as e:
        print(f"Unable to fetch page {page}: {e}")
        return None

def parse_income_value(raw_str: str) -> int | None:
    if raw_str is None:
        return None
    
    # Removing whitespace, unwanted characters, and normalizing
    cleaned_str = raw_str.strip().lower().replace("$", "").replace(",", "")

    # Handle for "X k" or "Xk"
    match_k = re.match(r"^(\d+(?:\.\d+)?)\s*k$", s)
    if match_k:
        return int(float(match_k.group(1)) * 1000)

    # Fallback: just digits
    digits = re.findall(r"\d+", s)
    if digits:
        return int("".join(digits))

    return None

if __name__ == "__main__":
    html = fetch_page_html(1)
    print(html[:1000])
