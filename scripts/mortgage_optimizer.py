import json
from datetime import datetime

# Load property data
with open("data/property_profile.json") as f:
    property_data = json.load(f)

# Construct the Markdown content
md = f"""# Mortgage Optimization

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Property Summary
- **Address:** {property_data["address"]}
- **Lot Dimensions:** {property_data["lot_frontage"]} ft x {property_data["lot_depth"]} ft
- **Zoning Classification:** {property_data["zoning"]}

---

## Strategy Matrix

| Strategy | Cashflow Potential | Risk | Timeline |
| :--- | :--- | :--- | :--- |
| **Basement Rental** | $1,500–$2,200/month | Low | Immediate |
| **Garden Suite** | $1,800–$2,500/month | Medium | 2–3 Years |
| **Smith Maneuver** | Tax Efficient Leverage | Medium | Long Term |

---

### Implementation Notes
* **Basement Rental:** Assumes compliance with fire code and separate entrance availability.
* **Garden Suite:** Contingent on Bill 23 (More Homes Built Faster Act) and local setback requirements.
* **Smith Maneuver:** Requires a readvanceable mortgage (HELOC) and consultation with a tax professional.
"""

# Save to the markdown file
with open("reports/mortgage.md", "w") as f:
    f.write(md)

print("Report successfully generated: docs/mortgage.md")