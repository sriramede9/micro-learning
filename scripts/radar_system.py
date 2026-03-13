import json
from datetime import datetime

# Centralized coordinates for 384 Lolita Gardens
HOME_BASE = {"lat": 43.581, "lng": -79.617}

def check_intensification_zone():
    """
    Simulates checking the Mississauga Planning Portal for Bill 23
    and 'Missing Middle' rezoning within 1km.
    """
    # In a production version, you would use requests.get() on Mississauga's Open Data API
    active_permits = [
        {"address": "600-620 Lolita Gardens", "status": "Proposed", "type": "25-storey Residential"},
        {"address": "384 Lolita Gardens", "status": "R3-Zoned", "type": "Garden Suite Potential"}
    ]
    return active_permits

md = f"""# 📡 Neighborhood Radar (1km Radius)
Generated: {datetime.now().strftime("%Y-%m-%d")}

## 🏗️ Active Development & Intensification
"""

permits = check_intensification_zone()
for p in permits:
    md += f"- **{p['address']}**: {p['type']} ({p['status']})\n"

md += """
---
### 💡 Strategic Insight
The proximity to the **Hazel McCallion LRT** and **Peter Gilgan Hospital** creates a 'Golden Radius'.
Any permit for a 4+ unit conversion within 500m of 384 Lolita directly increases your land value
due to 'comparable density' precedents.
"""

with open("reports/radar.md", "w") as f:
    f.write(md)

print("Radar report generated: reports/radar.md")