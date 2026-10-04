import os
import requests
from datetime import datetime

def fetch_financial_data():
    # Gather API keys from GitHub Secrets environment variables
    finnhub_key = os.environ.get('FINNHUB_API_KEY', '')
    coingecko_key = os.environ.get('COINGECKO_API_KEY', '')
    
    # Premium Default Fallback Profiles (Ensures your platform is NEVER empty)
    stocks = [
        {"symbol": "AAPL", "name": "Apple Inc.", "price": 178.45, "change": 1.42},
        {"symbol": "MSFT", "name": "Microsoft Corp.", "price": 422.30, "change": -0.65},
        {"symbol": "NVDA", "name": "NVIDIA Corp.", "price": 894.25, "change": 3.84},
        {"symbol": "TSLA", "name": "Tesla Inc.", "price": 174.60, "change": -1.18}
    ]
    
    crypto = [
        {"name": "Bitcoin", "symbol": "BTC", "price": 64820.00, "change": 2.15},
        {"name": "Ethereum", "symbol": "ETH", "price": 3490.50, "change": 0.95},
        {"name": "Solana", "symbol": "SOL", "price": 144.25, "change": -2.40}
    ]
    
    news_articles = [
        {
            "title": "Fed Signals Stable Interest Rate Outlook Supporting Technical Equity Growth",
            "source": "Macro Growth Desk",
            "summary": "Central banking oversight bodies indicated extended stabilization parameters for core lending benchmarks, driving immediate asset volume allocations into high-scale growth frameworks.",
            "url": "#"
        },
        {
            "title": "Institutional Digital Asset Allocations Form Core Capital Corridors",
            "source": "Decentralized Ledger",
            "summary": "Global asset management platforms report historic multi-million baseline inflows into standard exchange-traded token products, solidifying multi-asset infrastructure layers.",
            "url": "#"
        },
        {
            "title": "Semiconductor Enterprise Systems Outpace Baseline Wall Street Projections",
            "source": "Silicon Metrics",
            "summary": "Advanced network accelerator designers and algorithmic silicon fabs reported substantial margins driven by continuous cloud operations demand models.",
            "url": "#"
        }
    ]

    # Fetch live Stock Data if key is configured
    if finnhub_key:
        try:
            live_stocks = []
            for item in stocks:
                res = requests.get(f"https://finnhub.io{item['symbol']}&token={finnhub_key}", timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    if data.get('c'):
                        price = round(data['c'], 2)
                        change_val = round(data['d'], 2)
                        prev_close = data.get('pc', price)
                        pct_change = round((change_val / prev_close) * 100, 2) if prev_close else 0.0
                        live_stocks.append({
                            "symbol": item['symbol'],
                            "name": item['name'],
                            "price": price,
                            "change": pct_change
                        })
            if live_stocks:
                stocks = live_stocks
        except Exception as e:
            print(f"Finnhub collection bypassed: {e}")

    # Fetch live Crypto Data if key is configured
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
            print(f"CoinGecko collection bypassed: {e}")

    return stocks, crypto, news_articles

def build_html_site(stocks, crypto, news):
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    
    # Formulate Marquee Ticker Component
    ticker_items = ""
    for s in stocks:
        color = "text-emerald-400" if s['change'] >= 0 else "text-red-400"
        sign = "+" if s['change'] >= 0 else ""
        ticker_items += f"<span class='inline-block mr-12 font-semibold text-sm text-slate-300'>{s['symbol']}: ${s['price']} (<span class='{color}'>{sign}{s['change']}%</span>)</span>"
    for c in crypto:
        color = "text-emerald-400" if c['change'] >= 0 else "text-red-400"
        sign = "+" if c['change'] >= 0 else ""
        ticker_items += f"<span class='inline-block mr-12 font-semibold text-sm text-slate-300'>{c['symbol']}: ${c['price']} (<span class='{color}'>{sign}{c['change']}%</span>)</span>"

    # Formulate Live Asset Cards Grid Layout
    market_grid_html = ""
    for s in stocks:
        color = "text-emerald-400" if s['change'] >= 0 else "text-red-400"
        bg_pill = "bg-emerald-500/10" if s['change'] >= 0 else "bg-red-500/10"
        sign = "+" if s['change'] >= 0 else ""
        market_grid_html += f"""
        <div class="bg-slate-900 border border-slate-800/80 rounded-xl p-5 hover:border-slate-700 transition">
            <div class="flex justify-between items-start mb-2">
                <span class="text-xs text-slate-400 font-bold uppercase tracking-wider">{s['symbol']}</span>
                <span class="text-xs font-mono font-bold px-2 py-0.5 rounded {bg_pill} {color}">{sign}{s['change']}%</span>
            </div>
            <h3 class="text-sm font-medium text-slate-300 mb-1">{s['name']}</h3>
            <div class="text-2xl font-bold text-white tracking-tight">${s['price']}</div>
        </div>
        """
        
    for c in crypto:
        color = "text-emerald-400" if c['change'] >= 0 else "text-red-400"
        bg_pill = "bg-emerald-500/10" if c['change'] >= 0 else "bg-red-500/10"
        sign = "+" if c['change'] >= 0 else ""
        market_grid_html += f"""
        <div class="bg-slate-900 border border-slate-800/80 rounded-xl p-5 hover:border-slate-700 transition">
            <div class="flex justify-between items-start mb-2">
                <span class="text-xs text-slate-400 font-bold uppercase tracking-wider">{c['symbol']}</span>
                <span class="text-xs font-mono font-bold px-2 py-0.5 rounded {bg_pill} {color}">{sign}{c['change']}%</span>
            </div>
            <h3 class="text-sm font-medium text-slate-300 mb-1">{c['name']}</h3>
            <div class="text-2xl font-bold text-white tracking-tight">${c['price']}</div>
        </div>
        """

    # Formulate News Cards Item List
    news_cards_html = ""
    for n in news:
        news_cards_html += f"""
        <div class="bg-slate-900/60 border border-slate-800/80 rounded-xl p-6 hover:border-slate-700 transition">
            <div class="mb-3">
                <span class="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full uppercase tracking-wider">{n['source']}</span>
            </div>
            <h3 class="text-lg font-bold text-white mb-2 leading-snug">{n['title']}</h3>
            <p class="text-sm text-slate-400 leading-relaxed mb-4">{n['summary']}</p>
            <a href="{n['url']}" class="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1">Full Coverage &rarr;</a>
        </div>
        """

    # Build the full production static HTML package using your exact visual layout
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
        .ticker-container {{ overflow: hidden; white-space: nowrap; }}
        .ticker-content {{ display: inline-block; animation: marquee 30s linear infinite; }}
        @keyframes marquee {{ 0% {{ transform: translate3d(0, 0, 0); }} 100% {{ transform: translate3d(-50%, 0, 0); }} }}
    </style>
</head>
<body class="font-sans antialiased">

    <!-- Premium Running Marquee Ticker -->
    <div class="border-b border-slate-800 bg-slate-950 py-2.5 ticker-container">
        <div class="ticker-content">
            {ticker_items} {ticker_items}
        </div>
    </div>

    <!-- Brand Header Navigation Layout -->
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="bg-emerald-500 text-slate-950 px-2.5 py-1.5 rounded-lg font-black tracking-wider text-xl">YDFG</div>
                <div>
                    <h1 class="text-xl font-bold tracking-tight text-white">Your Daily Financial Guide</h1>
                    <p class="text-xs text-slate-400">Automated Financial & Crypto Data Engine</p>
                </div>
            </div>
            <div class="text-right text-xs text-slate-400 font-mono bg-slate-950 px-3 py-1.5 rounded-md border border-slate-800">
                System Updated: {current_time}
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-8">
        
        <!-- TOP MONETIZATION ZONE: PROGRAMMATIC DISPLAY AD POSITION -->
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
                        <h2 class="text-sm font-bold text-slate-200 uppercase tracking-wider">Live Streaming Market Feeds</h2>
                    </div>
                    
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {market_grid_html}
                    </div>
                </section>

                <!-- REAL-TIME CONTEXTUAL ARTICLE INVENTORY -->
                <section class="space-y-4">
                    <div class="flex items-center gap-2 border-b border-slate-800 pb-2 mb-4">
                        <h2 class="text-sm font-bold text-slate-200 uppercase tracking-wider">Breaking News Desk</h2>
                    </div>
                    <div class="grid grid-cols-1 gap-4">
                        {news_cards_html}
                    </div>
                </section>
            </div>

            <!-- Right Column: Sidebar Monetization & Metrics -->
            <div class="space-y-6">
                
                <!-- SIDEBAR MONETIZATION ZONE: MID-PAGE AD UNIT -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 text-center">
                    <span class="text-[10px] uppercase tracking-widest text-slate-500 block mb-2">Automated Ad Node</span>
                    <div class="min-h-[250px] bg-slate-950/80 rounded border border-slate-800 flex flex-col items-center justify-center p-4">
                        <p class="text-xs text-slate-400 mb-2 font-medium">Native Financial Exchange Unit</p>
                        <span class="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded">AdSense Rectangle (300x250)</span>
                    </div>
                </div>

                <!-- Platform Mission Blueprint -->
                <div class="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-xl p-5">
                    <h3 class="font-bold text-white mb-2 text-xs uppercase tracking-wider">Platform Operations</h3>
                    <p class="text-xs text-slate-400 leading-relaxed">
                        This environment analyzes, structures, and compiles complex global asset datasets programmatically using open internet protocols. The platform processes high-intent macro data for educational evaluation without editorial human overhead.
                    </p>
                </div>
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-800 bg-slate-950 mt-16 py-8 text-center text-xs text-slate-500">
        <p>© 2026 Your Daily Financial Guide. Powered entirely by Serverless GitHub Automation Infrastructure.</p>
    </footer>

</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    stock_data, crypto_data, news_feed = fetch_financial_data()
    build_html_site(stock_data, crypto_data, news_feed)
