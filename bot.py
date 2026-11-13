import os
import feedparser
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

feed_urls = [
    "https://www.ilsole24ore.com/rss/economia.xml",
    "https://xml2.corriereobjects.it/rss/economia.xml",
    "https://xml2.corriereobjects.it/rss/esteri.xml",
    "https://www.ilpost.it/feed/",
    "https://www.bloomberg.com/feeds/economics/news.rss",
    "https://www.theguardian.com/world/rss",
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "https://www.economist.com/finance-and-economics/rss.xml",
    "https://www.economist.com/science-and-technology/rss.xml",
    "https://news.google.com/rss/search?q=site:ft.com+economy+geopolitics+when:24h&hl=en-US&gl=US&ceid=US:en"
]

notizie = []

for url in feed_urls:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:1]:
            titolo = entry.get('title', 'Senza titolo')
            link = entry.get('link', '#')
            notizie.append(f"• <b>{titolo}</b>\n🔗 <a href='{link}'>Leggi l'approfondimento</a>\n")
    except Exception as e:
        print(f"Errore nel recupero del feed {url}: {e}")

if notizie:
    testo_messaggio = "<b>🎯 Briefing Quotidiano: Economia, Geopolitica & Tech</b>\n\n" + "\n".join(notizie[:12])
else:
    testo_messaggio = "⚠️ Al momento non è stato possibile recuperare le notizie."

url_telegram = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": testo_messaggio,
    "parse_mode": "HTML",
    "disable_web_page_preview": True
}

response = requests.post(url_telegram, json=payload)

if response.status_code == 200:
    print("✅ Briefing inviato con successo!")
else:
    print(f"❌ Errore nell'invio: {response.text}")
