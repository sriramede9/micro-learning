import json
from datetime import datetime

# Load the infrastructure data
with open("data/infrastructure.json") as f:
    infra = json.load(f)

# Define the property context
PROPERTY_ADDRESS = "384 Lolita Gardens"

# Construct the Markdown content
md = f"""# Infrastructure Catalysts

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Major Drivers Near {PROPERTY_ADDRESS}
"""

# Add infrastructure items as a bulleted list
for item in infra["infrastructure"]:
    md += f"- {item}\n"

md += """
---

## Expected Impact

* **Transit Proximity:** Direct appreciation of land value and "walk score" premiums.
* **Hospital Employment Hub:** Sustained increase in professional rental demand and low vacancy rates.
* **Mixed-Use Development:** Improved local amenities and neighborhood desirability via new retail/residential towers.

---
**Note:** These catalysts are primary indicators for long-term equity growth in the Peel Region.
"""

# Save to the markdown file
with open("reports/catalysts.md", "w") as f:
    f.write(md)

print("Report successfully generated: docs/catalysts.md")