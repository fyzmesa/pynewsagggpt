import feedparser
import time
import datetime
from datetime import timedelta
import uuid
from gpt4all import GPT4All

# copy/paste the model file under C:\Users\%USERNAME%\.cache\gpt4all

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
    model = GPT4All("mistral.7b.openhermes-2.5.gguf_v2.q4_k_m.gguf")
    
    summaries = {}
    for source, entries in news.items():
        headlines = [item.title for item in entries]
        prompt = (
            f"Please summarize the following news headlines from {source}:\n\n"
            + "\n".join(headlines) + 
            "\n\nSummary:"
        )
        
        summary = model.generate(prompt)
        summaries[source] = summary
    
    return summaries


def main():
    print("Fetching news...\n")

    update_interval = timedelta(minutes=30)
    next_update_time = datetime.datetime.now() + update_interval

    # Get news at a regular interval (e.g. every 30 minutes)
    while True:
        all_news = get_news()

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

        time_until_next_update = next_update_time - now
        formatNextNow = next_update_time.strftime("%H:%M:%S")
        print(f"\nNext update at {formatNextNow}")
        print(f"\n\n\n###############################################################################################")
        time.sleep(time_until_next_update.total_seconds())

        next_update_time += update_interval


if __name__ == '__main__':
    main()
