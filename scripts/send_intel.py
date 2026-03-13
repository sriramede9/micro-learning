import os
import json
import requests
import time
import markdown
from datetime import datetime

# --- HELPER FUNCTIONS ---

def get_live_models(api_key):
    """Fetch all models that support generating content."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        models_data = response.json()
        return [
            m['name'] for m in models_data.get('models', [])
            if 'generateContent' in m.get('supportedGenerationMethods', [])
        ]
    except Exception as e:
        print(f"⚠️ Failed to fetch models: {e}")
        return []

def call_gemini(api_key, model_name, prompt):
    """Attempt a single API call."""
    # model_name already contains 'models/', so we just append the method
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": {"message": str(e)}}

# --- MAIN LOGIC ---

# 1. Load Progress
PROGRESS_FILE = 'progress.json'
if not os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({"day": 1, "level": "Senior", "pillar_idx": 0}, f)

with open(PROGRESS_FILE, 'r') as f:
    state = json.load(f)

PILLARS = [
    "Modern Java (17-26) & Performance", 
    "GCP & AWS Cloud Native Architecture",
    "Distributed Systems & Payment Reliability",
    "Spring AI & Enterprise RAG",
    "MongoDB & High-Scale Persistence"
]
current_pillar = PILLARS[state['pillar_idx']]

# 2. Architect Prompt
prompt = f"""
Act as a Principal Engineer. Day {state['day']} topic: {current_pillar}.
Target: Java 17 to 26 (Virtual threads, Pattern matching, etc.).

Format:
- SIMPSONS ANALOGY: A witty scenario explaining the tech.
- BIG PICTURE: Problem/Solution and the 'Butterfly Effect' on a banking app.
- CODE: Java 21+ Spring Boot snippet.
- FOOD FOR THOUGHT: Explain a feature in (Uber/Amazon/Google Maps) using:
    - Java/Spring Boot (Logic)
    - MongoDB (Data)
    - Spring AI (Intelligence)
    - GCP/AWS (Scaling)
"""

# 3. Model Preference (High to Low)
MODEL_PRIORITY = [
    'models/gemini-3-flash-preview', 
    'models/gemini-2.5-flash', 
    'models/gemini-2.0-flash'
]

api_key = os.getenv("GEMINI_API_KEY")
available = get_live_models(api_key)

# Filter priority models; fallback to first 3 available if none match
ordered_targets = [m for m in MODEL_PRIORITY if m in available] or available[:3]

# 4. Round Robin Execution
intel = None
successful_model = None

for model in ordered_targets:
    print(f"🤖 Trying model: {model}...")
    data = call_gemini(api_key, model, prompt)
    
    if 'candidates' in data and data['candidates']:
        intel = data['candidates'][0]['content']['parts'][0]['text']
        successful_model = model
        print(f"✅ Success with {successful_model}!")
        break
    else:
        error = data.get('error', {})
        # ADDED: Quota/Rate Limit handling
        if error.get('code') == 429:
            print(f"⏳ Quota hit on {model}. Waiting 5s for backoff...")
            time.sleep(5) 
        else:
            print(f"⚠️ {model} failed: {error.get('message', 'Unknown Error')}")
            time.sleep(1)
            
# 5. Output and State Update
if intel:
    # 1. Convert Markdown to clean HTML
    # extensions=['fenced_code', 'codehilite'] makes code blocks look great
    html_body = markdown.markdown(intel, extensions=['fenced_code', 'tables'])

    # 2. Define a Professional CSS Theme
    style = """
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
               line-height: 1.6; color: #24292e; max-width: 850px; margin: 0 auto; padding: 40px 20px; background-color: #f6f8fa; }
        .card { background: white; border: 1px solid #e1e4e8; border-radius: 8px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 24px; }
        h1 { border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; color: #0366d6; }
        h2 { color: #24292e; margin-top: 24px; }
        code { background-color: rgba(27,31,35,0.05); padding: 0.2em 0.4em; border-radius: 3px; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 85%; }
        pre { background-color: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; border: 1px solid #dfe1e4; }
        pre code { background-color: transparent; padding: 0; }
        blockquote { border-left: 0.25em solid #dfe1e4; color: #6a737d; padding: 0 1em; margin: 0; }
        hr { height: 0.25em; background-color: #e1e4e8; border: 0; margin: 40px 0; }
        .meta { color: #586069; font-size: 0.9em; margin-bottom: 16px; }
    </style>
    """

    # 3. Write as a self-contained card
    with open('docs/index.html', 'a') as f:
        f.write(f"""
        {style if state['day'] == 1 else ""} 
        <div class="card">
            <div class="meta">Day {state['day']} • {successful_model} • {datetime.now().strftime('%Y-%m-%d')}</div>
            {html_body}
        </div>
        """)
    
    # 4. Save State
    state['day'] += 1
    state['pillar_idx'] = (state['pillar_idx'] + 1) % len(PILLARS)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(state, f)
else:
    print("🚨 All models exhausted. No intel generated.")
    exit(1)
