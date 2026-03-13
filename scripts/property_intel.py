import os
import requests
import json
from datetime import datetime

# --- ASSETS & PROMPT CONFIG ---
ASSET_LIST = [
    "Hazel McCallion LRT (2026/27 rollout)",
    "Peter Gilgan Hospital (Canada's largest hospital)",
    "600-620 Lolita Gardens (25-storey tower intensification)",
    "Garden Suite Updates (100% DC Waiver through Dec 2027)",
    "20 mins to Pearson Airport"
]

prompt = f"""
Act as a Senior Investment Strategist.
Target Property: 384 Lolita Gardens (Detached R3, 46.7x121ft lot).
1. Analyze equity multipliers for: {", ".join(ASSET_LIST)}.
2. Identify 3 NEW catalysts for 2026.
3. Detail 'Smith Maneuver' potential with 2026 rates (2.25%).
Style: Aggressive, Insightful. Use Markdown tables and bold headers.
"""

# --- MODEL CONFIG ---
MODEL_PRIORITY = [
    'models/gemini-2.0-flash-exp',
    'models/gemini-2.0-flash',
    'models/gemini-1.5-flash',
    'models/gemini-1.5-pro'
]

def get_best_model(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url, timeout=10).json()
        models = [m['name'] for m in response.get('models', [])
                  if 'generateContent' in m.get('supportedGenerationMethods', [])]
        for target in MODEL_PRIORITY:
            if target in models:
                return target
        return models[0] if models else None
    except Exception as e:
        print(f"⚠️ Model fetch failed, using fallback: {e}")
        return 'models/gemini-1.5-flash'

def call_gemini(api_key, model_name, prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    response = requests.post(url, json={"contents": [{"parts": [{"text": prompt_text}]}]}, timeout=30)
    return response.json()

# --- EXECUTION ---
api_key = os.getenv("GEMINI_API_KEY")
selected_model = get_best_model(api_key)

print(f"🤖 Using model: {selected_model}")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in environment.")
    exit(1)

try:
    data = call_gemini(api_key, selected_model, prompt)
except Exception as e:
    print(f"❌ Network/Request Error: {e}")
    data = {}

# Check for valid response candidates
if 'candidates' in data and len(data['candidates']) > 0:
    intel = data['candidates'][0]['content']['parts'][0]['text']

    nav = "[💼 CAREER](index.md) | **[🏠 ASSET TRACKER](property.md)**\n\n---\n"

    md_content = f"""{nav}
# 384 Lolita: 2026 Equity Masterplan

**Refreshed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{intel}

---
*Confidential Investment Intelligence — Generated via Gemini 2026*
"""

    # Save to reports directory (build_dashboard.py looks here)
    os.makedirs('reports', exist_ok=True)
    with open('reports/property.md', 'w') as f:
        f.write(md_content)

    print("✅ Intelligence Report generated: reports/property.md")

else:
    print(f"🚨 API Failure or empty response: {json.dumps(data, indent=2)}")
    exit(1)