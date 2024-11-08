from get_content import get_details, get_digital_data, get_job_posting_schema

import requests
import re
import pandas as pd
from urllib.parse import quote

import os
from dotenv import load_dotenv
load_dotenv()

if not os.path.exists("../../bbdd"):
    os.mkdir("../../bbdd")

if not os.mkdir("../../bbdd/backup"):
    os.path.exists("../../bbdd/backup")

def extract_base_url(link):
    pattern = re.compile(r'^https?://([^/]+)')

    match = pattern.match(link)

    base_url = match.group(1) if match else None

    return base_url

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es-AR,es-419;q=0.9,es;q=0.8,en;q=0.7',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


links = []
with open("links.txt", "r") as file:
    links = file.readlines()
    print(links)

df = pd.DataFrame(columns=["url", "digitalData", "jobPostingSchema", "details"])
i = 1
fallos = []

for link in links: 
    print(f"Obteniendo datos del link #{i}")
    i+=1
    if i % 500 == 0 and i > 0:
        df.to_excel(f"../../bbdd/backup/backup_{i / 500}.xlsx")

    base_url = extract_base_url(link)

    headers['authority'] = base_url
    headers['referer'] = f'https://{base_url}/'
    
    encoded_url = quote(link.strip(), safe=':/')
    try:
        response = requests.get(encoded_url, headers=headers)
    except:
        print("no se pudo obtener el link")
        continue

    if response.status_code == 200:
        pass
    else:
        print(f"Request failed with status code: {response.status_code}")
        fallos.append(i)
        continue
    new_data = {
        "url": link,
        "digitalData": get_digital_data(response),
        "jobPostingSchema": get_job_posting_schema(response),
        "details": get_details(response)
    }
    
    new_df = pd.DataFrame([new_data])
    df = pd.concat([df, new_df], ignore_index=True)

df.to_excel("../../bbdd/tecolococrudo.xlsx")