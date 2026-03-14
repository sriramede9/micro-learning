import subprocess
import time
from scripts.utils.limiter import GlobalRateLimiter

# Initialize the shared limiter
limiter = GlobalRateLimiter(rpm_limit=5) # Being conservative for Free Tier

scripts = [
    "scripts/weekly_briefing.py",
    "scripts/appraisal_engine.py",
    "scripts/market_radar.py",
    "scripts/catalyst_tracker.py",
    "scripts/policy_scanner.py",
    "scripts/mortgage_optimizer.py",
    "scripts/property_intel.py",
    "scripts/radar_system.py"
]

print("🚀 Starting Smart Intelligence Pipeline...")

for script in scripts:
    # STEP 1: Wait for global slot
    limiter.wait_for_slot()
    
    # STEP 2: Execute script
    print(f"📡 Executing: {script}")
    print("💎 Preparing for High-Value Analysis. Clearing API buffers (45s)...")
    time.sleep(45)
    result = subprocess.run(["python", script])

    if result.returncode != 0:
        print(f"❌ {script} failed. Switching to cooldown mode...")
        time.sleep(30) # Hard reset cooldown if we hit a wall
    
    # STEP 3: Mandatory 'pacing' sleep to protect the TPM (Tokens Per Minute)
    time.sleep(5) 

print("🎨 Finalizing Dashboard...")
subprocess.run(["python", "scripts/build_dashboard.py"])
print("✅ Dashboard built.")