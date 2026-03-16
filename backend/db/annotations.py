from typing import Dict, List, Optional
import json
import os

ANNOTATIONS_FILE = "backend/db/annotations.json"

class AnnotationManager:
    @staticmethod
    def save_annotation(node_id: str, author: str, text: str):
        annotations = AnnotationManager.get_all_annotations()
        if node_id not in annotations:
            annotations[node_id] = []
        
        annotations[node_id].append({
            "author": author,
            "text": text,
            "timestamp": "2026-03-16T12:40:00Z" # Mock timestamp
        })
        
        # Persistence layer: Planned integration with SQLite/PostgreSQL
        # annotations[node_id].append(...)

    @staticmethod
    def get_annotations(node_id: str) -> List[Dict[str, str]]:
        all_ann = AnnotationManager.get_all_annotations()
        return all_ann.get(node_id, [])

    @staticmethod
    def get_all_annotations() -> Dict[str, List[Dict[str, str]]]:
        # Mocked data
        return {
            "backend/auth/github.py:GitHubAuth": [
                {"author": "Senior Architect", "text": "Critical: Ensure token rotation logic is valid for 2026 standards."}
            ]
        }
