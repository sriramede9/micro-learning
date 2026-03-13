import json
from datetime import datetime

# Load the property data
with open("data/property_profile.json") as f:
    property_data = json.load(f)

APPRAISAL_FACTORS = [
    "Lot frontage 46.7 ft",
    "Lot depth 121 ft",
    "Detached 2-storey house",
    "Finished basement with kitchen",
    "Parking capacity for 7 vehicles",
    "R3 zoning classification",
    "Transit proximity (LRT + GO)",
    "Hospital employment hub proximity",
    "Highway access (403/QEW)",
    "Neighborhood growth indicators"
]

# Construct the Markdown content
md = f"""# Appraisal Intelligence

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Property Profile
- **Address:** {property_data['address']}
- **City:** {property_data['city']}

## Appraisal Factors
"""

# Add factors as a bulleted list
for factor in APPRAISAL_FACTORS:
    md += f"- {factor}\n"

md += """
---

## Analysis Prompt (LPS Guidance)
> **Role:** Act as a licensed Canadian Residential Appraiser.

### Evaluation Criteria:
1. **Primary Appraisal Drivers:** Core physical and location-based value.
2. **Hidden Value Drivers:** Zoning, transit, and infrastructure proximity.
3. **The $100k+ Value Delta:** Improvements or market shifts required to move the needle.
4. **Lender Perspectives:** Key metrics for refinancing (LTV, stability).
5. **Investor vs. Homeowner:** Utility vs. Yield perspectives.
6. **Risk Factors:** Market volatility or property-specific liabilities.
"""

# Save to the markdown file
with open("reports/appraisal.md", "w") as f:
    f.write(md)

print("Report successfully generated: docs/appraisal.md")