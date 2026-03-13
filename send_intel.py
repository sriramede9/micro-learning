import os
import json
import requests
import time
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
        error_msg = data.get('error', {}).get('message', 'Unknown Error')
        print(f"⚠️ {model} failed: {error_msg}")
        time.sleep(1) # Tiny backoff before next attempt

# 5. Output and State Update
if intel:
    # Append to your "Social Feed"
    # In send_intel.py, update your file write:
with open('docs/index.html', 'a') as f:
    # Adding simple HTML tags so the browser renders it
    f.write(f"<html><body><h1>Day {state['day']}</h1><p>{intel}</p></body></html>")
    
    # Save State
    state['day'] += 1
    state['pillar_idx'] = (state['pillar_idx'] + 1) % len(PILLARS)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(state, f)
else:
    print("🚨 All models exhausted. No intel generated.")
    exit(1)
