"use client";

import React, { useCallback } from 'react';
import { CollaborationPresence } from '@/components/CollaborationPresence';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
  Node,
  BackgroundVariant,
  Panel,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { GitCompare } from 'lucide-react';

const initialNodes: Node[] = [
  {
    id: 'repo-root',
    type: 'input',
    data: { label: 'repo-rosetta [root]' },
    position: { x: 250, y: 0 },
    className: 'bg-slate-900 border-2 border-blue-500 text-white rounded-lg p-4 shadow-[0_0_20px_rgba(59,130,246,0.2)]',
  },
  {
    id: 'backend',
    data: { label: 'Backend (FastAPI)' },
    position: { x: 100, y: 150 },
    className: 'bg-slate-800 border border-violet-500 text-white rounded-lg p-3',
  },
  {
    id: 'frontend',
    data: { label: 'Frontend (Next.js)' },
    position: { x: 400, y: 150 },
    className: 'bg-slate-800 border border-emerald-500 text-white rounded-lg p-3',
  },
  {
    id: 'parser',
    data: { label: 'Parser Engine' },
    position: { x: 0, y: 250 },
    className: 'bg-slate-800 border border-slate-700 text-slate-300 rounded-lg p-2 text-sm',
  },
  {
    id: 'graph',
    data: { label: 'Graph Manager' },
    position: { x: 200, y: 250 },
    className: 'bg-slate-800 border border-slate-700 text-slate-300 rounded-lg p-2 text-sm',
  },
];

const initialEdges: Edge[] = [
  { id: 'e-root-backend', source: 'repo-root', target: 'backend', animated: true, style: { stroke: '#8B5CF6' } },
  { id: 'e-root-frontend', source: 'repo-root', target: 'frontend', animated: true, style: { stroke: '#10B981' } },
  { id: 'e-backend-parser', source: 'backend', target: 'parser', label: 'uses', style: { stroke: '#64748B' } },
  { id: 'e-backend-graph', source: 'backend', target: 'graph', label: 'manages', style: { stroke: '#64748B' } },
];

export const ArchitectureMap = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  const [isRegressionMode, setIsRegressionMode] = React.useState(false);

  React.useEffect(() => {
    const fetchGraph = async () => {
      try {
        const response = await fetch('/api/graph');
        const data = await response.json();
        
        const flowNodes: Node[] = data.nodes.map((n: any, idx: number) => ({
          id: n.id,
          data: { label: `${n.name} [${n.type}]` },
          position: { x: (idx % 3) * 250, y: Math.floor(idx / 3) * 150 },
          className: n.type === 'module' 
            ? 'bg-slate-900 border-2 border-blue-500 text-white rounded-lg p-4 shadow-lg'
            : n.type === 'class'
            ? 'bg-slate-800 border border-violet-500 text-white rounded-lg p-3'
            : 'bg-slate-800 border border-slate-700 text-slate-300 rounded-lg p-2 text-sm'
        }));

        const flowEdges: Edge[] = data.edges.map((e: any) => ({
          id: `e-${e.source}-${e.target}`,
          source: e.source,
          target: e.target,
          label: e.type,
          animated: e.type === 'depends_on',
          style: { stroke: e.type === 'depends_on' ? '#8B5CF6' : '#64748B' }
        }));

        setNodes(flowNodes);
        setEdges(flowEdges);
      } catch (err) {
        console.error("Failed to fetch graph:", err);
      }
    };
    fetchGraph();
  }, []);

  const saveAnnotation = async (nodeId: string, text: string) => {
    try {
      await fetch('/api/annotation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ node_id: nodeId, author: 'User', text })
      });
      alert(`Annotation saved for ${nodeId}`);
    } catch (err) {
      console.error("Failed to save annotation:", err);
    }
  };

  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  return (
    <div className="w-full h-full bg-slate-950">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeContextMenu={(event, node) => {
          event.preventDefault();
          const note = prompt(`Add Team Note for ${node.data.label}:`);
          if (note) {
            saveAnnotation(node.id, note);
          }
        }}
        onSelectionChange={({ nodes }) => {
          if (nodes.length > 1) {
            console.log(`Multi-selection active: ${nodes.length} entities selected`);
          }
        }}
        multiSelectionKeyCode="Shift"
        fitView
        colorMode="dark"
      >
        <Controls className="bg-slate-900 border-slate-800 text-white fill-white [&_button]:border-slate-800" />
        
        {/* P6: Regression & Collaboration Panels */}
        <Panel position="top-right" className="flex flex-col gap-2">
          <button 
            onClick={() => setIsRegressionMode(!isRegressionMode)}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg border font-bold text-xs transition-all shadow-lg ${
              isRegressionMode 
                ? 'bg-emerald-500/20 border-emerald-500 text-emerald-400' 
                : 'bg-slate-900 border-slate-700 text-slate-400 hover:border-slate-500'
            }`}
          >
            <GitCompare size={14} />
            {isRegressionMode ? 'REGRESSION MODE: ACTIVE' : 'VIEW ARCHITECTURAL CHANGES'}
          </button>
          <div className="bg-slate-900/80 backdrop-blur border border-slate-800 p-1.5 rounded-full shadow-xl">
             <CollaborationPresence />
          </div>
        </Panel>

        <MiniMap 
          className="bg-slate-900 border border-slate-800" 
          nodeColor={(node) => {
            if (isRegressionMode) {
                if (node.id === 'parser') return '#10B981'; // Mock "Added"
                if (node.id === 'backend') return '#F59E0B'; // Mock "Modified"
            }
            if (node.id === 'backend') return '#8B5CF6';
            if (node.id === 'frontend') return '#10B981';
            return '#3B82F6';
          }}
          maskColor="rgba(15, 23, 42, 0.6)"
        />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} color="#1e293b" />
      </ReactFlow>
    </div>
  );
};
