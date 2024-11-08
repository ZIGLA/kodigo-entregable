from get_n_links import get_n_links
from get_links import get_links

import requests
import numpy as np

# Environment variables initialization
import os
import json
from dotenv import load_dotenv

load_dotenv()

if not os.path.exists("../../bbdd"):
    os.mkdir("../../bbdd")

if not os.mkdir("../../bbdd/backup"):
    os.path.exists("../../bbdd/backup")

HEADER_BASE = json.loads(os.getenv("HEADER_BASE"))

RESULTS_PER_PAGE = int(os.getenv("RESULTS_PER_PAGE"))
BASE_URL = os.getenv("BASE_URL")

headers = HEADER_BASE
headers['authority'] = BASE_URL
headers['referer'] = f'https://{BASE_URL}/'

url = f'https://{BASE_URL}/empleos?Keywords=&autosuggestEndpoint=%2Fautosuggest&Categoria=1&btnSubmit=%20&Page=1&PerPage={RESULTS_PER_PAGE}&PaisId=0'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Request successful")
else:
    raise(f"Request failed with status code: {response.status_code}")

q_results = get_n_links(response.content)
q_paginas = int(np.ceil(q_results/RESULTS_PER_PAGE))

links = get_links(q_paginas)

with open(f"links.txt", "w+") as file:
    file.writelines(f"%s\n" % link for link in links)