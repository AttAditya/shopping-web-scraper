from requests import Response
from bs4 import BeautifulSoup, Tag
import requests
import threading

class Source:
    name: str = ""

    source: str = ""
    headers: dict[str, str] = {}

    search_dest: str = ""
    user_agents: list[str] = []

    scrape_data: dict[str, list] = {
        "item": [
            [],
            {"class": ""}
        ],
        "name": [
            [],
            {"class": ""}
        ],
        "price": [
            [],
            {"class": ""}
        ]
    }

    thread_search_queue: dict[str, bool] = {}
    thread_search_response: dict[str, str] = {}

    def __init__(self, source: str, *,
        name: str = "",
        headers: dict[str, str] = {},
        search_dest: str = "/",
        user_agents: list[str] = [],
        scrape_data: dict[str, list] = {
            "item": [
                [],
                {"class": ""}
            ],
            "name": [
                [],
                {"class": ""}
            ],
            "price": [
                [],
                {"class": ""}
            ]
        }
    ) -> None:
        """
        Initialize a source
        """

        self.name = name if name else source
        self.source = source
        self.headers = headers
        self.search_dest = search_dest
        self.user_agents = user_agents
        self.scrape_data = scrape_data

        return None
    
    def fetch_page_task(self, dest: str, *,
            user_agent: str = "",
            call_limit: int=25,
            thread_id: int=0
        ) -> str:
        """
        Fetch destination web page from source website
        """

        url: str = f"{self.source}{dest}"

        headers: dict = self.headers
        headers["user-agent"] = user_agent
        
        # print(f"(Thread {thread_id}) ", end="")
        # print(f"Getting response from: {url}")
        resp: Response = requests.get(url, headers=headers)

        call_count: int = 1
        
        while all([
            resp.status_code != 200,
            call_count <= call_limit,
            not self.thread_search_queue[dest]
        ]):
            try:
                # print(f"(Thread {thread_id}) ", end="")
                # print(f"Status: {resp.status_code}, Retrying...({call_count})")
                
                resp = requests.get(url, headers=self.headers)
                call_count += 1
            except requests.exceptions.ConnectionError:
                # print(f"(Thread {thread_id}) ", end="")
                # print("Connection error, retrying")
                pass

        if call_count == call_limit:
            # print(f"(Thread {thread_id}) ", end="")
            # print(f"Exceeded limit of {call_limit} calls")
            return ""
        
        if not self.thread_search_queue[dest]:
            self.thread_search_queue[dest] = True
            self.thread_search_response[dest] = resp.text

        return resp.text
    
    def fetch_page(self, dest: str, *,
            call_limit: int=25,
            thread_limit: int=1
        ) -> str:
        """
        Fetch destination web page from source website(Threaded)
        """

        threads: list[threading.Thread] = []

        for thread_id in range(thread_limit):
            agent_id: int = thread_id % len(self.user_agents)
            thread_agent: str = self.user_agents[agent_id]

            thread_data: dict = {
                "target": self.fetch_page_task,
                "args": [
                    dest
                ],
                "kwargs": {
                    "user_agent": thread_agent,
                    "call_limit": call_limit,
                    "thread_id": thread_id + 1
                }
            }
            current_thread: threading.Thread = threading.Thread(**thread_data)
            threads.append(current_thread)
        
        self.thread_search_queue.update({
            dest: False
        })
        self.thread_search_response.update({
            dest: ""
        })
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        response_data = self.thread_search_response[dest]

        return response_data
    
    def search(self, query: str, *,
            max_items: int=25,
            call_limit: int=25,
            thread_count: int=1
        ) -> list[dict[str, str]]:
        """
        Search for products on Source Website
        """

        url_prefix: str = self.search_dest
        page_html: str = self.fetch_page(
            url_prefix + query,
            call_limit=call_limit,
            thread_limit=thread_count
        )

        soup: BeautifulSoup = BeautifulSoup(page_html, "html.parser")
        raw_results: list[BeautifulSoup] = soup.find_all(
            *self.scrape_data["item"][0],
            **self.scrape_data["item"][1]
        )

        # print(f"Found {min(len(raw_results), max_items)} results")

        results: list[dict[str, str]] = []

        for item_count, div in enumerate(raw_results):
            if item_count >= max_items:
                break

            name: Tag = div.find(
                *self.scrape_data["name"][0],
                **self.scrape_data["name"][1]
            ) # type: ignore

            price: Tag = div.find(
                *self.scrape_data["price"][0],
                **self.scrape_data["price"][1]
            ) # type: ignore

            link: Tag = div.find("a", href=True) # type: ignore

            if not all([name, price, link]):
                continue
            
            if not link["href"].startswith("http"): # type: ignore
                dest = link["href"]
                link["href"] = f"{self.source}{dest}"

            div_data = {
                "name": name.get_text(),
                "price": price.get_text(),
                "link": link["href"],
                "source": self.name
            }

            results.append(div_data)
        
        return results
    
    # TODO
    def cached_search(self, query: str, max_items: int=25) -> list[dict[str, str]]:
        """
        Search but cached
        """

        # TODO: Cache the results temporarily...

        # TODO: Check if today's cache folder exists
        # TODO: If exists, check if query's cache exist
        # TODO: If exists, get cache
        # TODO: If not create cache

        return self.search(query, max_items=max_items)

