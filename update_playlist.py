# update_playlist.py
# Python 3 script for GitHub Actions
# - reads existing playlist.m3u (keeps header & channel blocks)
# - fetches new VOD items from mykadri (metadata + poster + stream link fallback)
# - writes updated playlist.m3u
# - safe placeholders remain for paid/proprietary channels

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os

# CONFIG
REPO_PLAYLIST = "playlist.m3u"  # file in repo root
MYKADRI_BASE = "https://mykadri.tv"  # base site; adjust if different
MYKADRI_LIST_URL = f"{MYKADRI_BASE}/movies"  # adjust if their structure differs
MAX_MOVIES = 500  # maximum items to import (can tune)
USER_AGENT = "DIMUK100-Playlist-Updater/1.0 (+https://dimuk100-premium.link)"

headers = {"User-Agent": USER_AGENT}

def read_existing_playlist(path=REPO_PLAYLIST):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def write_playlist(lines, path=REPO_PLAYLIST):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def fetch_mykadri_movies_page(url=MYKADRI_LIST_URL):
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r.text

def parse_movie_tiles(html, limit=MAX_MOVIES):
    soup = BeautifulSoup(html, "html.parser")
    movies = []
    cards = soup.select("article, .movie-card, .card, .item") or soup.find_all("a", href=True)
    for c in cards:
        if len(movies) >= limit:
            break
        title = None
        href = None
        poster = None
        a = c if c.name == "a" else c.find("a", href=True)
        if a:
            href = a.get("href")
        img = c.find("img") if hasattr(c, "find") else None
        if img:
            poster = img.get("src") or img.get("data-src")
            title = img.get("alt") or title
        if not title:
            t = c.select_one(".title, .movie-title, h3, h2")
            if t:
                title = t.get_text(strip=True)
        if href and not href.startswith("http"):
            href = MYKADRI_BASE.rstrip("/") + "/" + href.lstrip("/")
        if title and href:
            movies.append({
                "title": title,
                "page_url": href,
                "poster": poster or "",
            })
    seen = set()
    unique = []
    for m in movies:
        if m["page_url"] in seen: continue
        seen.add(m["page_url"])
        unique.append(m)
    return unique[:limit]

def extract_stream_from_movie_page(page_url):
    try:
        r = requests.get(page_url, headers=headers, timeout=20)
        r.raise_for_status()
        html = r.text
        m = re.search(r'(https?:\/\/[^\s\'"]+\.m3u8[^\s\'"]*)', html)
        if m:
            return m.group(1)
        m2 = re.search(r'(https?:\/\/[^\s\'"]+\.mp4[^\s\'"]*)', html)
        if m2:
            return m2.group(1)
    except Exception as e:
        print("stream extract error:", e)
    return page_url

def build_vod_entries(movies):
    lines = []
    lines.append("")
    lines.append("# ───────────── 🎞️ კინო და სერიალები / Movies & Series ─────────────")
    for m in movies:
        title = m.get("title", "Unknown")
        poster = m.get("poster", "")
        page = m.get("page_url", "")
        stream = extract_stream_from_movie_page(page)
        safe_title = title.replace(",", " -")
        ext = f'#EXTINF:-1 tvg-logo="{poster}" group-title="🎬 კინო და სერიალები", {safe_title}'
        lines.append(ext)
        lines.append(stream)
    lines.append("# ───────────────────────────────────────────────────────────")
    return lines

def main():
    print("Starting update:", datetime.utcnow().isoformat())
    existing = read_existing_playlist()
    header = []
    marker = "# 🔄 განახლების ბმული / Update link"
    if marker in existing:
        idx = existing.index(marker)
        header = existing[:idx+3]
    else:
        header = existing[:50]

    try:
        html = fetch_mykadri_movies_page()
        movies = parse_movie_tiles(html, limit=200)
        print("found movies:", len(movies))
    except Exception as e:
        print("Error fetching/parsing mykadri:", e)
        movies = []

    vod_lines = build_vod_entries(movies) if movies else ["# No VOD items found"]

    new_lines = []
    if not header or not header[0].strip().upper().startswith("#EXTM3U"):
        new_lines.append("#EXTM3U")
        new_lines.extend(header)
    else:
        new_lines.extend(header)

    skip = False
    for line in existing:
        if line.strip().startswith("# ───────────── 🎞️"):
            skip = True
        if not skip:
            new_lines.append(line)
    new_lines.extend(vod_lines)
    new_lines.append(f"# Auto-updated: {datetime.utcnow().isoformat()} UTC")
    write_playlist(new_lines)
    print("Playlist updated:", REPO_PLAYLIST)

if __name__ == "__main__":
    main()
