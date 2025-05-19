import re


def extract_article_from_url(url: str) -> str | None:
    match = re.search(r'/catalog/(\d+)/', url)
    return match.group(1) if match else None