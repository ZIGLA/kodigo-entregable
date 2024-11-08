import re
import json
from html import unescape

from bs4 import BeautifulSoup

def get_digital_data(response):
    try:
        regex = r"var digitalData\s*=\s*({[\s\S]*?});"
        compiled_regex = re.compile(regex, re.DOTALL)

        digitalData = compiled_regex.search(response.text)
        if digitalData and digitalData.group(1):
            digitalData = eval(digitalData.group(1).strip())
        return json.dumps(digitalData)
    except Exception as e:
        return {"Error": e}

def get_job_posting_schema(response):
    try:  
        try:
            regex = r'<script\s+id="jobPostingSchema"\s+type="application\/ld\+json">\s*([\s\S]*?)\s*<\/script>'
            compiled_regex = re.compile(regex, re.DOTALL)
            jobPostingSchema = compiled_regex.search(response.text)
            if jobPostingSchema and jobPostingSchema.group(1):
                jobPostingSchema = dict(json.loads(jobPostingSchema.group(1).strip()))
            return json.dumps(jobPostingSchema)
        except Exception as e:
            response_limpio = unescape(response.text)
            response_limpio = response_limpio.replace('&quot;', '')
            jobPostingSchema = compiled_regex.search(response_limpio)
            if jobPostingSchema and jobPostingSchema.group(1):
                jobPostingSchema = dict(json.loads(jobPostingSchema.group(1).strip()))
            return json.dumps(jobPostingSchema)
    except Exception as e:
            print({e: e})
            return {e: e}
            


def get_details(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='detalle-oferta')

    if table is None:
        print("Error")
        exit()
    else:
        table_text = dict()
        for row in table.find_all('tr'):
            row_text = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            if len(row_text) in range(1,3):
                table_text[row_text[0]] = row_text[1] if len(row_text) == 2 else ""
            elif len(row_text) != 0:
                print(row_text)

        return table_text