import feedparser
import time
import datetime
from datetime import timedelta
import uuid
from gpt4all import GPT4All
# pip install gpt4all==2.2.1.post1
# copy/paste the model file under C:\Users\%USERNAME%\.cache\gpt4all
# https://docs.gpt4all.io/gpt4all_python.html
# List of RSS feeds to aggregate
# Source: https://rss.feedspot.com/cryptocurrency_rss_feeds/
feeds = [
    {'name': 'Coindesk', 'url': 'https://www.coindesk.com/arc/outboundfeeds/rss/'},
    {'name': 'Bitcoin Magazine', 'url': 'https://bitcoinmagazine.com/.rss/full/'},
    {'name': 'Decrypt', 'url': 'https://decrypt.co/feed'},
    {'name': 'The Block', 'url': 'https://www.theblockcrypto.com/rss.xml'},
    {'name': 'Cointelegraph', 'url': 'https://cointelegraph.com/rss'},
    {'name': 'Bitcoinist', 'url': 'https://bitcoinist.com/feed/'},
    {'name': 'NewsBTC', 'url': 'https://www.newsbtc.com/feed/'},
    {'name': 'Cryptopotato', 'url': 'https://cryptopotato.com/feed/'},
    {'name': '99 Bitcoins', 'url': 'https://99bitcoins.com/feed/'},
    {'name': 'Bloomberg', 'url': 'https://feeds.bloomberg.com/markets/news.rss'},
    {'name': 'Investing', 'url': 'https://www.investing.com/rss/news.rss'},
    {'name': 'Market Watch', 'url': 'https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines'},
    {'name': 'Financial Time', 'url': 'https://www.ft.com/news-feed?format=rss'}
    # {'name': 'FEEDNAME', 'url': 'FEEDURL'} /!\ add a comma to the line above
]

# Dictionary to store article IDs and titles
article_ids = {}
# Set to store displayed article IDs
displayed_article_ids = set()

def get_news():
    """Fetch news from the RSS feeds"""
    all_news = {}
    for feed in feeds:
        news = feedparser.parse(feed['url'])
        for entry in news.entries:
            # Generate a unique ID for the article
            article_id = str(uuid.uuid4())
            # Check if the article title already exists
            if entry.title not in article_ids.values():
                article_ids[article_id] = entry.title
                # Add the article ID to the entry
                entry['id'] = article_id
                # Append the entry to the feed's list
                if feed['name'] not in all_news:
                    all_news[feed['name']] = []
                all_news[feed['name']].append(entry)

    return all_news

def display_news(news):
    """Display the news titles and links"""
    for source, entries in news.items():
        print(f"\n# News from {source}")
        for item in entries:
            # Check if the article has already been displayed
            if item.id not in displayed_article_ids:
                print(f"{item.title}: {item.link}")
                displayed_article_ids.add(item.id)
        print("-----------------------------------------------------------------------------------------------")

def summarize_news(news):
    """Generate summaries of news headlines using GPT4All"""
    # Initialize the GPT4All model
    # llm = "C:\\Users\\COL\\.cache\\gpt4all\\qwen1_5-7b-chat-q5_k_m.gguf"
    llm = "C:\\Users\\COL\\.cache\\gpt4all\\Meta-Llama-3-8B.Q5_K_M.gguf"
    # llm = "C:\\Users\\COL\\.cache\\gpt4all\\Phi-3-mini-4k-instruct-q4.gguf"
    # llm = "C:\\Users\\COL\\.cache\\gpt4all\\mistral.7b.openhermes-2.5.gguf_v2.q4_k_m.gguf"
    model = GPT4All(llm, allow_download=False)
    summaries = {}
    for source, entries in news.items():
        headlines = [item.title for item in entries]
        prompt = (
            f"En tant qu'expert en actifs numériques, écrit un résumé en Français des articles suivant: {source}:\n\n"
            + "\n".join(headlines) + 
            "\n\nSummary:"
        )
        summary = model.generate(prompt)
        summaries[source] = summary
    
    return summaries

def main():
    print("Fetching news...\n")
    # Get news at a regular interval (e.g. every 30 minutes)
    while True:
        all_news = get_news()
        update_interval = timedelta(minutes=30)
        next_update_time = datetime.datetime.now() + update_interval
        now = datetime.datetime.now()
        formatNow = now.strftime("%Y/%m/%d %H:%M:%S")
        print(formatNow)
        display_news(all_news)
        print("\nGenerating summaries...")
        summaries = summarize_news(all_news)    
        print("\nSummaries:")
        for source, summary in summaries.items():
            print(f"{source}:")
            print(summary)
            print("-----------------------------------------------------------------------------------------------")
        # time_until_next_update = next_update_time - now
        formatNextNow = next_update_time.strftime("%H:%M:%S")
        print(f"\nNext update at {formatNextNow}")
        print(f"\n\n\n###############################################################################################")
        # time.sleep(time_until_next_update.total_seconds())
        time.sleep(60)
        next_update_time += update_interval

if __name__ == '__main__':
    main()
