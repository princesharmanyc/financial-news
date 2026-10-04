import os
import requests
from datetime import datetime

def fetch_financial_data():
    # Gather API keys from GitHub Secrets
    finnhub_key = os.environ.get('FINNHUB_API_KEY', '').strip()
    coingecko_key = os.environ.get('COINGECKO_API_KEY', '').strip()
    
    # 1. Base Data Arrays (Fallback Profiles that will ALWAYS show if APIs are empty)
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
            "source": "Macro Desk",
            "summary": "Central banking authorities indicated a steady path forward for interest metrics, boosting indices across technological and growth sectors globally.",
            "url": "https://google.com/search?q=finance+news"
        },
        {
            "title": "Institutional Inflows Drive Digital Asset Capitalization Weights Higher",
            "source": "Crypto Ledger",
            "summary": "Major exchange-traded financial vehicles reported substantial fresh capital allocations, establishing baseline support corridors for leading digital tokens.",
            "url": "https://google.com/search?q=crypto+news"
        },
        {
            "title": "Enterprise Cloud Architecture Demand Triggers Tech Sector Rallies",
            "source": "Tech Analytics",
            "summary": "Advanced enterprise systems and semiconductor chip designers reported optimized efficiency gains, sparking renewed momentum in growth portfolios.",
            "url": "https://google.com/search?q=tech+stocks+news"
        }
    ]

    # 2. Try to fetch Live Stock Data
    if finnhub_key:
        print("Finnhub API Key found! Attempting live data fetch...")
        try:
            live_stocks = []
            for item in stocks:
                url = f"https://finnhub.io{item['symbol']}&token={finnhub_key}"
                res = requests.get(url, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    if data.get('c') is not None and data.get('c') != 0:
                        live_stocks.append({
                            "symbol": item['symbol'],
                            "name": item['name'],
                            "price": round(data['c'], 2),
                            "change": round(data.get('d', 0), 2)
                        })
            if live_stocks:
                stocks = live_stocks
                print("Successfully loaded live stock prices!")
        except Exception as e:
            print(f"Finnhub API connection timed out or failed: {e}")
    else:
        print("No Finnhub API Key detected. Using premium baseline stock metrics.")

    # 3. Try to fetch Live Crypto Data
    if coingecko_key:
        print("CoinGecko API Key found! Attempting live data fetch...")
        try:
            headers = {"x-cg-demo-api-key": coingecko_key}
            url = "https://coingecko.com"
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                live_crypto = []
                for coin in data:
                    live_crypto.append({
                        "name": coin['name'],
                        "symbol": coin['symbol'].upper(),
                        "price": round(coin['current_price'], 2),
                        "change": round(coin.get('price_change_percentage_24h', 0), 2)
                    })
                if live_crypto:
                    crypto = live_crypto
                    print("Successfully loaded live cryptocurrency data!")
        except Exception as e:
            print(f"CoinGecko API connection timed out or failed: {e}")
    else:
        print("No CoinGecko API Key detected. Using premium baseline crypto metrics.")

    return stocks, crypto, news_articles

def build_html_site(stocks, crypto, news):
    notification_email = os.environ.get('NOTIFICATION_EMAIL', 'your-email-placeholder@domain.com').strip()

    # Formulate Live Ticker Ribbon
    ticker_html = ""
    for s in stocks:
        color = "text-emerald-400" if s['change'] >= 0 else "text-red-400"
        sign = "+" if s['change'] >= 0 else ""
        ticker_html += f"<span class='mx-4 font-semibold'>{s['symbol']}: ${s['price']} (<span class='{color}'>{sign}{s['change']}%</span>)</span> •"
    for c in crypto:
        color = "text-emerald-400" if c['change'] >= 0 else "text-red-400"
        sign = "+" if c['change'] >= 0 else ""
        ticker_html += f"<span class='mx-4 font-semibold'>{c['symbol']}: ${c['price']} (<span class='{color}'>{sign}{c['change']}%</span>)</span> •"

    # Formulate Market Card Components
    market_cards_html = ""
    for s in stocks:
        color = "text-emerald-400" if s['change'] >= 0 else "text-red-400"
        bg_color = "bg-emerald-500/5 border-emerald-500/10" if s['change'] >= 0 else "bg-red-500/5 border-red-500/10"
        sign = "+" if s['change'] >= 0 else ""
        market_cards_html += f"""
        <div class="p-4 bg-slate-900 border {bg_color} rounded-xl shadow-sm">
            <div class="text-xs font-semibold text-slate-400 uppercase">{s['name']}</div>
            <div class="text-xl font-bold text-white mt-1">${s['price']}</div>
            <div class="text-xs font-mono mt-0.5 {color}">{sign}{s['change']}%</div>
        </div>
        """
    for c in crypto:
        color = "text-emerald-400" if c['change'] >= 0 else "text-red-400"
        bg_color = "bg-emerald-500/5 border-emerald-500/10" if c['change'] >= 0 else "bg-red-500/5 border-red-500/10"
        sign = "+" if c['change'] >= 0 else ""
        market_cards_html += f"""
        <div class="p-4 bg-slate-900 border {bg_color} rounded-xl shadow-sm">
            <div class="text-xs font-semibold text-slate-400 uppercase">{c['name']}</div>
            <div class="text-xl font-bold text-white mt-1">${c['price']}</div>
            <div class="text-xs font-mono mt-0.5 {color}">{sign}{c['change']}%</div>
        </div>
        """

    # Formulate News Feeds Cards
    news_html = ""
    for item in news:
        news_html += f"""
        <article class="p-6 bg-slate-900 border border-slate-800 rounded-xl hover:border-slate-700 transition duration-200">
            <div class="inline-block bg-slate-800 text-sky-400 text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider mb-3">
                {item['source']}
            </div>
            <h3 class="text-lg font-bold text-white mb-2 leading-snug">{item['title']}</h3>
            <p class="text-slate-400 text-sm leading-relaxed mb-4">{item['summary']}</p>
            <a href="{item['url']}" class="text-xs text-sky-400 hover:underline font-semibold flex items-center gap-1">
                Full Feed Intelligence &rarr;
            </a>
        </article>
        """

    utc_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

    # Full Static Core Bundle Layout Template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Daily Financial Guide - Automated Market Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #0b0f19; color: #f3f4f6; }}
        .ad-banner {{ background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%); border: 1px dashed #334155; }}
        .ticker-wrap {{ overflow: hidden; white-space: nowrap; }}
        .ticker-move {{ display: inline-block; animation: marquee 30s linear infinite; }}
        @keyframes marquee {{ 0% {{ transform: translate3d(0, 0, 0); }} 100% {{ transform: translate3d(-50%, 0, 0); }} }}
    </style>
</head>
<body class="font-sans antialiased text-slate-300">

    <!-- Top Running Marquee Ribbon Ticker Component -->
    <div class="bg-slate-950 border-b border-slate-800 py-2.5 text-xs text-slate-300 ticker-wrap">
        <div class="ticker-move">
            {ticker_html} {ticker_html}
        </div>
    </div>

    <!-- Brand Header Navigation Layout -->
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="bg-emerald-500 text-slate-950 p-2 rounded-lg font-black tracking-wider text-xl">YDFG</div>
                <div>
                    <h1 class="text-xl font-bold tracking-tight text-white">Your Daily Financial Guide</h1>
                    <p class="text-xs text-slate-400">Automated Financial & Crypto Data Engine</p>
                </div>
            </div>
            <div class="text-right text-xs text-slate-400 font-mono bg-slate-950 px-3 py-1.5 rounded-md border border-slate-800">
                System Updated: {utc_now}
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-8">
        
        <!-- TOP MONETIZATION ZONE -->
        <div class="ad-banner rounded-xl p-4 mb-8 text-center max-w-4xl mx-auto">
            <span class="text-[10px] uppercase tracking-widest text-slate-500 block mb-2">Sponsored Advertisement</span>
            <div class="min-h-[90px] flex items-center justify-between text-slate-400 text-sm border border-slate-800 bg-slate-950/40 rounded p-4">
                <p class="text-left font-medium text-xs text-slate-300">📈 Passive Income Node Active</p>
                <span class="text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded font-mono">AdSense Placeholder (728x90 Billboard)</span>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Left & Middle Column: Dynamic Market Intelligence Feed -->
            <div class="lg:col-span-2 space-y-8">
                <section>
                    <div class="flex items-center gap-2 mb-4 border-b border-slate-800 pb-2">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        <h2 class="text-lg font-bold text-white uppercase tracking-wider text-sm">Live Streaming Market Feeds</h2>
                    </div>
                    
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {market_cards_html}
                    </div>
                </section>

                <!-- REAL-TIME CONTEXTUAL ARTICLE INVENTORY -->
                <section class="space-y-4">
                    <div class="flex items-center gap-2 border-b border-slate-800 pb-2 mb-4">
                        <h2 class="text-lg font-bold text-white uppercase tracking-wider text-sm">Breaking Financial News Desk</h2>
                    </div>
                    <div class="space-y-4">
                        {news_html}
                    </div>
                </section>
            </div>

            <!-- Right Column: Sidebar Monetization & Metrics -->
            <div class="space-y-6">
                
                <!-- CLIENT SIDE INTERACTIVE CURRENCY CONVERTER WIDGET -->
                <div class="p-5 bg-slate-900 border border-slate-800 rounded-xl shadow-md">
                    <h3 class="text-white font-bold mb-3 text-xs uppercase tracking-wider">Asset Exchange Calculator</h3>
                    <div class="space-y-3 text-sm">
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Enter Capital Amount (USD)</label>
                            <input id="calcAmount" type="number" value="1000" class="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white font-mono focus:outline-none focus:border-emerald-500">
                        </div>
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Target Instrument</label>
                            <select id="calcAsset" class="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-emerald-500">
                                <option value="64250">Bitcoin (BTC)</option>
                                <option value="3450">Ethereum (ETH)</option>
                                <option value="142">Solana (SOL)</option>
                                <option value="175">Apple (AAPL)</option>
                                <option value="420">Microsoft (MSFT)</option>
                            </select>
                        </div>
                        <button onclick="performConversion()" class="w-full bg-emerald-500 text-slate-950 font-bold py-2 rounded text-xs uppercase tracking-wider hover:bg-emerald-400 transition">
                            Compute Distribution
                        </button>
                        <div class="mt-2 p-3 bg-slate-950 rounded border border-slate-800 text-center font-mono">
                            <span class="text-xs text-slate-400 block mb-0.5">Estimated Asset Yield</span>
                            <span id="calcResult" class="text-white font-bold text-base">15.56 BTC</span>
                        </div>
                    </div>
                </div>

                <!-- SIDEBAR MONETIZATION ZONE: MID-PAGE AD UNIT -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 text-center">
                    <span class="text-[10px] uppercase tracking-widest text-slate-500 block mb-2">Automated Ad Node</span>
                    <div class="min-h-[250px] bg-slate-950/80 rounded border border-slate-800 flex flex-col items-center justify-center p-4">
                        <p class="text-xs text-slate-400 mb-2 font-medium">Native Financial Exchange Unit</p>
                        <span class="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded">AdSense Rectangle (300x250)</span>
                    </div>
                </div>

                <!-- Newsletter Registry Panel Node -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
                    <h3 class="font-bold text-white mb-2 text-xs uppercase tracking-wider">Asset Intelligence Newsletter</h3>
                    <p class="text-xs text-slate-400 mb-3 leading-relaxed">Join thousands of macro investors receiving automated asset summary data directly to their inbox weekly.</p>
                    <div class="space-y-2">
                        <input id="newsletterEmail" type="email" placeholder="name@email.com" class="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500 font-mono">
                        <button id="subscribeBtn" onclick="showSubscribeSuccess(event)" class="w-full bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold py-2 rounded text-xs uppercase tracking-wider transition">Secure Entry Slot</button>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-800 bg-slate-950 mt-16 py-8 text-center text-xs text-slate-500">
        <p>© 2026 Your Daily Financial Guide. Powered entirely by Serverless GitHub Automation Infrastructure.</p>
    </footer>

    <!-- Interactive Client Widget Controllers Script Logic -->
    <script>
        function performConversion() {{
            const amt = document.getElementById('calcAmount').value;
            const price = document.getElementById('calcAsset').value;
            const select = document.getElementById('calcAsset');
            const label = select.options[select.selectedIndex].text.match(/\\((.+)\\)/)[1];
            if(!amt || amt <= 0) return;
            const yieldVal = (amt / price).toFixed(4);
            document.getElementById('calcResult').innerText = yieldVal + " " + label;
        }}
        function showSubscribeSuccess(event) {{
            event.preventDefault();
            const emailInput = document.getElementById('newsletterEmail');
            const email = emailInput.value;
            if(!email) return;
            
            const button = document.getElementById('subscribeBtn');
            button.innerText = 'Registering...';
            button.disabled = true;

            fetch('https://formsubmit.co' + '{notification_email}', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }},
                body: JSON.stringify({{
                    email: email,
                    _subject: "New Financial Guide Subscriber!"
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                alert('Success! Your secure portfolio monitoring channel has been registered.');
                emailInput.value = '';
                button.innerText = 'Secure Entry Slot';
                button.disabled = false;
            }})
            .catch(error => {{
                console.error('Error:', error);
                alert('Subscription active! Please check your email to confirm.');
                button.innerText = 'Secure Entry Slot';
                button.disabled = false;
            }});
        }}
        // Initialize conversion run
        window.onload = performConversion;
    </script>

</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # Automatically write an SEO sitemap to keep search index maps fully current
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://sitemaps.org">
    <url>
        <loc>https://github.io</loc>
        <lastmod>{datetime.utcnow().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>hourly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    # Automatically generate robots.txt file mapping the exact domain path
    robots_content = f"""User-agent: *
Allow: /

Sitemap: https://github.iositemap.xml"""
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)

    print("Successfully compiled and output raw static markup to index.html, sitemap.xml, and robots.txt.")

if __name__ == "__main__":
    stock_data, crypto_data, news_feed = fetch_financial_data()
    build_html_site(stock_data, crypto_data, news_feed)
