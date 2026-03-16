from sqlalchemy import Column, String, Integer, DateTime, Text
from backend.db.session import Base
from datetime import datetime

class Annotation(Base):
    __tablename__ = "annotations"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, index=True)
    author = Column(String)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class AuditLogEntry(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    repo_id = Column(String, index=True)
    action = Column(String)
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
