"use client";

import React from 'react';
import { ExternalLink, Activity, Info, Code2, Layers, MessageSquare } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface ExplanationPanelProps {
  entityName?: string;
  type?: string;
  lineCount?: number;
  purpose?: string;
  keyFunctions?: { name: string; line: number }[];
  dependencies?: string[];
  persona: string;
  setPersona: (persona: string) => void;
  verbosity: string;
  setVerbosity: (verbosity: string) => void;
  selectedNodeId?: string | null;
  isLoading?: boolean;
  isDebugEnabled?: boolean;
  onTrace?: (nodeId: string) => void;
}

export const ExplanationPanel: React.FC<ExplanationPanelProps> = ({
  entityName,
  type,
  lineCount,
  purpose,
  keyFunctions,
  dependencies,
  persona,
  setPersona,
  verbosity,
  setVerbosity,
  selectedNodeId,
  isLoading,
  isDebugEnabled,
  onTrace
}) => {
  const [annotations, setAnnotations] = React.useState<any[]>([]);

  React.useEffect(() => {
    if (selectedNodeId) {
      const fetchAnnotations = async () => {
        try {
          const res = await fetch(`/api/annotations/${encodeURIComponent(selectedNodeId)}`);
          if (res.ok) {
            const data = await res.json();
            setAnnotations(data);
          }
        } catch (err) {
          console.error("Failed to fetch annotations:", err);
        }
      };
      fetchAnnotations();
    }
  }, [selectedNodeId]);

  return (
    <div className="w-[450px] h-full bg-slate-900/80 backdrop-blur-xl border-l border-slate-800 text-slate-200 flex flex-col shadow-2xl overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-slate-800 bg-slate-900/40">
        <div className="flex justify-between items-start mb-2">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Code2 className="text-blue-400" size={24} />
            {entityName}
          </h2>
          <span className="px-2 py-1 rounded bg-slate-800 text-xs font-medium text-slate-400 border border-slate-700">
            {lineCount} lines
          </span>
        </div>
        <p className="text-sm font-medium text-blue-400 flex items-center gap-1.5 uppercase tracking-wider">
          <Layers size={14} />
          {type}
        </p>
      </div>

      {/* Controls */}
      <div className="px-6 py-4 bg-slate-900/60 border-b border-slate-800 flex gap-4">
        <div className="flex-1">
          <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1.5 block">Persona</label>
          <select 
            value={persona} 
            onChange={(e) => setPersona(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-1.5 text-sm focus:ring-2 focus:ring-blue-500/40 outline-none transition-all cursor-pointer"
          >
            <option value="intermediate">Intermediate</option>
            <option value="senior-engineer">Senior Engineer</option>
            <option value="architect">System Architect</option>
            <option value="pm">Product Manager</option>
          </select>
        </div>
        <div className="flex-1">
          <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1.5 block">Verbosity</label>
          <div className="flex gap-1 h-[34px] items-center">
            {["scan", "brief", "standard", "deep"].map((v) => (
              <button
                key={v}
                onClick={() => setVerbosity(v)}
                className={cn(
                  "flex-1 h-2 rounded-full transition-all",
                  verbosity === v ? "bg-blue-500 shadow-[0_0_12px_rgba(59,130,246,0.5)]" : "bg-slate-700 hover:bg-slate-600"
                )}
                title={v}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">
        {/* Purpose */}
        <section>
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-[0.2em] mb-3 flex items-center gap-2">
            <Info size={14} className="text-slate-400" />
            Purpose
          </h3>
          {isLoading ? (
            <div className="space-y-2 animate-pulse">
              <div className="h-4 bg-slate-800 rounded w-full" />
              <div className="h-4 bg-slate-800 rounded w-5/6" />
              <div className="h-4 bg-slate-800 rounded w-4/6" />
            </div>
          ) : (
            <p className="text-slate-300 leading-relaxed text-[15px]">
              {purpose}
            </p>
          )}
        </section>

        {/* Key Functions */}
        <section>
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-[0.2em] mb-3 flex items-center gap-2">
            <Activity size={14} className="text-slate-400" />
            Key Functions
          </h3>
          {isLoading ? (
            <div className="space-y-2 animate-pulse">
              {[1, 2, 3].map((v) => (
                <div key={v} className="h-10 bg-slate-800 rounded-lg w-full" />
              ))}
            </div>
          ) : (
            <div className="space-y-2">
              {keyFunctions?.map((fn, idx) => (
                <button key={idx} className="w-full flex justify-between items-center group p-2.5 rounded-lg bg-slate-800/40 hover:bg-slate-800 border border-slate-700/50 hover:border-slate-600 transition-all">
                  <span className="text-sm font-mono text-blue-300 group-hover:text-blue-200">{fn.name}</span>
                  <span className="text-[10px] text-slate-500 font-mono">L{fn.line}</span>
                </button>
              ))}
            </div>
          )}
        </section>

        {/* Saved Annotations (Internal Context) */}
        <section>
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-[0.2em] mb-3 flex items-center gap-2">
            <MessageSquare size={14} className="text-slate-400" />
            Saved Annotations
          </h3>
          <div className="space-y-2">
            {annotations.length > 0 ? annotations.map((ann, idx) => (
              <div key={idx} className="p-2.5 rounded-lg bg-slate-800/20 border border-slate-800 flex flex-col gap-1 hover:border-slate-600 transition-colors">
                <div className="flex justify-between items-center text-[10px] font-bold">
                  <span className="text-blue-400 uppercase tracking-tighter">{ann.author}</span>
                  <span className="text-slate-600 font-mono">{new Date(ann.timestamp).toLocaleDateString()}</span>
                </div>
                <p className="text-xs text-slate-300 italic">&quot;{ann.text}&quot;</p>
              </div>
            )) : (
              <div className="p-3 rounded-lg border border-dashed border-slate-800 text-center">
                <p className="text-[10px] text-slate-500 uppercase tracking-widest">No annotations found</p>
              </div>
            )}
          </div>
        </section>

        {/* Dependencies */}
        <section>
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-[0.2em] mb-3 flex items-center gap-2">
            <Layers size={14} className="text-slate-400" />
            Dependencies
          </h3>
          {isLoading ? (
            <div className="flex flex-wrap gap-2 animate-pulse">
              {[1, 2, 3, 4].map((v) => (
                <div key={v} className="h-6 bg-slate-800 rounded-full w-16" />
              ))}
            </div>
          ) : (
            <ul className="flex flex-wrap gap-2">
              {dependencies?.map((dep, idx) => (
                <li key={idx} className="px-2.5 py-1 rounded-full bg-slate-800 text-[11px] font-medium text-slate-400 border border-slate-700">
                  {dep}
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>

      {/* Footer Actions */}
      <div className="p-6 border-t border-slate-800 bg-slate-900/40 grid grid-cols-2 gap-4">
        <button 
          onClick={() => window.open(`https://github.com/fastapi/fastapi/blob/master/${entityName}`, '_blank')}
          className="flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm font-semibold text-white transition-all border border-slate-700"
        >
          <ExternalLink size={16} />
          GitHub
        </button>
        <button 
          onClick={() => selectedNodeId && onTrace && onTrace(selectedNodeId)}
          className="flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg bg-blue-600 hover:bg-blue-500 text-sm font-semibold text-white transition-all shadow-lg shadow-blue-900/20"
        >
          <Activity size={16} />
          Trace
        </button>
      </div>
    </div>
  );
};
