from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import time
import re

BASE_URL = "https://www.pisos.com"
SEARCH_URL = "https://www.pisos.com/venta/pisos-madrid_capital_zona_urbana"
MAX_PROPERTIES = 100


def text(parent, selector):
    try:
        return parent.find_element(By.CSS_SELECTOR, selector).text.strip()
    except:
        return ""


def get_url(card):
    try:
        return card.find_element(
            By.CSS_SELECTOR,
            ".ad-preview__title"
        ).get_attribute("href")
    except:
        return ""


def get_image(card):
    try:
        image = card.find_element(By.CSS_SELECTOR, "img")

        src = image.get_attribute("src")

        if not src:
            src = image.get_attribute("data-src")

        return src or ""

    except:
        return ""


def parse_card(card):
    title = text(card, ".ad-preview__title")
    card_text = card.text.lower()

    rooms = re.search(r"(\d+)\s*(habs?\.?|habitaciones?)", card_text)
    bathrooms = re.search(r"(\d+)\s*(baños?|aseos?)", card_text)
    meters = re.search(r"(\d+)\s*m²", card_text)

    floor = re.search(
        r"(\d+\s*[ªº]?\s*planta|planta\s*\d+|bajo|entreplanta|semisótano|ático|atico)",
        card_text
    )

    return {
        "title": title,
        "url": get_url(card),
        "image": get_image(card),
        "property_type": "unknown",
        "price": text(card, ".ad-preview__price"),
        "location": text(card, ".ad-preview__subtitle"),
        "rooms": rooms.group(0) if rooms else "",
        "bathrooms": bathrooms.group(0) if bathrooms else "",
        "square_meters": meters.group(0) if meters else "",
        "floor": floor.group(0) if floor else "",
    }


driver = webdriver.Chrome()
driver.maximize_window()

rows = []
seen = set()
page = 1

while len(rows) < MAX_PROPERTIES:

    url = SEARCH_URL if page == 1 else f"{SEARCH_URL}/{page}/"

    print(f"Reading page {page}: {url}")

    driver.get(url)

    time.sleep(2)

    if page == 1:
        try:
            driver.find_element(
                By.ID,
                "didomi-notice-agree-button"
            ).click()

            time.sleep(1)

        except:
            pass

    cards = driver.find_elements(
        By.CSS_SELECTOR,
        "div.ad-preview"
    )

    if not cards:
        break

    for card in cards:

        if len(rows) >= MAX_PROPERTIES:
            break

        if "€" not in card.text or "m²" not in card.text:
            continue

        data = parse_card(card)

        if not data["title"] or not data["price"]:
            continue

        key = (
            data["title"] +
            data["price"] +
            data["location"]
        )

        if key in seen:
            continue

        seen.add(key)

        rows.append(data)

        print(f"Saved {len(rows)}: {data['title']}")

    page += 1

driver.quit()

os.makedirs("../data", exist_ok=True)

csv_path = "../data/properties.csv"

with open(csv_path, "w", newline="", encoding="utf-8-sig") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(rows)

print(f"\nSaved {len(rows)} properties to {csv_path}")