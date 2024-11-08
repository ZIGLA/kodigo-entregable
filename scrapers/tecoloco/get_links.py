import requests
from get_page_links import get_page_links

# Environment variables initialization
import os
import json
from dotenv import load_dotenv
load_dotenv()

HEADER_BASE = json.loads(os.getenv("HEADER_BASE"))
RESULTS_PER_PAGE = os.getenv("RESULTS_PER_PAGE")
BASE_URL = os.getenv("BASE_URL")

def get_links(q_paginas):
    headers = HEADER_BASE
    headers['authority'] = BASE_URL
    headers['referer'] = f'https://{BASE_URL}/'
    full_links = []

    for pagina in range(1, q_paginas+1):
        url = f'https://{BASE_URL}/empleos?Keywords=&autosuggestEndpoint=%2Fautosuggest&Categoria=1&btnSubmit=%20&Page={pagina}&PerPage={RESULTS_PER_PAGE}'
        response = requests.get(url, headers=headers)

        l = get_page_links(response)
        if len(l) > 0:
            full_links.extend(l)
        else:
            print("No se encontraron links")

    full_links = list(set(full_links))
    return full_links
