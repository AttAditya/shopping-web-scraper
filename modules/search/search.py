from modules.search import sources

def int_extractor(string: str) -> int:
    """
    Extracts integer from string
    """

    int_string: str = ""

    for ch in [c for c in string]:
        if ch == "." and int_string:
            break

        if not ch.isdigit():
            continue

        int_string += ch

    return int(int_string)

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
    for pid, product in enumerate(collected_data):
        price_int = int_extractor(product["price"])
        price = f"{price_int:,}"
        collected_data[pid]["price"] = f"Rs. {price:>10}"

    return collected_data[:max_items]

