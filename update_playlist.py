import requests

# 📺 არხების ჩამონათვალი (შეგიძლია დაამატო ახალი არხები ქვემოთ)
CHANNELS = [
    # 🇬🇪 ქართული არხები
    {
        "name": "პირველი არხი (1TV)",
        "url": "https://livetv.1tv.ge/1tv/1tv.m3u8",
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
        "logo": "https://upload.wikimedia.org/wikipedia/ka/f/f9/Imedi_TV_logo.png",
        "group": "🇬🇪 ქართული არხები"
    },

    # 🌍 World + Geo არხები
    {
        "name": "National Geographic",
        "url": "https://example.com/natgeo.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6a/National_Geographic_Channel_logo.png",
        "group": "🌍 World+Geo"
    },
    {
        "name": "Discovery Channel",
        "url": "https://example.com/discovery.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Discovery_Channel_logo_2019.svg",
        "group": "🌍 World+Geo"
    },

    # 🎬 Mykadri კატეგორია (შეგიძლია დაამატო საკუთარი ბმულები)
    {
        "name": "Mykadri ფილმები",
        "url": "https://mykadri.tv/live.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Film_icon.png",
        "group": "🎬 Mykadri"
    }
]

# 🎯 M3U playlist-ის გენერაცია
def generate_playlist():
    lines = [
        "#EXTM3U",
        "# 🌍 DTI MUK100 World+Geo Premium",
        "# ავტო განახლება GitHub Actions-ით"
    ]
    for ch in CHANNELS:
        lines.append(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["group"]}", {ch["name"]}')
        lines.append(ch["url"])
    return "\n".join(lines)

# 💾 ფაილის შენახვა
def main():
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(generate_playlist())
        print("✅ Playlist updated successfully!")

if __name__ == "__main__":
    main()
