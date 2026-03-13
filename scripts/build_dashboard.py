import markdown
from pathlib import Path

REPORTS = [
    "weekly.md",
    "property.md",
    "appraisal.md",
    "market.md",
    "policy.md",
    "catalysts.md",
    "mortgage.md",
    "radar.md"
]

html_sections = ""

for r in REPORTS:
    path = Path("reports") / r
    if path.exists():
        md = path.read_text()
        html = markdown.markdown(md, extensions=["tables","fenced_code"])
        html_sections += f"<div class='card'>{html}</div>"

style = """
<style>
body {
    font-family: system-ui;
    background:#0f172a;
    color:white;
    max-width:1200px;
    margin:auto;
    padding:40px;
}

.card {
    background:#1e293b;
    padding:30px;
    border-radius:12px;
    margin-bottom:30px;
}

h1 {color:#38bdf8}
table {width:100%;border-collapse:collapse}
td,th {border:1px solid #334155;padding:8px}
</style>
"""

html = f"""
<html>
<head>{style}</head>
<body>

<h1>🏠 Property Intelligence Terminal</h1>

{html_sections}

</body>
</html>
"""

Path("docs/index.html").write_text(html)