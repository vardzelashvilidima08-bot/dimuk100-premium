import requests
from bs4 import BeautifulSoup
import re, os, time
from datetime import datetime

REPO_PLAYLIST = "dimuk100.m3u"
MYKADRI_BASE = "https://mykadri.tv"
HEADERS = {"User-Agent": "DIMUK100-Updater/1.0"}
MAX_PER_CATEGORY = 100

def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print("Fetch error:", url, e)
        return ""

def absolute(url):
    if not url.startswith("http"):
        return MYKADRI_BASE.rstrip("/") + "/" + url.lstrip("/")
    return url

def parse_categories():
    html = fetch(MYKADRI_BASE)
    soup = BeautifulSoup(html, "html.parser")
    cats = []
    for a in soup.select("a[href]"):
        text = a.get_text(strip=True)
        href = a.get("href")
        if href and text and ("/category" in href or "/genres" in href or "/tag" in href):
            cats.append({"name": text, "url": absolute(href)})
    # remove duplicates
    seen = set(); final = []
    for c in cats:
        if c["url"] not in seen:
            seen.add(c["url"])
            final.append(c)
    return final

def parse_items(cat_url):
    html = fetch(cat_url)
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for a in soup.select("a[href]"):
        t = a.get_text(strip=True)
        href = a.get("href")
        if href and t and ("/movie" in href or "/film" in href or "/watch" in href):
            items.append({"title": t, "link": absolute(href)})
    seen = set(); final=[]
    for i in items:
        if i["link"] not in seen:
            seen.add(i["link"])
            final.append(i)
    return final[:MAX_PER_CATEGORY]

def main():
    print("Updating playlist...")
    lines = ["#EXTM3U"]
    cats = parse_categories()
    print("Found", len(cats), "categories")

    for c in cats:
        print("Category:", c["name"])
        lines.append(f"\n# ───────── {c['name']} ─────────")
        items = parse_items(c["url"])
        for i in items:
            lines.append(f'#EXTINF:-1 group-title="🎞 {c["name"]}", {i["title"]}')
            lines.append(i["link"])
        time.sleep(1)

    lines.append(f"# Updated: {datetime.utcnow().isoformat()} UTC")

    with open(REPO_PLAYLIST, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Playlist saved as dimuk100.m3u")

if __name__ == "__main__":
    main()
