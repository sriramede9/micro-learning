import os
import requests
import json
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
# Note: Keeping your aggressive, high-level persona.
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
data = call_gemini(api_key, 'models/gemini-1.5-flash', prompt) # Updated to latest stable model name

if 'candidates' in data:
    intel = data['candidates'][0]['content']['parts'][0]['text']

    # Simple Markdown Navigation
    nav = "[💼 CAREER](index.md) | **[🏠 ASSET TRACKER](property.md)**\n\n---\n"

    # Constructing the Final MD Report
    md_content = f"""{nav}
# 384 Lolita: 2026 Equity Masterplan

**Refreshed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{intel}

---
*Confidential Investment Intelligence — Generated via Gemini Flash 2026*
"""

    # Save as Markdown
    with open('reports/property.md', 'w') as f:
        f.write(md_content)

    print("Intelligence Report generated: docs/property.md")
else:
    print("Error: Could not retrieve AI intelligence. Check API Key.")