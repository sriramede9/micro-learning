import json
from datetime import datetime

with open("data/comparables.json") as f:
    comps = json.load(f)

md = f"""
# Market Radar

Generated: {datetime.now()}

## Comparable Properties
"""

for c in comps["comparables"]:
    md += f"- {c['address']} — {c['city']}\n"

md += """

## Analysis Goals

- Average detached home price
- Renovation premium
- Price per square foot
- Investor activity signals
- 12 month price outlook

## Data Sources

- Toronto Regional Real Estate Board
- HouseSigma
- Zolo
"""

with open("reports/market.md", "w") as f:
    f.write(md)