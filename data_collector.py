import urllib.request
import xml.etree.ElementTree as ET
import html

# Free, public financial news RSS feeds
FEEDS = {
    "Stock Market News (Yahoo Finance)": "https://finance.yahoo.com/news/rssindex",
    "Crypto News (CoinDesk)": "https://www.coindesk.com/arc/outboundfeeds/rss/"
}

def fetch_news():
    articles_html = ""
    
    for category, url in FEEDS.items():
        articles_html += f"<div class='category-section'><h2>{category}</h2>"
        try:
            # Request feed data mimicking a browser connection
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            items = root.findall('.//item')[:10]  # Grab the 10 newest articles
            
            if not items:
                articles_html += "<p>No recent articles found.</p>"
                
            for item in items:
                title = item.find('title').text if item.find('title') is not None else "No Title"
                link = item.find('link').text if item.find('link') is not None else "#"
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                
                # Format each headline cleanly
                articles_html += f"""
                <div class='article-card'>
                    <h3><a href='{link}' target='_blank'>{html.escape(title)}</a></h3>
                    <p class='date'>{pub_date}</p>
                </div>
                """
        except Exception as e:
            articles_html += f"<p>Error loading feed: {str(e)}</p>"
            
        articles_html += "</div>"
    return articles_html

def build_site():
    news_content = fetch_news()
    
    # Modern, fully mobile-responsive single-page layout
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automated Financial Radar</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
        max-width: 800px; margin: 0 auto;
        header {{ text-align: center; padding: 20px 0; background: #1a2a3a; color: white; border-radius: 8px; margin-bottom: 20px; }}
        h1 {{ margin: 0; font-size: 24px; }}
        .category-section {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 25px; }}
        h2 {{ color: #1a2a3a; border-bottom: 2px solid #eaeaea; padding-bottom: 8px; margin-top: 0; }}
        .article-card {{ padding: 12px 0; border-bottom: 1px solid #f0f0f0; }}
        .article-card:last-child {{ border-bottom: none; }}
        .article-card h3 {{ margin: 0 0 5px 0; font-size: 16px; }}
        .article-card a {{ color: #0066cc; text-decoration: none; }}
        .article-card a:hover {{ text-decoration: underline; }}
        .date {{ font-size: 12px; color: #888; margin: 0; }}
    </style>
</head>
<body>
    <div style="max-width: 800px; margin: 0 auto;">
        <header>
            <h1>Automated Financial Radar</h1>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.8;">24/7 Global Market & Crypto Headlines</p>
        </header>
        {news_content}
    </div>
</body>
</html>"""

    # Write out the complete single page
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    build_site()
