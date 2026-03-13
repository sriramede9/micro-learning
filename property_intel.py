import os, json, requests, time
from datetime import datetime

# --- CONFIG ---
PROGRESS_FILE = 'property_progress.json'
PILLARS = [
    "LRT & Infrastructure Growth (Hazel McCallion/Dundas BRT)",
    "Zoning & Intensification (Garden Suites/R3/ARUs)",
    "Financial Optimization (Smith Maneuver/Equity Leverage)",
    "Local Micro-Market (Lolita Gardens/Mississauga Valleys Sales)",
    "Tenant & Cash Flow Strategy (Basement/Garden Suite yields)"
]

def get_live_models(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        return [m['name'] for m in response.json().get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
    except: return []

def call_gemini(api_key, model_name, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
    return response.json()

# 1. State Management
if not os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'w') as f: json.dump({"day": 1, "idx": 0}, f)
with open(PROGRESS_FILE, 'r') as f: state = json.load(f)

current_pillar = PILLARS[state['idx']]

# 2. The Asset Prompt
prompt = f"""
Act as a Real Estate Investment Strategist for 384 Lolita Gardens, Mississauga.
Today's Focus: {current_pillar}.

Property Context:
- Lot: 46.7 x 121.78 ft | Zoning: R3 | Detached 2-Storey (4+2 Bed, 4 Bath).
- Proximity: Hazel McCallion LRT, Dundas BRT, Cooksville GO, Mississauga Valley CC.

Provide:
1. THE CATALYST: How today's topic specifically impacts the property's appraisal or equity.
2. WEALTH MOVE: A specific action (e.g., Garden Suite feasibility, Smith Maneuver steps, or Permit applications).
3. MARKET INTEL: What an owner in Mississauga Valleys should look for this week.
4. "BULLETPROOF" FACTOR: One risk-mitigation strategy to ensure the asset survives a market shift.
"""

# 3. Execution (Your Round Robin Logic)
api_key = os.getenv("GEMINI_API_KEY")
targets = ['models/gemini-3-flash-preview', 'models/gemini-2.5-flash', 'models/gemini-2.0-flash']
available = get_live_models(api_key)
ordered = [m for m in targets if m in available] or available[:3]

intel = None
for model in ordered:
    data = call_gemini(api_key, model, prompt)
    if 'candidates' in data:
        intel = data['candidates'][0]['content']['parts'][0]['text']
        break

if intel:
    # Save as a separate HTML file for your Asset Feed
    with open('docs/property.html', 'a') as f:
        f.write(f"<div class='card'><h2>Day {state['day']}: {current_pillar}</h2>{intel}</div>")
    
    state['day'] += 1
    state['idx'] = (state['idx'] + 1) % len(PILLARS)
    with open(PROGRESS_FILE, 'w') as f: json.dump(state, f)
