import requests
import time, pprint

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


def walk(query: str, depth: int = 0):
    """Recursively walk the ATO law database TOC."""
    for node in fetch(query):
        if node.get('folder'):
            time.sleep(0.2)  # polite throttle
            # pass only the query string, not BASE + query, fetch BASE + node["data"]["url"]
            yield from walk(node['data']['url'], depth + 1)  # e.g. BASE + "Mode=topic&Action=inject&TOC=02%3AGoods%20and%20services%20tax%3ACharities%20and%20non-profit"
        else:
            yield node


# fetch BASE + ROOT
all_gst_docs = list(walk(ROOT))
pprint.pprint(all_gst_docs)
