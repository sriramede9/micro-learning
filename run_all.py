import os

scripts = [
    "scripts/appraisal_engine.py",
    "scripts/market_radar.py",
    "scripts/policy_scanner.py",
    "scripts/catalyst_tracker.py",
    "scripts/mortgage_optimizer.py",
    "scripts/property_intel.py",
    "scripts/radar_system.py",
]

for s in scripts:
    print(f"🚀 Running {s}...")
    os.system(f"python {s}")

os.system("python scripts/build_dashboard.py")