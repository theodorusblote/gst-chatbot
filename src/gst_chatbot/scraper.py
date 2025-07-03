import requests
import pprint, time

s = requests.Session()
s.headers.update({
    "user-agent": "my-app/0.01",
    "accept": "application/json, text/javascript, */*; q=0.01"
})

BASE = "https://www.ato.gov.au/API/v1/law/lawservices/browse-content/?"
ROOT = "Mode=topic&Action=inject&TOC=01%3AGoods%20and%20services%20tax"  # GST root


def fetch(query: str) -> list[dict]:
    """Perform a GET request to the ATO browse-content endpoint."""
    r = s.get(BASE + query, timeout=(3.05, 27))  # connect timeout (3.05) is the number of seconds Requests will wait for the client to establish a connection. read timeout (27) is the number of seconds the client will wait for the server to send a response
    r.raise_for_status()
    return r.json()


def walk(query: str):
    """Recursively walk the ATO law database TOC to fetch the href link for each document under GST."""
    for node in fetch(query):
        url = node.get('data', {}).get('url')
        if url:
            time.sleep(0.2)
            yield from walk(url)
        else:
            href = node.get('a_attr', {}).get('href')
            if href:
                yield href


if __name__ == "__main__":
    for link in walk(ROOT):
        print(link)
