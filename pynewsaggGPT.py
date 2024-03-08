import feedparser
import time
from gpt4all import GPT4All

# copy/paste the model file under C:\Users\%USERNAME%\.cache\gpt4all

# List of RSS feeds to aggregate
feeds = [
    {'name': 'Coindesk', 'url': 'https://www.coindesk.com/arc/outboundfeeds/rss/'},
    {'name': 'Bitcoin Magazine', 'url': 'https://bitcoinmagazine.com/.rss/full/'},
    {'name': 'Decrypt', 'url': 'https://decrypt.co/feed'},
    {'name': 'The Block', 'url': 'https://www.theblockcrypto.com/rss.xml'},
    {'name': 'Cointelegraph', 'url': 'https://cointelegraph.com/rss'}
]

def get_news():
    """Fetch news from the RSS feeds"""
    all_news = {}
    for feed in feeds:
        news = feedparser.parse(feed['url'])
        all_news[feed['name']] = news.entries
    
    return all_news

def display_news(news):
    """Display the news titles and links"""
    for source, entries in news.items():
        print(f"News from {source}:")
        for item in entries:
            print(f"{item.title}: {item.link}")
        print("--------")

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
    print("Fetching news...")
    
    # Get news at a regular interval (e.g. every 30 minutes)
    while True:
        all_news = get_news()
        
        print(f"Found news from {len(all_news)} sources\n")
        
        display_news(all_news)
        
        print("\nGenerating summaries...")
        summaries = summarize_news(all_news)
        
        print("\nSummaries:")
        for source, summary in summaries.items():
            print(f"{source}:")
            print(summary)
            print("--------")
        
        print(f"\nNext update in 30 minutes...")
        time.sleep(30 * 60) # Wait 30 minutes

if __name__ == '__main__':
    main()
