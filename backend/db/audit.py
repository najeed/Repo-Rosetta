from datetime import datetime
from typing import Optional

class AuditLogger:
    def __init__(self, log_dir: str = "logs/audit"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def log_access(self, user_id: str, repo_id: str, action: str, ip_address: Optional[str] = None):
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] User: {user_id} | Repo: {repo_id} | Action: {action} | IP: {ip_address or 'unknown'}\n"
        
        log_file = os.path.join(self.log_dir, f"audit_{datetime.now().strftime('%Y-%m')}.log")
        with open(log_file, "a") as f:
            f.write(log_entry)
        print(f"[*] Audit logged: {action} on {repo_id} by {user_id}")
import os
