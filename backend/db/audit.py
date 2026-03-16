import os
from datetime import datetime
from typing import Optional

from backend.db.session import SessionLocal
from backend.db.schema import AuditLogEntry

class AuditLogger:
    def __init__(self, log_dir: str = "logs/audit"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def log_access(self, user_id: str, repo_id: str, action: str, ip_address: Optional[str] = None):
        # 1. Database Persistence
        db = SessionLocal()
        try:
            entry = AuditLogEntry(
                user_id=user_id,
                repo_id=repo_id,
                action=action,
                ip_address=ip_address
            )
            db.add(entry)
            db.commit()
        finally:
            db.close()

        # 2. File-based redundancy
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] User: {user_id} | Repo: {repo_id} | Action: {action} | IP: {ip_address or 'unknown'}\n"
        
        log_file = os.path.join(self.log_dir, f"audit_{datetime.now().strftime('%Y-%m')}.log")
        with open(log_file, "a") as f:
            f.write(log_entry)
        print(f"[*] Audit logged to DB and file: {action} on {repo_id} by {user_id}")
