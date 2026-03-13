import subprocess
import time
from scripts.utils.limiter import GlobalRateLimiter

# Initialize the shared limiter
limiter = GlobalRateLimiter(rpm_limit=5) # Being conservative for Free Tier

scripts = [
    "scripts/appraisal_engine.py",
    "scripts/policy_scanner.py",
    "scripts/property_intel.py",  # Heavy Logic
    "scripts/radar_system.py"
]

print("🚀 Starting Smart Intelligence Pipeline...")

for script in scripts:
    # STEP 1: Wait for global slot
    limiter.wait_for_slot()
    
    # STEP 2: Execute script
    print(f"📡 Executing: {script}")
    result = subprocess.run(["python", script])
    
    if result.returncode != 0:
        print(f"❌ {script} failed. Switching to cooldown mode...")
        time.sleep(30) # Hard reset cooldown if we hit a wall
    
    # STEP 3: Mandatory 'pacing' sleep to protect the TPM (Tokens Per Minute)
    time.sleep(5) 

print("🎨 Finalizing Dashboard...")
