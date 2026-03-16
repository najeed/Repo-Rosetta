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

    def add_relationship(self, source_id_str: str, target_id_str: str, relationship_type: str):
        """source_id_str and target_id_str are the path:name identifiers."""
        if source_id_str in self.node_map and target_id_str in self.node_map:
            self.graph.add_edge(
                self.node_map[source_id_str], 
                self.node_map[target_id_str], 
                {"type": relationship_type}
            )

    def build_semantic_connections(self):
        """
        Analyzes the existing entities in the graph and creates edges based on imports.
        This is a basic implementation that looks for exact name matches across files.
        """
        imports = []
        definitions = {} # name -> list of node_id_strs

        # Phase 1: Inventory all imports and definitions
        for node_id in self.graph.node_indices():
            data = self.node_data[node_id]
            node_id_str = self.graph[node_id]
            
            if data["type"] == "import":
                imports.append((node_id, data))
            else:
                name = data["name"]
                if name not in definitions:
                    definitions[name] = []
                definitions[name].append(node_id_str)

        # Phase 2: Link imports to definitions
        for imp_node_id, imp_data in imports:
            imp_name = imp_data["name"]
            # Simple heuristic: if the imported name exists as a class/function elsewhere
            if imp_name in definitions:
                for target_id_str in definitions[imp_name]:
                    source_id_str = self.graph[imp_node_id]
                    # Link the FILE containing the import to the target entity
                    # or link the import node itself? Usually file-to-entity is better for summary.
                    file_node_id_str = f"{imp_data['path']}:module"
                    if file_node_id_str in self.node_map:
                        self.add_relationship(file_node_id_str, target_id_str, "depends_on")

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
