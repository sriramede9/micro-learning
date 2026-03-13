import subprocess
import sys

scripts = [
    "scripts/appraisal_engine.py",
    "scripts/market_radar.py",
    "scripts/policy_scanner.py",
    "scripts/catalyst_tracker.py",
    "scripts/mortgage_optimizer.py",
    "scripts/property_intel.py",
    "scripts/radar_system.py",
]

python = sys.executable

for s in scripts:
    print(f"🚀 EXECUTING: {s}", flush=True)
    # Using subprocess.run is cleaner for GitHub Actions than os.system
    result = subprocess.run([python, s])
    
    if result.returncode != 0:
        print(f"❌ {s} failed with exit code {result.returncode}", flush=True)

print("🎨 Finalizing Dashboard...", flush=True)
subprocess.run([python, "scripts/build_dashboard.py"])
