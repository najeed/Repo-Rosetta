import rustworkx as rx
import os
import re
from typing import List, Dict, Any
from backend.models import CodeEntity

class GraphManager:
    def __init__(self):
        self.graph = rx.PyDiGraph()
        self.node_map = {}  # Map path:name to internal integer ID
        self.node_data = {} # Map internal ID to entity data

    def clear(self):
        """Resets the graph and all associated metadata for a fresh analysis."""
        self.graph = rx.PyDiGraph()
        self.node_map = {}
        self.node_data = {}

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
        Enhanced to handle module hierarchy and partial matches.
        """
        imports = []
        definitions = {} # name -> list of node_id_strs
        modules = {}     # normalized_module_path -> internal_id

        # Phase 1: Inventory all imports, definitions and modules
        for node_id in self.graph.node_indices():
            data = self.node_data[node_id]
            node_id_str = self.graph[node_id]
            
            if data["type"] == "import":
                imports.append((node_id, data))
            elif data["type"] == "module":
                # Normalize path for matching (e.g. backend/parser/engine.py -> backend.parser.engine)
                norm_path = data["path"].replace(".py", "").replace("/", ".").replace("\\", ".")
                modules[norm_path] = node_id
                definitions[data["name"]] = [node_id_str]
            else:
                name = data["name"]
                if name not in definitions:
                    definitions[name] = []
                definitions[name].append(node_id_str)

        # Phase 2: Link imports to definitions or modules
        for imp_node_id, imp_data in imports:
            # Strip quotes/backticks for JS/TS/Go imports
            imp_name = imp_data["name"].strip("\"'`")
            
            # Handle relative JS/TS paths (./utils -> utils)
            if imp_name.startswith("./") or imp_name.startswith("../"):
                imp_name = os.path.basename(imp_name)

            source_file_id_str = f"{imp_data['path']}:module"
            
            # Heuristic match: Exact name (classes/functions)
            if imp_name in definitions:
                for target_id_str in definitions[imp_name]:
                    if source_file_id_str != target_id_str:
                        self.add_relationship(source_file_id_str, target_id_str, "depends_on")
            
            # Heuristic match: Module import (e.g. backend.parser.engine)
            for mod_norm, mod_id in modules.items():
                if mod_norm.endswith(imp_name) or imp_name.endswith(mod_norm):
                    target_id_str = self.graph[mod_id]
                    if source_file_id_str != target_id_str:
                        self.add_relationship(source_file_id_str, target_id_str, "imports")

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
                "id": f"e-{self.graph[source]}-{self.graph[target]}-{edge_id}",
                "source": self.graph[source],
                "target": self.graph[target],
                **data
            })
            
        return {"nodes": nodes, "edges": edges}

    def find_relevant_nodes(self, query: str, limit: int = 5) -> List[str]:
        """Finds node IDs related to the query keywords."""
        # Pre-check exact ID match
        if query in self.node_map:
            return [query]

        # Tokenize better: split by space and common separators
        keywords = re.split(r'[\s:/\\._\-"]+', query.lower())
        keywords = [k for k in keywords if k and len(k) > 1]
        
        scores = []
        for node_id in self.graph.node_indices():
            data = self.node_data[node_id]
            id_str = self.graph[node_id]
            id_str_lower = id_str.lower()
            
            # Simple scoring: matches in name/path/summary
            score = 0
            text = f"{data['name']} {data['path']} {data.get('summary', '')}".lower()
            
            # Boost score for direct substring match of the whole query in the ID
            if query.lower() in id_str_lower:
                score += 10

            for kw in keywords:
                if kw in text or kw in id_str_lower:
                    score += 1
            
            if score > 0:
                scores.append((score, id_str))
        
        # Sort by score and return top limit
        scores.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scores[:limit]]

    def get_node_context(self, node_id_str: str) -> str:
        """Returns a string describing a node and its immediate neighbors."""
        if node_id_str not in self.node_map:
            return ""
        
        internal_id = int(self.node_map[node_id_str])
        data = self.node_data[internal_id]
        
        context = f"Node `{node_id_str}` ({data['type']}): {data.get('summary', 'No summary available.')}\n"
        
        # Add neighbors (traversal)
        successors = [self.graph[int(i)] for i in self.graph.successors(internal_id)]
        predecessors = [self.graph[int(i)] for i in self.graph.predecessors(internal_id)]
        
        if successors:
            context += f"  - Relies on: {', '.join(successors)}\n"
        if predecessors:
            context += f"  - Is used by: {', '.join(predecessors)}\n"
            
        return context
    def get_execution_flow(self, start_node_id_str: str, depth: int = 3) -> Dict[str, Any]:
        """Traces a workflow from a starting node through the semantic graph."""
        if start_node_id_str not in self.node_map:
            return {"nodes": [], "edges": []}
            
        internal_start = self.node_map[start_node_id_str]
        
        # Simple BFS traversal up to 'depth'
        visited_nodes = {internal_start}
        visited_edges = []
        queue = [(internal_start, 0)]
        
        while queue:
            curr_node, curr_depth = queue.pop(0)
            if curr_depth >= depth:
                continue
                
            for neighbor_id in self.graph.successors(int(curr_node)):
                neighbor_id = int(neighbor_id)
                if neighbor_id not in visited_nodes:
                    visited_nodes.add(neighbor_id)
                    queue.append((neighbor_id, curr_depth + 1))
                
                # Capture the edge
                edge_data = self.graph.get_edge_data(int(curr_node), neighbor_id)
                visited_edges.append({
                    "id": f"trace-e-{len(visited_edges)}",
                    "source": self.graph[int(curr_node)],
                    "target": self.graph[neighbor_id],
                    "type": edge_data.get("type", "dependency")
                })
        
        nodes = []
        for n_id in visited_nodes:
            nodes.append({
                "id": self.graph[n_id],
                **self.node_data[n_id]
            })
            
        return {"nodes": nodes, "edges": visited_edges}
