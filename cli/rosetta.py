import argparse
import os
import sys
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.parser.engine import ParserEngine
from backend.graph.manager import GraphManager
from backend.summarizer.engine import SummarizerEngine
from backend.models import CodeEntity

class RosettaCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Repo Rosetta - Codebase Understanding Tool")
        self.parser_engine = ParserEngine()
        self.graph_manager = GraphManager()
        self.summarizer = SummarizerEngine()
        self._setup_args()

    def _setup_args(self):
        self.parser.add_argument("path", help="Path to the repository to analyze", default=".")
        self.parser.add_argument("--verbosity", choices=["scan", "brief", "standard", "deep"], default="standard")
        self.parser.add_argument("--persona", choices=["beginner", "intermediate", "senior-engineer", "architect", "pm"], default="senior-engineer")
        self.parser.add_argument("--llm", help="LLM provider (e.g. anthropic, gemini, ollama, heuristic). Examples: --llm gemini, --llm ollama", default=None)
        self.parser.add_argument("--model", help="Specific model. Examples: --model deepseek-coder-v2, --model gemini-1.5-pro, --model qwen3-coder:30b", default=None)
        self.parser.add_argument("--output", help="Output directory", default="./docs/rosetta")
        self.parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
        self.parser.add_argument("--debug", action="store_true", help="Enable verbose debug logging")

    async def run(self):
        args = self.parser.parse_args()
        
        if args.debug:
            os.environ["ROSETTA_DEBUG"] = "true"
        
        from backend.utils.logger import logger
        logger.setup()
        
        logger.info("CLI", f"Analyzing codebase at: {os.path.abspath(args.path)}")
        logger.info("CLI", f"Configuration: Verbosity={args.verbosity}, Persona={args.persona}")
        
        if not os.path.exists(args.path):
            print(f"[!] Error: Path {args.path} does not exist.")
            sys.exit(1)

        # Real Analysis Flow
        local_path = args.path
        SUPPORTED_EXTS = {".py", ".js", ".ts", ".tsx", ".go", ".rs", ".cpp", ".h"}
        IGNORED_DIRS = {".git", "node_modules", "venv", "__pycache__", ".next", ".gemini", "brain", ".agents", "dist", "build"}

        print("[*] Scanning repository contents...")
        scan_count = 0
        for root, dirs, files in os.walk(local_path):
            path_parts = set(os.path.normpath(root).split(os.sep))
            if any(ignored in path_parts for ignored in IGNORED_DIRS):
                continue
                
            valid_files = [f for f in files if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS]
            for file in valid_files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, local_path).replace("\\", "/")
                
                # Parse
                result = self.parser_engine.parse_file(file_path)
                if result and result.get("entities") is not None:
                    scan_count += 1
                    # Keep standard ID for GraphManager compatibility
                    self.graph_manager.add_entity(CodeEntity(
                        name="module", type="module", path=rel_path,
                        line_start=1, line_end=result.get("line_count", 1)
                    ))
                    for ent in result["entities"]:
                        self.graph_manager.add_entity(CodeEntity(
                            name=ent["name"], type=ent["type"], path=rel_path,
                            line_start=ent["line_start"], line_end=ent["line_end"]
                        ))
        
        print(f"[*] Indexed {scan_count} files. Building semantic connections...")
        self.graph_manager.build_semantic_connections()
        
        await self._generate_output(args)

    async def _generate_output(self, args):
        if not os.path.exists(args.output):
            os.makedirs(args.output)
            
        if args.format == "markdown":
            await self._write_codebase_md(args)
        else:
            self._write_json_export(args)

    def _generate_mermaid(self) -> str:
        # Convert rustworkx edges to Mermaid with hierarchical subgraphs
        lines = ["graph TD", "    classDef module fill:#f9f,stroke:#333,stroke-width:2px;"]
        seen_edges = set()
        
        # Phase 1: Group modules by directory
        dirs = {}
        for internal_id in self.graph_manager.node_data:
            data = self.graph_manager.node_data[internal_id]
            if data["type"] == "module":
                d = os.path.dirname(data["path"]) or "root"
                if d not in dirs: dirs[d] = []
                dirs[d].append(data)

        # Phase 2: Create subgraphs
        for d, modules in dirs.items():
            sub_id = d.replace("/", "_").replace("\\", "_").replace(".", "_")
            lines.append(f"    subgraph {sub_id} [{d}]")
            for m in modules:
                m_label = os.path.basename(m["path"])
                lines.append(f'        "{m["path"]}"["{m_label}"]:::module')
            lines.append("    end")

        # Phase 3: Add edges
        for edge_id in self.graph_manager.graph.edge_indices():
            u_idx, v_idx = self.graph_manager.graph.get_edge_endpoints_by_index(edge_id)
            u_data = self.graph_manager.node_data[u_idx]
            v_data = self.graph_manager.node_data[v_idx]
            
            u_key = u_data["path"].replace("\\", "/") if u_data["type"] == "module" else u_data["name"]
            v_key = v_data["path"].replace("\\", "/") if v_data["type"] == "module" else v_data["name"]
            
            if u_key != v_key:
                edge_pair = (u_key, v_key)
                if edge_pair not in seen_edges:
                    lines.append(f'    "{u_key}" --> "{v_key}"')
                    seen_edges.add(edge_pair)
        
        if len(lines) < 5: # Basic fallback
            lines.append("    Root[Codebase] --> Sub[Modules]")
            
        return "\n".join(lines) 

    async def _write_codebase_md(self, args):
        mermaid_block = self._generate_mermaid()
        
        module_rows = []
        limit = 20 # Increased limit for module reference
        count = 0
        
        print(f"[*] Generating {args.persona} summaries for key modules...")
        for node_id, internal_id in self.graph_manager.node_map.items():
            data = self.graph_manager.node_data[internal_id]
            if data["type"] == "module":
                # Enhance summary_data with structural and relational context
                summary_data = data.copy()
                summary_data["name"] = data["path"] # Use path as name for clarity
                
                # Relational context (in-degree/out-degree)
                out_edges = self.graph_manager.graph.out_edges(internal_id)
                in_edges = self.graph_manager.graph.in_edges(internal_id)
                
                # Find children (classes, functions) for this module
                children = []
                for _, other_id in self.graph_manager.node_map.items():
                    other_data = self.graph_manager.node_data[other_id]
                    if other_data["path"] == data["path"] and other_data["type"] != "module":
                        children.append({"name": other_data["name"], "type": other_data["type"]})
                
                summary_data["metadata"] = summary_data.get("metadata", {}) or {}
                summary_data["metadata"]["contained_entities"] = children
                summary_data["metadata"]["out_degree"] = len(out_edges)
                summary_data["metadata"]["in_degree"] = len(in_edges)
                
                summary = await self.summarizer.generate_summary(
                    summary_data, args.persona, args.verbosity, 
                    approved_provider=args.llm, model=args.model
                )
                module_rows.append(f"| {data['path']} | {summary} |")
                count += 1
                if count >= limit: break
        
        reference_table = "\n".join(module_rows) if module_rows else "| None | No modules identified. |"

        content = f"""# CODEBASE.md - {os.path.basename(os.path.abspath(args.path))}

## Overview
This is a high-fidelity architectural guide generated by Repo Rosetta.

## Configuration
- **Generated on**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Persona**: {args.persona}
- **Verbosity**: {args.verbosity}

## Architecture Map
```mermaid
{mermaid_block}
```

## Module Reference
| Module | Description |
|---|---|
{reference_table}

Generated by Repo Rosetta.
"""
        filename = f"codebase_{args.persona.replace('-', '_')}_{args.verbosity}.md"
        filepath = os.path.join(args.output, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Analysis complete. Results saved to: {filepath}")

    def _write_json_export(self, args):
        data = {
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "config": {
                "persona": args.persona,
                "verbosity": args.verbosity
            },
            "nodes": [],
            "edges": []
        }
        filename = f"codebase_{args.persona.replace('-', '_')}_{args.verbosity}.json"
        filepath = os.path.join(args.output, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[+] Analysis complete. Results saved to: {filepath}")

if __name__ == "__main__":
    cli = RosettaCLI()
    asyncio.run(cli.run())
