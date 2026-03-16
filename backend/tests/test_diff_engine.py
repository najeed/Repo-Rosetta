import pytest
import rustworkx as rx
from backend.ecosystem.diff_engine import GraphDiffEngine

def test_graph_comparison():
    baseline = rx.PyDiGraph()
    baseline.add_node("file1:func1")
    baseline.add_node("file1:func2")
    
    current = rx.PyDiGraph()
    current.add_node("file1:func1")
    current.add_node("file2:func3")
    
    delta = GraphDiffEngine.compare_graphs(baseline, current)
    
    assert "file2:func3" in delta["added"]
    assert "file1:func2" in delta["removed"]
    assert "file1:func1" not in delta["added"]
    assert "file1:func1" not in delta["removed"]
    assert len(delta["added"]) == 1
    assert len(delta["removed"]) == 1

def test_regression_metadata():
    engine = GraphDiffEngine()
    meta = engine.get_regression_metadata("backend/api/router.py:analyze")
    assert meta["impact"] == "high"
    
    meta_low = engine.get_regression_metadata("backend/utils/helper.py:debug")
    assert meta_low["impact"] == "low"

if __name__ == "__main__":
    test_graph_comparison()
