import pytest
from backend.graph.manager import GraphManager
from backend.models import CodeEntity

def test_semantic_linking():
    manager = GraphManager()
    
    # Add a definition node
    entity1 = CodeEntity(
        name="TargetFunc",
        type="function",
        path="backend/utils.py",
        line_start=1,
        line_end=10
    )
    manager.add_entity(entity1)
    
    # Add a module node (normally created by the orchestrator)
    module_entity = CodeEntity(
        name="module",
        type="module",
        path="backend/main.py",
        line_start=1,
        line_end=100
    )
    manager.add_entity(module_entity)
    
    # Add an import node in main.py
    import_entity = CodeEntity(
        name="TargetFunc", # Importing TargetFunc
        type="import",
        path="backend/main.py",
        line_start=1,
        line_end=1
    )
    manager.add_entity(import_entity)
    
    # Build connections
    manager.build_semantic_connections()
    
    # Verify the edge exists from main.py:module to backend/utils.py:TargetFunc
    graph_data = manager.get_graph_data()
    edges = graph_data["edges"]
    
    # Source: backend/main.py:module
    # Target: backend/utils.py:TargetFunc
    found = False
    for edge in edges:
        if edge["source"] == "backend/main.py:module" and edge["target"] == "backend/utils.py:TargetFunc":
            found = True
            assert edge["type"] == "depends_on"
            
    assert found, "Semantic link 'depends_on' not found between module and imported entity"

if __name__ == "__main__":
    test_semantic_linking()
