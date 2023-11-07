from modules.search import sources

def int_extractor(string: str) -> int:
    """
    Extracts integer from string
    """

    return int("".join([c for c in string if c.isdigit()]))

def search_item(query: str, *, max_items: int=25) -> list[dict[str, str]]:
    """
    Search for items on several web pages
    """

    collected_data: list[dict[str, str]] = []

    for source in sources:
        print(f"Searching {source.name}")
        source_data: list[dict[str, str]] = source.search(query, thread_count=16)
        collected_data.extend(source_data)

    collected_data.sort(key=lambda product: int_extractor(product["price"]))

    return collected_data[:max_items]

