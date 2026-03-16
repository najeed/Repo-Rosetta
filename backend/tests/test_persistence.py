import pytest
import os
from backend.db.annotations import AnnotationManager
from backend.db.audit import AuditLogger
from backend.db.session import SessionLocal, engine, Base
from backend.db.schema import Annotation, AuditLogEntry

def setup_module(module):
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

def test_annotation_persistence():
    node_id = "test/file.py:TestFunc"
    author = "Tester"
    text = "Initial annotation"
    
    # Save
    AnnotationManager.save_annotation(node_id, author, text)
    
    # Get
    annotations = AnnotationManager.get_annotations(node_id)
    assert len(annotations) > 0
    assert annotations[-1]["text"] == text
    assert annotations[-1]["author"] == author

def test_audit_persistence():
    logger = AuditLogger()
    user_id = "test_user"
    repo_id = "test_repo"
    action = "test_action"
    
    # Log
    logger.log_access(user_id, repo_id, action)
    
    # Check DB directly for verification
    db = SessionLocal()
    try:
        entry = db.query(AuditLogEntry).filter(AuditLogEntry.action == action).first()
        assert entry is not None
        assert entry.user_id == user_id
    finally:
        db.close()

if __name__ == "__main__":
    test_annotation_persistence()
