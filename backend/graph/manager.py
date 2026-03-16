import rustworkx as rx
from typing import List, Dict, Any
from backend.models import CodeEntity

class GraphManager:
    def __init__(self):
        self.graph = rx.PyDiGraph()
        self.node_map = {}  # Map path:name to internal integer ID
        self.node_data = {} # Map internal ID to entity data

    def add_entity(self, entity: CodeEntity):
        node_id_str = f"{entity.path}:{entity.name}"
        if node_id_str not in self.node_map:
            internal_id = self.graph.add_node(node_id_str)
            self.node_map[node_id_str] = internal_id
            self.node_data[internal_id] = {
                "name": entity.name,
                "type": entity.type,
                "path": entity.path,
                "line_start": entity.line_start,
                "line_end": entity.line_end,
                "summary": entity.summary,
                "metadata": entity.metadata
            }

    def add_relationship(self, source_id: str, target_id: str, relationship_type: str):
        if source_id in self.node_map and target_id in self.node_map:
            self.graph.add_edge(
                self.node_map[source_id], 
                self.node_map[target_id], 
                {"type": relationship_type}
            )

    def get_graph_data(self) -> Dict[str, Any]:
        nodes = []
        for node_id in self.graph.node_indices():
            nodes.append({
                "id": self.graph[node_id],
                **self.node_data[node_id]
            })
            
        edges = []
        for edge_id in self.graph.edge_indices():
            source, target = self.graph.get_edge_endpoints_by_index(edge_id)
            data = self.graph.get_edge_data_by_index(edge_id)
            edges.append({
                "source": self.graph[source],
                "target": self.graph[target],
                **data
            })
            
        return {"nodes": nodes, "edges": edges}
