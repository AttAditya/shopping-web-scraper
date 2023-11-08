from modules.search.search import search_item

def search() -> None:
    """
    Search command
    """

    query: str = input("Search for: ")
    data: list[dict[str, str]] = search_item(query, max_items=100)

    if not data:
        print(f"Could not load any results for {query}")
        return None
    
    for product in data:
        name: str = product["name"]
        price: str = product["price"]
        source: str = product["source"]
        source = f"({source})"

        if len(name) > 30:
            name = name[:27] + "..."
        
        print(f"{name:<30} {source:<20} {price}")
    
    return None

def main() -> None:
    """
    Start program in CLI mode
    """

    while True:
        print("Actions:")
        print("[0] Exit")
        print("[1] Search")

        print()
        option = input("> ")

        match option.lower():
            case "0" | "exit":
                print()
                exit(0)
            case "1" | "search":
                search()
            case _:
                print("Couldn't understand the action. Try again!")
        
        print()

if __name__ == "__main__":
    main()

