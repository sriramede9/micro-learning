import os
import json
import requests
from datetime import datetime

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

# 3. Call Gemini
api_key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
intel = response.json()['candidates'][0]['content']['parts'][0]['text']

# 4. Append to your "Social Feed"
with open('docs/index.md', 'a') as f:
    f.write(f"\n\n---\n# 🚀 Day {state['day']}: {current_pillar}\n*Generated on {datetime.now().strftime('%Y-%m-%d')}*\n\n{intel}")

# 5. Save State
state['day'] += 1
state['pillar_idx'] = (state['pillar_idx'] + 1) % len(PILLARS)
with open(PROGRESS_FILE, 'w') as f:
    json.dump(state, f)
