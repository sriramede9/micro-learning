import os, requests
from datetime import datetime

# --- THE BLUEPRINT: 384 LOLITA GARDENS ASSETS ---
ASSET_LIST = [
    "Hazel McCallion LRT (18km line, 19 stops, 2026/27 rollout)",
    "Dundas BRT (Key link for Kipling/Hamilton connectivity)",
    "T&T Supermarket (High-density retail anchor)",
    "Peter Gilgan Hospital (Canada's largest hospital, 950+ beds, 2,800+ staff)",
    "TOC and Loop (Downtown Square One extension)",
    "Cooksville GO Station (Major regional mobility hub)",
    "Mississauga Valley CC & Library (Renovation completion 2027)",
    "600-620 Lolita Gardens (25-storey tower intensification next door)",
    "Cooksville & Iggy Kaneff Park (Public realm upgrades)",
    "Fire Station 124 (Critical infrastructure/Safety)",
    "Mary Fix Creek (Environmental/Flood resilience)",
    "20 mins to Pearson Airport (Global logistic proximity)",
    "Princess Royal Drive (Urban core link)",
    "Garden Suite Updates (100% DC Waiver through Dec 2027)",
    "Panchavati & Cedarbrae Park (Green space value)",
    "Highway 403/QEW Proximity (Regional logistics link)"
]

def call_gemini(api_key, model_name, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
    return response.json()

# --- THE "RICH BITCH" PROMPT ---
prompt = f"""
Act as a Senior Investment Strategist and Real Estate Architect.
Current Date: March 13, 2026.
Target Property: 384 Lolita Gardens (Detached R3, 46.7x121ft lot).

1. CORE REVIEW: Analyze the equity multiplier for these assets: {", ".join(ASSET_LIST)}.
2. HORIZON SCAN: Identify 3 NEW catalysts for 2026 (e.g., specific Mississauga 'Missing Middle' grants, TOC pre-zoning in Cooksville, or hospital staff rental demand).
3. STRATEGIC QUESTIONS: Generate 3 'Million-Dollar Questions' for a city planner or private lender to unlock land value.
4. WEALTH MOVE: Detail the 'Smith Maneuver' potential given current 2026 Bank of Canada rates (2.25%) and the 121ft lot depth.

Style: Aggressive, Insightful, Senior Developer level. Use Markdown tables and bold headers.
"""

api_key = os.getenv("GEMINI_API_KEY")
data = call_gemini(api_key, 'models/gemini-3-flash-preview', prompt)

if 'candidates' in data:
    intel = data['candidates'][0]['content']['parts'][0]['text']
    nav = """<nav style="margin-bottom:20px; padding:15px; background:#1a1a1a; color:white; display:flex; gap:20px;">
                <a href="index.html" style="color:#00d4ff; text-decoration:none;">💼 CAREER</a>
                <a href="property.html" style="color:#00d4ff; text-decoration:none; font-weight:bold;">🏠 ASSET TRACKER</a>
             </nav>"""
    
    with open('docs/property.html', 'w') as f:
        f.write(f"<html><head><style>body{{font-family:'Segoe UI',sans-serif;max-width:1000px;margin:auto;padding:20px;background:#f0f2f5;}} .card{{background:white;padding:40px;border-radius:15px;box-shadow:0 10px 25px rgba(0,0,0,0.1);line-height:1.6;}} h1{{color:#1a1a1a;border-bottom:4px solid #00d4ff;display:inline-block;}} table{{width:100%;border-collapse:collapse;margin:20px 0;}} th,td{{padding:12px;border:1px solid #ddd;text-align:left;}} th{{background:#f8f9fa;}}</style></head><body>{nav}")
        f.write(f"<div class='card'><h1>384 Lolita: 2026 Equity Masterplan</h1><p><strong>Refreshed:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>{intel}</div></body></html>")
