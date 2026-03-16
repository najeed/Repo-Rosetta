"use client";

import React, { useState, useRef } from 'react';
import { ArchitectureMap } from '@/components/ArchitectureMap';
import { ExplanationPanel } from '@/components/ExplanationPanel';
import { AuthGate } from '@/components/AuthGate';
import { ChatOverlay } from '@/components/ChatOverlay';
import { Search, Github, Menu, Settings as SettingsIcon, Shield, MessageSquare, Activity, Layers } from 'lucide-react';
import { clsx } from 'clsx';

export default function Home() {
  const [persona, setPersona] = useState('senior-engineer');
  const [verbosity, setVerbosity] = useState('standard');
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [selectedNodeData, setSelectedNodeData] = useState<any>(null);
  const [isPrivate, setIsPrivate] = useState(false);
  const [isDebugEnabled, setIsDebugEnabled] = useState(false);
  const [repoUrl, setRepoUrl] = useState('https://github.com/fastapi/fastapi');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [graphKey, setGraphKey] = useState(0);
  const [authToken, setAuthToken] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [summaryData, setSummaryData] = useState<any>(null);
  const [isLoadingSummary, setIsLoadingSummary] = useState(false);
  const [activeTrace, setActiveTrace] = useState<any>(null);

  const searchInputRef = React.useRef<HTMLInputElement>(null);

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    try {
      const url = new URL('/api/analyze', window.location.origin);
      url.searchParams.append('repo_url', repoUrl);
      url.searchParams.append('is_private', isPrivate.toString());
      if (authToken) url.searchParams.append('token', authToken);

      const res = await fetch(url.toString(), { method: 'POST' });
      if (res.ok) {
        setGraphKey(prev => prev + 1); // Refresh graph
      }
    } catch (err) {
      console.error("Analysis failed:", err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleTrace = async (nodeId: string) => {
    try {
      const res = await fetch(`/api/trace/${encodeURIComponent(nodeId)}`);
      if (!res.ok) throw new Error("Trace failed");
      const data = await res.json();
      if (data?.nodes && data.nodes.length > 0) {
        setActiveTrace({ nodeId, ...data });
      } else {
        alert(`Trace returned no data for ${nodeId}. Ensure the node has outbound connections in the graph.`);
      }
    } catch (err) {
      console.error("Trace failed:", err);
      alert("Failed to trace node. Check backend connectivity.");
    }
  };

  // Reactive summary fetching
  React.useEffect(() => {
    if (selectedNodeId) {
      const fetchSummary = async () => {
        setIsLoadingSummary(true);
        try {
          const res = await fetch(`/api/summary?entity_id=${encodeURIComponent(selectedNodeId)}&persona=${persona}&verbosity=${verbosity}`);
          if (res.ok) {
            const data = await res.json();
            setSummaryData(data);
          }
        } catch (err) {
          console.error("Failed to fetch summary:", err);
        } finally {
          setIsLoadingSummary(false);
        }
      };
      fetchSummary();
    }
  }, [selectedNodeId, persona, verbosity]);

  return (
    <main className="flex h-screen w-full bg-slate-950 overflow-hidden font-sans selection:bg-blue-500/30">
      {/* Sidebar / Navigation (Mini) */}
      <div className="w-16 h-full bg-slate-900 border-r border-slate-800 flex flex-col items-center py-6 gap-8 z-20">
        <button 
          onClick={() => window.open(repoUrl.startsWith('http') ? repoUrl : `https://github.com/${repoUrl}`, '_blank')}
          className="w-10 h-10 bg-gradient-to-br from-blue-500 to-violet-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20 hover:scale-105 transition-transform"
        >
          <Github className="text-white" size={24} />
        </button>
        <div className="flex-1 flex flex-col gap-6">
          <button 
            onClick={() => setIsSidebarOpen(true)}
            className="p-2 text-slate-400 hover:text-white transition-colors"
          >
            <Menu size={24} />
          </button>
          
          <div className={clsx(
            "fixed inset-0 z-[60] transition-all duration-500",
            isSidebarOpen ? "visible" : "invisible"
          )}>
             <div 
               className={clsx(
                 "absolute inset-0 bg-slate-950/80 backdrop-blur-md transition-opacity duration-500",
                 isSidebarOpen ? "opacity-100" : "opacity-0"
               )}
               onClick={() => setIsSidebarOpen(false)}
             />
             <div className={clsx(
               "absolute top-0 left-0 bottom-0 w-80 bg-slate-900 border-r border-slate-800 shadow-2xl transition-transform duration-500 cubic-bezier(0.4, 0, 0.2, 1)",
               isSidebarOpen ? "translate-x-0" : "-translate-x-full"
             )}>
               <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/40">
                 <h3 className="text-white font-bold uppercase tracking-widest text-sm flex items-center gap-2">
                   <Shield className="text-blue-500" size={16} />
                   Navigation
                 </h3>
                 <button onClick={() => setIsSidebarOpen(false)} className="w-8 h-8 rounded-full flex items-center justify-center hover:bg-slate-800 text-slate-500 hover:text-white transition-all">✕</button>
               </div>
               <div className="p-4 space-y-4">
                 <div className="p-4 rounded-2xl bg-slate-800/20 border border-slate-800/60 hover:border-blue-500/30 transition-colors group">
                   <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3">Recent Repositories</p>
                   <div className="space-y-3">
                      <button 
                        onClick={() => { setRepoUrl("https://github.com/fastapi/fastapi"); setIsSidebarOpen(false); }}
                        className="w-full flex items-center gap-3 text-xs text-blue-400 font-medium cursor-pointer hover:text-blue-300 text-left"
                      >
                        <div className="w-2 h-2 rounded-full bg-blue-500" />
                        <span className="truncate">fastapi/fastapi</span>
                      </button>
                      <button 
                        onClick={() => { setRepoUrl("https://github.com/najeed/repo-rosetta"); setIsSidebarOpen(false); }}
                        className="w-full flex items-center gap-3 text-xs text-slate-400 font-medium cursor-pointer hover:text-slate-300 text-left"
                      >
                        <div className="w-2 h-2 rounded-full bg-slate-700" />
                        <span className="truncate">najeed/repo-rosetta</span>
                      </button>
                   </div>
                 </div>
                 <div className="p-4 rounded-2xl bg-slate-800/20 border border-slate-800/60 hover:border-amber-500/30 transition-colors group">
                   <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3">Team Context</p>
                   <div className="flex items-center gap-2 text-xs text-slate-400 mb-4">
                      <MessageSquare size={14} className="text-violet-500" />
                      <span>Shared Annotations Enabled</span>
                   </div>
                   <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full w-2/3 bg-blue-500" />
                   </div>
                 </div>
               </div>
               <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-slate-800 bg-slate-900/40">
                 <div className="flex items-center gap-4">
                   <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-600 to-violet-600 flex items-center justify-center font-bold text-sm ring-2 ring-slate-800 shadow-xl">NK</div>
                   <div>
                     <div className="text-sm font-bold text-white">Najeed Khan</div>
                     <div className="text-[11px] text-slate-500 font-medium">System Maintainer</div>
                   </div>
                 </div>
               </div>
             </div>
          </div>

          <button 
            onClick={() => searchInputRef.current?.focus()}
            className="p-2 text-blue-400 hover:text-white transition-colors"
          >
            <Search size={24} />
          </button>
        </div>
        <button className="p-2 text-slate-400 hover:text-white transition-colors">
          <SettingsIcon size={24} />
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col relative">
        {/* Top Navbar */}
        <header className="h-16 border-b border-slate-800/60 bg-slate-950/50 backdrop-blur-md px-8 flex items-center justify-between z-10">
          <div className="flex items-center gap-4 flex-1">
            <h1 className="text-lg font-bold text-white tracking-tight shrink-0">Repo Rosetta</h1>
            <div className="h-4 w-px bg-slate-800 shrink-0" />
            
            <div className="flex items-center gap-2 flex-1 max-w-xl">
               <input 
                 type="text"
                 value={repoUrl}
                 onChange={(e) => setRepoUrl(e.target.value)}
                 className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:ring-1 focus:ring-blue-500 outline-none"
                 placeholder="Enter GitHub Repo URL..."
               />
               <button 
                 onClick={handleAnalyze}
                 disabled={isAnalyzing}
                 className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white text-xs font-bold rounded-lg transition-all shrink-0"
               >
                 {isAnalyzing ? "ANALYZING..." : "ANALYZE"}
               </button>
            </div>

            <button 
              onClick={() => setIsPrivate(!isPrivate)}
              className={clsx(
                "flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold transition-all border",
                isPrivate ? "bg-blue-500/10 border-blue-500 text-blue-400" : "bg-slate-800 border-slate-700 text-slate-400"
              )}
            >
              <Shield size={14} className={isPrivate ? "text-blue-500" : "text-slate-500"} />
              {isPrivate ? "PRIVATE" : "PUBLIC"}
            </button>
            <button 
              onClick={() => setIsDebugEnabled(!isDebugEnabled)}
              className={clsx(
                "flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold transition-all border",
                isDebugEnabled ? "bg-amber-500/10 border-amber-500 text-amber-400" : "bg-slate-800 border-slate-700 text-slate-400"
              )}
            >
              <Activity size={14} className={isDebugEnabled ? "text-amber-500" : "text-slate-500"} />
              DEBUG
            </button>
          </div>
          <div className="flex items-center gap-3">
             <div className="relative group">
                <input 
                  ref={searchInputRef}
                  type="text" 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search entities..." 
                  className="w-64 bg-slate-900/80 border border-slate-800 rounded-full px-5 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500/40 transition-all"
                />
                <kbd className="absolute right-3 top-1/2 -translate-y-1/2 px-1.5 py-0.5 rounded border border-slate-700 bg-slate-800 text-[10px] text-slate-500 font-mono pointer-events-none">⌘K</kbd>
             </div>
          </div>
        </header>

        {/* Viewport (Diagram) */}
        <div className="flex-1 relative bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-slate-900/20 via-slate-950 to-slate-950">
          <AuthGate 
            repoUrl={repoUrl} 
            isPrivate={isPrivate} 
            authToken={authToken}
            onAuthSuccess={(token) => setAuthToken(token)}
          >
            <ArchitectureMap 
              key={graphKey}
              searchQuery={searchQuery}
              onNodeClick={(nodeId: string, data: any) => {
                setSelectedNodeId(nodeId);
                setSelectedNodeData(data);
              }} 
            />
          </AuthGate>

          {/* Chat Toggle Button */}
          {!isChatOpen && (
            <button 
              onClick={() => setIsChatOpen(true)}
              className="absolute bottom-8 right-8 w-14 h-14 bg-blue-600 hover:bg-blue-500 text-white rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(37,99,235,0.4)] transition-all transform hover:scale-110 active:scale-95 z-40"
            >
              <MessageSquare size={24} />
            </button>
          )}

          {/* Chat Overlay */}
          {isChatOpen && <ChatOverlay repoUrl={repoUrl} persona={persona} onClose={() => setIsChatOpen(false)} />}
        </div>
      </div>

      {/* Right Sidebar (Explanation) */}
      <ExplanationPanel 
        entityName={selectedNodeData?.name || "Select a node"}
        type={selectedNodeData?.type || "Metadata"}
        lineCount={selectedNodeData ? ((selectedNodeData.line_end ?? 0) - (selectedNodeData.line_start ?? 0) + 1) : 0}
        purpose={summaryData?.summary}
        keyFunctions={summaryData?.key_functions}
        dependencies={summaryData?.dependencies}
        selectedNodeId={selectedNodeId}
        isLoading={isLoadingSummary}
        persona={persona}
        setPersona={setPersona}
        verbosity={verbosity}
        setVerbosity={setVerbosity}
        isDebugEnabled={isDebugEnabled}
        onTrace={handleTrace}
      />

      {/* Trace Modal */}
      {activeTrace && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-8 bg-slate-950/90 backdrop-blur-xl">
          <div className="bg-slate-900 border border-slate-700 w-full max-w-4xl max-h-[80vh] rounded-3xl overflow-hidden flex flex-col shadow-2xl">
            <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
              <div>
                <h3 className="text-white font-bold text-lg flex items-center gap-2">
                  <Activity className="text-blue-500" size={20} />
                  Execution Trace: {activeTrace.nodeId.split(':').pop()}
                </h3>
                <p className="text-xs text-slate-500 font-medium mt-1">Found {activeTrace.nodes.length} connected nodes in path</p>
              </div>
              <button 
                onClick={() => setActiveTrace(null)}
                className="w-10 h-10 rounded-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition-all"
              >✕</button>
            </div>
            <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
              {activeTrace.nodes.map((node: any, idx: number) => (
                <div key={idx} className="flex gap-4 group">
                  <div className="flex flex-col items-center">
                    <div className="w-8 h-8 rounded-full bg-blue-500/20 border border-blue-500/40 text-blue-400 flex items-center justify-center text-xs font-bold">{idx + 1}</div>
                    {idx < activeTrace.nodes.length - 1 && <div className="w-0.5 flex-1 bg-slate-800 my-1" />}
                  </div>
                  <div className="flex-1 pb-6">
                    <div className="bg-slate-800/40 p-4 rounded-2xl border border-slate-800 hover:border-blue-500/30 transition-all">
                      <div className="flex justify-between items-start mb-2">
                        <span className="text-sm font-bold text-white uppercase tracking-tight">{node.name}</span>
                        <span className="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-bold text-slate-500 border border-slate-700 uppercase">{node.type}</span>
                      </div>
                      <p className="text-xs text-slate-400 line-clamp-2 italic">{node.summary || "No description available for this step."}</p>
                      <div className="mt-3 flex items-center gap-2 text-[10px] font-mono text-slate-500">
                        <Layers size={10} />
                        <span>{node.path}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="p-6 border-t border-slate-800 bg-slate-900/50 flex justify-end gap-3">
              <button 
                onClick={() => setActiveTrace(null)}
                className="px-6 py-2.5 bg-slate-800 hover:bg-slate-700 text-white text-sm font-bold rounded-xl transition-all"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
