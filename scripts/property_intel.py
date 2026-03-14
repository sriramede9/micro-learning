import os
import requests
import json
import time
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

# --- HELPER FUNCTIONS ---
def get_live_models(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url, timeout=10)
        return [m['name'] for m in response.json().get('models', [])
                if 'generateContent' in m.get('supportedGenerationMethods', [])]
    except:
        return []

def call_gemini(api_key, model_name, prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt_text}]}]}, timeout=45)
        return response.json()
    except Exception as e:
        return {"error": {"message": str(e)}}

# --- MAIN EXECUTION ---
MODEL_PRIORITY = ['models/gemini-2.0-flash', 'models/gemini-1.5-flash', 'models/gemini-1.5-pro']
api_key = os.getenv("GEMINI_API_KEY")
available = get_live_models(api_key)
ordered_targets = [m for m in MODEL_PRIORITY if m in available] or available[:3]

intel = None
successful_model = None

# NEW: Double-layer loop (Models x Retries)
for model in ordered_targets:
    if intel: break 
    
    print(f"🤖 Target Model: {model}")
    
    for attempt in range(3):  # 3 attempts per model
        data = call_gemini(api_key, model, prompt)
        
        if 'candidates' in data and data['candidates']:
            intel = data['candidates'][0]['content']['parts'][0]['text']
            successful_model = model
            print(f"✅ Success on attempt {attempt + 1}!")
            break
        
        error = data.get('error', {})
        if error.get('code') == 429:
            # Exponential backoff: 30s, 60s, 90s
            wait_time = (attempt + 1) * 30 
            print(f"⏳ TPM/RPM Limit hit. Backing off for {wait_time}s...")
            time.sleep(wait_time)
        else:
            print(f"⚠️ {model} failed: {error.get('message', 'Unknown Error')}")
            break # If it's not a rate limit, don't waste time retrying this model

if intel:
    nav = "[💼 CAREER](index.md) | **[🏠 ASSET TRACKER](property.md)**\n\n---\n"
    md_content = f"{nav}\n# 384 Lolita: 2026 Equity Masterplan\n\n**Refreshed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{intel}\n\n---\n*Confidential Investment Intelligence — Generated via {successful_model}*"
    
    os.makedirs('reports', exist_ok=True)
    with open('reports/property.md', 'w') as f:
        f.write(md_content)
    print("✅ Intelligence Report generated: reports/property.md")
else:
    print("🚨 All models and retries exhausted.")
    exit(1)
