import json
from datetime import datetime

# Load the policy data
with open("data/policies.json") as f:
    policies = json.load(f)

# Construct the Markdown content
md = f"""# Housing Policy Opportunities

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Legislative & Regulatory Matrix

| Policy | Opportunity |
| :--- | :--- |
"""

# Iterate through policies to populate table rows
for p in policies["policies"]:
    md += f"| {p['name']} | {p['opportunity']} |\n"

md += """
---

### Strategic Summary
* **Density Plays:** Focus on areas recently rezoned for multi-unit conversion.
* **Incentive Tracking:** Monitor federal and provincial grants for energy-efficient retrofits (e.g., Greener Homes Grant).
* **Compliance:** Ensure all "opportunity" pathways align with the latest building code amendments.
"""

# Save to the markdown file
with open("reports/policy.md", "w") as f:
    f.write(md)

print("Report successfully generated: docs/policy.md")