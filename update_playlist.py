import requests

# ახალი არხების მონაცემების წყარო (შეგიძლია დაამატო mykadri ფილმები ან სხვა)
CHANNELS = [
    {
        "name": "პირველი არხი (1TV)",
        "url": "https://live1tv.1tv.ge/1tv/1tv.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6b/1TV_Georgia_logo.png",
        "group": "🇬🇪 ქართული არხები"
    },
    {
        "name": "რუსთავი 2",
        "url": "https://streaming.cdn77.com/rustavi2/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/en/d/d7/Rustavi_2_2021_logo.png",
        "group": "🇬🇪 ქართული არხები"
    },
    {
        "name": "იმედი TV",
        "url": "https://cdn.ghn.ge/imedi_tv/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/ka/f/f8/Imedi_TV_logo.png",
        "group": "🇬🇪 ქართული არხები"
    }
]

def generate_playlist():
    lines = [
        "EXTM3U",
        "# 💎 DIMUK100 World+Geo Premium",
        "# ავტომატური განახლება ყოველ 6 საათში"
    ]
    for ch in CHANNELS:
        lines.append(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["group"]}", {ch["name"]}')
        lines.append(ch["url"])
    return "\n".join(lines)

def main():
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(generate_playlist())
    print("✅ Playlist updated successfully!")

if __name__ == "__main__":
    main()
