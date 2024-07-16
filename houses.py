import json
import requests
import time
import pandas as pd
from datetime import datetime
from lxml import html

# TODO: dynamize and make it usable for any city
results = {}

def scrape_apartment(link):
    content = requests.get(link).text
    tree = html.fromstring(content)

    table = tree.xpath("//dl")[0]
    names = [name.xpath("./text()")[0] for name in table.xpath("dt")]
    values = table.xpath("dd")

    a_values = {}
    for idx, name in enumerate(names):
        value = values[idx]
        if value.xpath("./*[contains(@class, 'check')]"): # checkmark
            value = True
        else:
            value = value.xpath("./text()")[0].lstrip().rstrip()

        a_values[name] = value

    results[link] = a_values


link = "https://reality.idnes.cz/s/prodej/byty/praha/"

print(f"[{datetime.now().strftime('%H:%M:%S')}] apartments started loading")
run = True
while run:
    try:
        content = requests.get(link).text
        tree = html.fromstring(content)

        windows = tree.xpath('//*[@class="c-products__inner"]')
        apartment_links = [window.xpath(".//a")[0].get("href") for window in windows]

        for a_link in apartment_links:
            scrape_apartment(a_link)
            time.sleep(1) # not to make too many requests

        next_button = tree.xpath("//a[@class='btn paging__item next']")
        if next_button:
            href = next_button[0].get("href")
            link = f"https://reality.idnes.cz{href}"
        else:
            run = False
    except:
        run = False


print(f"[{datetime.now().strftime('%H:%M:%S')}] apartments finished loading")
print(f"{len(results)} apartments loaded")

with open("praha.json", "w", encoding="utf-8") as fi:
    json.dump(results, fi, ensure_ascii=False)

print(f"[{datetime.now().strftime('%H:%M:%S')}] content exported")