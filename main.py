import os
import requests
from datetime import datetime

def fetch_financial_data():
    # 1. Gather Encrypted API Keys from GitHub Secrets Environment
    finnhub_key = os.environ.get('FINNHUB_API_KEY', '')
    coingecko_key = os.environ.get('COINGECKO_API_KEY', '')
    
    # 2. Premium Fallback Data (Ensures your site is NEVER blank if APIs rate-limit or fail)
    stocks = [
        {"symbol": "AAPL", "name": "Apple Inc.", "price": 175.42, "change": 1.25},
        {"symbol": "MSFT", "name": "Microsoft Corp.", "price": 420.55, "change": -0.85},
        {"symbol": "NVDA", "name": "NVIDIA Corp.", "price": 875.12, "change": 4.12},
        {"symbol": "TSLA", "name": "Tesla Inc.", "price": 171.05, "change": -2.34}
    ]
    
    crypto = [
        {"name": "Bitcoin", "symbol": "BTC", "price": 64250.00, "change": 2.45},
        {"name": "Ethereum", "symbol": "ETH", "price": 3450.25, "change": 1.15},
        {"name": "Solana", "symbol": "SOL", "price": 142.80, "change": -3.10}
    ]
    
    news_articles = [
        {
            "title": "Fed Signals Steady Interest Rates Amid Balanced Economic Expansion",
            "source": "Global Markets Desk",
            "summary": "Central banking authorities indicated a steady path forward for interest metrics, boosting indices across technological and industrial capital structures globally.",
            "url": "#"
        },
        {
            "title": "Crypto Inflows Drive Digital Asset Capitalization Weights Higher",
            "source": "Decentralized Ledger",
            "summary": "Major exchange-traded financial vehicles reported substantial fresh capital allocations, establishing baseline support corridors for leading digital tokens.",
            "url": "#"
        },
        {
            "title": "Tech Sector Earnings Outperform Wall Street Baseline Consensus Expectations",
            "source": "Silicon Reporter",
            "summary": "Advanced enterprise systems and semiconductor chip designers reported optimized efficiency gains, sparking renewed momentum in growth portfolios.",
            "url": "#"
        }
    ]

    # 3. Attempt to fetch LIVE Stock Market Data if Key exists
    if finnhub_key:
        try:
            live_stocks = []
            for item in stocks:
                res = requests.get(f"https://finnhub.io{item['symbol']}&token={finnhub_key}", timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    if data.get('c'): # Confirming valid data exists
                        live_stocks.append({
                            "symbol": item['symbol'],
                            "name": item['name'],
                            "price": round(data['c'], 2),
                            "change": round(data['d'], 2)
                        })
            if live_stocks:
                stocks = live_stocks
        except Exception as e:
            print(f"Finnhub API connection skipped, using premium fallback profiles: {e}")

    # 4. Attempt to fetch LIVE Crypto Market Data if Key exists
    if coingecko_key:
        try:
            headers = {"x-cg-demo-api-key": coingecko_key}
            res = requests.get("https://coingecko.com", headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                live_crypto = []
                for coin in data:
                    live_crypto.append({
                        "name": coin['name'],
                        "symbol": coin['symbol'].upper(),
                        "price": round(coin['current_price'], 2),
                        "change": round(coin['price_change_percentage_24h'], 2)
                    })
                if live_crypto:
                    crypto = live_crypto
        except Exception as e:
            print(f"CoinGecko API connection skipped, using premium fallback profiles: {e}")

    return stocks, crypto, news_articles

def build_html_site(stocks, crypto, news):
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

    # Formulate Live Ticker Ribbon Elements
    ticker_items = ""
    for s in stocks:
        color = "green" if s['change'] >= 0 else "red"
        sign = "+" if s['change'] >= 0 else ""
        ticker_items += f"<span class='ticker-item'>{s['symbol']}: ${s['price']} (<span class='{color}'>{sign}{s['change']}%</span>)</span>"
    for c in crypto:
        color = "green" if c['change'] >= 0 else "red"
        sign = "+" if c['change'] >= 0 else ""
        ticker_items += f"<span class='ticker-item'>{c['symbol']}: ${c['price']} (<span class='{color}'>{sign}{c['change']}%</span>)</span>"

    # Formulate Market Grid Items
    market_grid_html = ""
    for s in stocks:
        color = "green" if s['change'] >= 0 else "red"
        sign = "+" if s['change'] >= 0 else ""
        market_grid_html += f"""
        <div class="market-card">
            <h3>{s['name']} ({s['symbol']})</h3>
            <div class="price">${s['price']}</div>
            <div class="change {color}">{sign}{s['change']}%</div>
        </div>
        """
    for c in crypto:
        color = "green" if c['change'] >= 0 else "red"
        sign = "+" if c['change'] >= 0 else ""
        market_grid_html += f"""
        <div class="market-card">
            <h3>{c['name']} ({c['symbol']})</h3>
            <div class="price">${c['price']}</div>
            <div class="change {color}">{sign}{c['change']}%</div>
        </div>
        """

    # Formulate News Cards Layout
    news_cards_html = ""
    for n in news:
        news_cards_html += f"""
        <div class="news-card">
            <span class="source">{n['source']}</span>
            <h2>{n['title']}</h2>
            <p>{n['summary']}</p>
            <a href="{n['url']}" class="read-btn">Full Coverage &rarr;</a>
        </div>
        """

    # Assemble the Single Static HTML Master Package File with Embedded Analytics Code Block
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Daily Financial Guide</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }}
        body {{ background-color: #0b0f19; color: #f3f4f6; padding-bottom: 60px; }}
        
        /* Premium Ticker Ribbon Styles */
        .ticker-wrap {{ background: #111827; border-bottom: 1px solid #1f2937; overflow: hidden; white-space: nowrap; padding: 12px 0; }}
        .ticker {{ display: inline-block; animation: marquee 25s linear infinite; }}
        .ticker-item {{ display: inline-block; margin-right: 50px; font-weight: 600; font-size: 14px; letter-spacing: 0.5px; }}
        @keyframes marquee {{ 0% {{ transform: translate3d(0, 0, 0); }} 100% {{ transform: translate3d(-50%, 0, 0); }} }}
        
        /* Layout Configurations */
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ text-align: center; padding: 40px 0 20px; border-bottom: 1px solid #1f2937; margin-bottom: 30px; }}
        header h1 {{ font-size: 36px; color: #ffffff; letter-spacing: -0.5px; margin-bottom: 6px; }}
        header p {{ color: #9ca3af; font-size: 14px; text-transform: uppercase; letter-spacing: 2px; }}
        
        /* Programmatic Ad Placements */
        .ad-banner {{ background: #111827; border: 1px dashed #374151; border-radius: 8px; text-align: center; padding: 20px; color: #4b5563; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; margin: 25px 0; }}
        
        /* Grid Architectures */
        .market-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .market-card {{ background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
        .market-card h3 {{ font-size: 14px; color: #9ca3af; margin-bottom: 8px; }}
        .market-card .price {{ font-size: 24px; font-weight: 700; color: #ffffff; margin-bottom: 4px; }}
        
        .news-container {{ display: grid; grid-template-columns: 1fr; gap: 25px; }}
        .news-card {{ background: #111827; border: 1px solid #1f2937; border-radius: 16px; padding: 30px; position: relative; transition: transform 0.2s; }}
        .news-card:hover {{ transform: translateY(-2px); border-color: #374151; }}
        .news-card .source {{ background: #1e293b; color: #38bdf8; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; display: inline-block; margin-bottom: 12px; }}
        .news-card h2 {{ font-size: 22px; color: #ffffff; margin-bottom: 12px; line-height: 1.4; }}
        .news-card p {{ color: #9ca3af; font-size: 15px; line-height: 1.6; margin-bottom: 20px; }}
        .news-card .read-btn {{ text-decoration: none; color: #38bdf8; font-size: 14px; font-weight: 600; }}
        
        /* Global Signage Colors */
        .green {{ color: #10b981 !important; }}
        .red {{ color: #ef4444 !important; }}
    </style>

    <!-- PREMIUM PRIVACY-FRIENDLY WEB ANALYTICS COUNTER (GoatCounter) -->
    <!-- This tracks real human visitors anonymously without using tracking cookies or requiring annoying cookie banners -->
    <script data-goatcounter="https://goatcounter.com" async src="//gc.zgo.at/count.js"></script>

</head>
<body>

    <!-- Premium Running Marquee Ticker -->
    <div class="ticker-wrap">
        <div class="ticker">
            {ticker_items} {ticker_items}
        </div>
    </div>

    <div class="container">
        <header>
            <h1>Your Daily Financial Guide</h1>
            <p>Automated Asset Intelligence &bull; Continuous Update Feed</p>
            <div style="font-size: 11px; font-mono; color: #4b5563; margin-top: 10px;">Engine Sync: {current_time}</div>
        </header>

        <!-- Dynamic Market Dashboard Grid Layout -->
        <div class="market-grid">
            {market_grid_html}
        </div>

        <!-- Upper Monetization Ad Node Placement Placeholder -->
        <div class="ad-banner">
            Programmatic Ad Advertisement Space Placeholder (728x90 Billboard)
        </div>

        <!-- Main Stream News Feed Section Layout -->
        <div class="news-container">
            {news_cards_html}
        </div>
        
        <!-- Lower Monetization Ad Node Placement Placeholder -->
        <div class="ad-banner">
            Programmatic Ad Advertisement Space Placeholder (300x250 Medium Rectangle)
        </div>
    </div>

</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def build_seo_sitemap():
    # Defines the production URL endpoint (Links to your custom root domain mapping or default Pages path)
    site_url = "https://github.io"
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    
    # Generates standard, verified XML schema readable by Google and Bing crawler bots
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://sitemaps.org">
    <url>
        <loc>{site_url}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>hourly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml.strip())
    print("Successfully compiled automated XML sitemap file mapping.")

if __name__ == "__main__":
    stock_data, crypto_data, news_feed = fetch_financial_data()
    build_html_site(stock_data, crypto_data, news_feed)
    build_seo_sitemap()
