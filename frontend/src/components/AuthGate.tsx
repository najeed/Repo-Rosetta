"use client";

import React, { useState, useEffect } from 'react';
import { Lock, Github, ShieldCheck, AlertCircle } from 'lucide-react';

interface AuthGateProps {
  children: React.ReactNode;
  repoUrl: string;
  isPrivate: boolean;
  onAuthSuccess?: (token: string) => void;
  authToken?: string | null;
}

export const AuthGate: React.FC<AuthGateProps> = ({ children, repoUrl, isPrivate, onAuthSuccess, authToken }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!authToken);
  const [loading, setLoading] = useState(isPrivate && !authToken);

  useEffect(() => {
    if (!isPrivate || authToken) {
      if (!isAuthenticated && (authToken || !isPrivate)) setIsAuthenticated(true);
      setLoading(false);
      return;
    }

    // Simulate session check
    const checkAuth = async () => {
      setLoading(true);
      setTimeout(() => {
        // Mock: user is not authenticated yet
        setIsAuthenticated(false);
        setLoading(false);
      }, 1000);
    };

    checkAuth();
  }, [isPrivate, authToken]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4 text-slate-400">
        <div className="w-12 h-12 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin" />
        <p className="text-sm font-medium animate-pulse">Verifying repository permissions...</p>
      </div>
    );
  }

  if (isPrivate && !isAuthenticated) {
    return (
      <div className="flex items-center justify-center h-full bg-slate-950 px-6">
        <div className="max-w-md w-full p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl text-center">
          <div className="w-16 h-16 bg-blue-500/10 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <Lock className="text-blue-500" size={32} />
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">Private Repository</h2>
          <p className="text-slate-400 text-sm mb-8 leading-relaxed">
            Target repository <code className="text-blue-400">{repoUrl}</code> is private. 
            Authorization is required to proceed with architectural analysis.
          </p>
          
          <button 
            onClick={() => {
              setLoading(true);
              setTimeout(() => {
                setIsAuthenticated(true);
                setLoading(false);
                if (onAuthSuccess) onAuthSuccess("mock-codebase-token");
              }, 1500);
            }}
            disabled={loading}
            className="w-full flex items-center justify-center gap-3 py-3 px-6 rounded-xl bg-white hover:bg-slate-200 text-slate-950 font-bold transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-slate-900/20 border-t-slate-900 rounded-full animate-spin" />
            ) : (
              <Github size={20} />
            )}
            {loading ? "Authorizing..." : "Authorize with GitHub"}
          </button>
          
          <div className="mt-8 pt-6 border-t border-slate-800 grid grid-cols-2 gap-4">
            <div className="text-left">
              <div className="flex items-center gap-1.5 text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">
                <ShieldCheck size={14} className="text-emerald-500" />
                Secure
              </div>
              <p className="text-[10px] text-slate-500">Code never leaves your environment.</p>
            </div>
            <div className="text-left">
              <div className="flex items-center gap-1.5 text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">
                <AlertCircle size={14} className="text-blue-500" />
                Scoped
              </div>
              <p className="text-[10px] text-slate-500">Read-only access to this repository.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};
