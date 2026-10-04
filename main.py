import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Targeted top financial and crypto RSS feeds (100% Free, no custom API keys required)
FEEDS = {
    "Stocks & Economy News": "https://yahoo.com",
    "Crypto Currency Market": "https://coindesk.com"
}

def fetch_news(feed_name, url):
    """Fetches raw headlines from free RSS endpoints safely with user-agent masks."""
    print(f"Initializing connection to: {feed_name}...")
    news_items = []
    try:
        # User-agent header prevents servers from blocking script requests
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) FrameworkEngine/1.0'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Skipping {feed_name}: Received unexpected server status code {response.status_code}")
            return news_items
            
        # Parse XML structure natively without external parser packages
        root = ET.fromstring(response.content)
        for item in root.findall('.//item')[:6]:  # Curate top 6 breaking stories per market sector
            title = item.find('title').text if item.find('title') is not None else "Breaking Market Update"
            link = item.find('link').text if item.find('link') is not None else "#"
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            
            # Truncate timestamps for clean dashboard presentation grid layouts
            if pub_date:
                try:
                    pub_date = pub_date.split(' +')[0].split(' GMT')[0]
                except Exception:
                    pass
                    
            news_items.append({
                "title": title,
                "link": link,
                "date": pub_date
            })
    except Exception as error_context:
        print(f"Could not extract node elements for {feed_name}: {error_context}")
    return news_items

def generate_html(all_news):
    """Compiles curated aggregate headlines into a premium, responsive dark-mode dashboard."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Fully responsive architecture optimized using premium Tailwind CSS configurations
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlphaPulse | Automated Market Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #0b0f19; color: #f3f4f6; }}
    </style>
</head>
<body class="font-sans antialiased min-h-screen flex flex-col justify-between">

    <!-- Top Navigation Framework -->
    <header class="border-b border-gray-800 bg-gray-900/50 backdrop-blur sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <span class="text-2xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">AlphaPulse</span>
                <span class="text-[10px] bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded-full font-mono border border-emerald-500/20 tracking-wider font-bold">AUTOMATED ENGINE</span>
            </div>
            <div class="text-xs text-gray-400 font-mono hidden sm:block">
                System Sync: {current_time}
            </div>
        </div>
    </header>

    <!-- Main Content Stream -->
    <main class="flex-grow max-w-6xl w-full mx-auto px-4 py-8">
        
        <!-- Premium Native Non-Intrusive Monetization Segment Placeholder -->
        <div class="mb-8 p-4 bg-gradient-to-r from-gray-900 to-gray-800 rounded-xl border border-gray-800 text-center">
            <span class="text-[9px] uppercase tracking-widest text-gray-500 block mb-1 font-bold">Market Sponsor Context</span>
            <div class="text-xs text-gray-400 italic">
                [Monetization Optimization Slot: Future programmatic contextual ad code or premium financial product banner placement]
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
"""
    
    for category, items in all_news.items():
        html_content += f"""
            <!-- Market Category Block -->
            <section class="space-y-4">
                <div class="flex items-center space-x-2 pb-2 border-b border-gray-800">
                    <h2 class="text-md font-bold text-gray-100 uppercase tracking-wide">{category}</h2>
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                </div>
                <div class="space-y-3">
"""
        if not items:
            html_content += """
                    <div class="p-4 bg-gray-900/30 rounded-lg text-xs text-gray-500 italic border border-gray-800/40">
                        Queue empty. Fetch mechanism retry executing automatically during upcoming cloud cycle.
                    </div>
            """
        else:
            for item in items:
                html_content += f"""
                    <a href="{item['link']}" target="_blank" rel="noopener noreferrer" class="block p-4 bg-gray-900/40 hover:bg-gray-900/80 border border-gray-800/60 hover:border-gray-700/80 rounded-xl transition duration-150 group">
                        <h3 class="text-sm font-medium text-gray-200 group-hover:text-emerald-400 transition-colors line-clamp-2 leading-relaxed">{item['title']}</h3>
                        <span class="text-[11px] text-gray-500 font-mono mt-2 block">{item['date']}</span>
                    </a>
                """
        html_content += """
                </div>
            </section>
        """
        
    html_content += """
        </div>

        <!-- Monetization Widget Block 2 (Audience Newsletter Funnel Setup) -->
        <div class="mt-12 p-6 bg-gradient-to-b from-gray-900/40 to-gray-950/20 rounded-2xl border border-gray-800 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div>
                <h3 class="text-sm font-bold text-gray-200">System Premium Aggregate Channel</h3>
                <p class="text-xs text-gray-400 mt-0.5">High-impact serverless data arrays synthesized every four hours without structural server load overhead.</p>
            </div>
            <div class="w-full sm:w-auto text-xs bg-gray-900 px-4 py-2.5 rounded-lg border border-gray-800 text-center font-medium text-gray-400 select-none">
                [Future Automated Revenue Stream Slot]
            </div>
        </div>
    </main>

    <!-- Structural Base Matrix -->
    <footer class="border-t border-gray-800 bg-gray-950 py-6 mt-16 text-center text-[11px] text-gray-500 font-mono">
        <p>Operational Status: Nominal | Managed Serverless Cloud Framework via GitHub Actions Engine</p>
    </footer>

</body>
</html>
"""
    # Write output matrix file securely into repository root structure
    with open("index.html", "w", encoding="utf-8") as file_stream:
        file_stream.write(html_content)
    print("Process Complete: Single static news system architecture refreshed successfully.")

if __name__ == "__main__":
    aggregated_market_data = {}
    for feed_title, feed_endpoint in FEEDS.items():
        aggregated_market_data[feed_title] = fetch_news(feed_title, feed_endpoint)
    generate_html(aggregated_market_data)
