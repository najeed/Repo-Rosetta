"use client";

import React, { useState } from 'react';
import { ArchitectureMap } from '@/components/ArchitectureMap';
import { ExplanationPanel } from '@/components/ExplanationPanel';
import { AuthGate } from '@/components/AuthGate';
import { ChatOverlay } from '@/components/ChatOverlay';
import { Search, Github, Menu, Settings as SettingsIcon, Shield, MessageSquare } from 'lucide-react';
import { clsx } from 'clsx';

export default function Home() {
  const [persona, setPersona] = useState('senior-engineer');
  const [verbosity, setVerbosity] = useState('standard');
  const [isPanelOpen, setIsPanelOpen] = useState(true);
  const [isPrivate, setIsPrivate] = useState(false);
  const [repoUrl, setRepoUrl] = useState('fastapi / fastapi');
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <main className="flex h-screen w-full bg-slate-950 overflow-hidden font-sans selection:bg-blue-500/30">
      {/* Sidebar / Navigation (Mini) */}
      <div className="w-16 h-full bg-slate-900 border-r border-slate-800 flex flex-col items-center py-6 gap-8 z-20">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-violet-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Github className="text-white" size={24} />
        </div>
        <div className="flex-1 flex flex-col gap-6">
          <button className="p-2 text-slate-400 hover:text-white transition-colors">
            <Menu size={24} />
          </button>
          <button className="p-2 text-slate-400 hover:text-white transition-colors">
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
          <div className="flex items-center gap-4">
            <h1 className="text-lg font-bold text-white tracking-tight">Repo Rosetta</h1>
            <div className="h-4 w-px bg-slate-800" />
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
            <span className="text-sm font-medium text-slate-400">{repoUrl}</span>
          </div>
          <div className="flex items-center gap-3">
             <div className="relative group">
                <input 
                  type="text" 
                  placeholder="Ask a question about this repo..." 
                  className="w-80 bg-slate-900/80 border border-slate-800 rounded-full px-5 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500/40 transition-all"
                />
                <kbd className="absolute right-3 top-1/2 -translate-y-1/2 px-1.5 py-0.5 rounded border border-slate-700 bg-slate-800 text-[10px] text-slate-500 font-mono pointer-events-none">⌘K</kbd>
             </div>
          </div>
        </header>

        {/* Viewport (Diagram) */}
        <div className="flex-1 relative bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-slate-900/20 via-slate-950 to-slate-950">
          <AuthGate repoUrl={repoUrl} isPrivate={isPrivate}>
            <ArchitectureMap />
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
          {isChatOpen && <ChatOverlay onClose={() => setIsChatOpen(false)} />}
        </div>
      </div>

      {/* Right Sidebar (Explanation) */}
      <ExplanationPanel 
        persona={persona}
        setPersona={setPersona}
        verbosity={verbosity}
        setVerbosity={setVerbosity}
      />
    </main>
  );
}
