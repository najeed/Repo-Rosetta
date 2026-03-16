import rustworkx as rx
from typing import Dict, Any, List, Set

class GraphDiffEngine:
    @staticmethod
    def compare_graphs(baseline: rx.PyDiGraph, current: rx.PyDiGraph) -> Dict[str, List[str]]:
        """
        Compares two graphs and returns sets of added/removed/modified nodes.
        Labels are assumed to be the 'path:name' unique strings.
        """
        baseline_nodes = {baseline[i] for i in baseline.node_indices()}
        current_nodes = {current[i] for i in current.node_indices()}
        
        added = list(current_nodes - baseline_nodes)
        removed = list(baseline_nodes - current_nodes)
        
        # Modified is complex (requires comparing node weights/data)
        # For now, we identity nodes that exist in both
        common = current_nodes & baseline_nodes
        modified = [] # Placeholder for deep property comparison
        
        return {
            "added": sorted(added),
            "removed": sorted(removed),
            "modified": modified
        }

    @staticmethod
    def get_regression_metadata(node_id: str) -> Dict[str, Any]:
        # Return metadata about architectural impact
        if "api" in node_id:
            return {"impact": "high", "type": "Interface Change"}
        return {"impact": "low", "type": "Internal Modification"}
