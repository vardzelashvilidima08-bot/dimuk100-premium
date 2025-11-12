import requests
from bs4 import BeautifulSoup
from datetime import datetime

# შექმნის საბოლოო ფაილს
OUTPUT_FILE = "dimuk100.m3u"

# IPTV არხების წყარო (შენი არსებული playlist.m3u)
IPTV_SOURCE = "https://raw.githubusercontent.com/vardzelashvilidima08-bot/dimuk100-premium/main/playlist.m3u"

# MyKadri ძირითადი ბმული
MYKADRI_URL = "https://mykadri.tv"

def fetch_channels():
    try:
        data = requests.get(IPTV_SOURCE, timeout=10).text
        return data
    except Exception as e:
        print("❌ ვერ წამოიღო IPTV არხები:", e)
        return ""

def fetch_mykadri_movies():
    try:
        page = requests.get(MYKADRI_URL, timeout=10).text
        soup = BeautifulSoup(page, "html.parser")

        movies = []
        for a in soup.select(".movie-item a"):
            title = a.get("title") or a.text.strip()
            link = a.get("href")
            if not link.startswith("http"):
                link = MYKADRI_URL + link
            movies.append((title, link))
        return movies
    except Exception as e:
        print("⚠️ ვერ წამოიღო MyKadri ფილმები:", e)
        return []

def build_playlist(channels_text, movies):
    lines = []
    lines.append("#EXTM3U\n")
    lines.append(f"# 📅 განახლდა: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("# 🎨 ფერი: იასამნისფერი თემით\n\n")

    # --- არხების კატეგორიები ---
    categories = {
        "🇬🇪 ქართული არხები (Georgian Channels)": [],
        "⚽ სპორტი (Sports)": [],
        "🎬 კინო და სერიალები (Movies & Series)": [],
        "👶 ბავშვური არხები (Kids)": [],
        "🧠 დოკუმენტური (Documentary)": [],
        "🎵 მუსიკა (Music)": [],
        "⛪ რელიგიური / რეგიონული (Religious / Regional)": [],
        "🌍 საერთაშორისო არხები (World Channels)": [],
        "🎞️ ქართული კინო / VOD (Georgian Movies / VOD)": [],
        "📻 რადიო არხები (Radio)": [],
    }

    # ყველა არსებული არხი გადაიტანე ძირითად ფაილიდან
    for line in channels_text.splitlines():
        lines.append(line)

    # დაამატე MyKadri ფილმები ცალკე კატეგორიად
    lines.append("\n# -------- 🎞️ ქართული კინო / VOD --------\n")
    for title, link in movies:
        lines.append(f'#EXTINF:-1 group-title="ქართული კინო / VOD",{title}\n{link}\n')

    return "".join(lines)

def main():
    channels_text = fetch_channels()
    movies = fetch_mykadri_movies()

    final_text = build_playlist(channels_text, movies)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_text)

    print("✅ dimuk100.m3u წარმატებით განახლდა!")

if __name__ == "__main__":
    main()
