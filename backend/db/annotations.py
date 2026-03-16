from typing import Dict, List, Optional
import json
import os

ANNOTATIONS_FILE = "backend/db/annotations.json"

from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.db.schema import Annotation as AnnotationModel

class AnnotationManager:
    @staticmethod
    def save_annotation(node_id: str, author: str, text: str):
        db: Session = SessionLocal()
        try:
            db_annotation = AnnotationModel(
                node_id=node_id,
                author=author,
                text=text
            )
            db.add(db_annotation)
            db.commit()
            db.refresh(db_annotation)
            return db_annotation
        finally:
            db.close()

    @staticmethod
    def get_annotations(node_id: str) -> List[Dict[str, Any]]:
        db: Session = SessionLocal()
        try:
            results = db.query(AnnotationModel).filter(AnnotationModel.node_id == node_id).all()
            return [
                {
                    "author": r.author,
                    "text": r.text,
                    "timestamp": r.timestamp.isoformat()
                } for r in results
            ]
        finally:
            db.close()

    @staticmethod
    def get_all_annotations() -> Dict[str, List[Dict[str, Any]]]:
        db: Session = SessionLocal()
        try:
            all_ann = db.query(AnnotationModel).all()
            formatted = {}
            for a in all_ann:
                if a.node_id not in formatted:
                    formatted[a.node_id] = []
                formatted[a.node_id].append({
                    "author": a.author,
                    "text": a.text,
                    "timestamp": a.timestamp.isoformat()
                })
            return formatted
        finally:
            db.close()
