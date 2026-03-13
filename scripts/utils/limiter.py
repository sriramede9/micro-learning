import time
import json
import os

class GlobalRateLimiter:
    """A persistent, file-based token bucket to sync across multiple Python processes."""
    STATE_FILE = ".api_state.json"

    def __init__(self, rpm_limit=10, tpm_limit=1000000):
        self.rpm_limit = rpm_limit
        self.tpm_limit = tpm_limit
        self._load_state()

    def _load_state(self):
        if os.path.exists(self.STATE_FILE):
            with open(self.STATE_FILE, 'r') as f:
                self.state = json.load(f)
        else:
            # FIX: Use self.rpm_limit here
            self.state = {"tokens": self.rpm_limit, "last_refill": time.time()}

    def _save_state(self):
        with open(self.STATE_FILE, 'w') as f:
            json.dump(self.state, f)

    def wait_for_slot(self):
        now = time.time()
        elapsed = now - self.state["last_refill"]
        
        # Refill tokens based on time passed
        refill_amount = elapsed * (self.rpm_limit / 60.0)
        self.state["tokens"] = min(self.rpm_limit, self.state["tokens"] + refill_amount)
        self.state["last_refill"] = now

        if self.state["tokens"] < 1:
            wait_time = (1 - self.state["tokens"]) * (60.0 / self.rpm_limit)
            print(f"⏳ Global Throttle: Waiting {wait_time:.2f}s for API slot...")
            time.sleep(wait_time)
            self.state["tokens"] = 0
        else:
            self.state["tokens"] -= 1
        
        self._save_state()
