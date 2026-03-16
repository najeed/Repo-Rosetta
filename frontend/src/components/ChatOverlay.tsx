"use client";

import React, { useState } from 'react';
import { Send, X, Bot, User } from 'lucide-react';
import { clsx } from 'clsx';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

export const ChatOverlay = ({ onClose }: { onClose: () => void }) => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', role: 'assistant', content: 'Hello! I am your Rosetta AI. Ask me anything about the codebase.' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    // Mock API call
    setTimeout(() => {
      const assistantMsg: Message = { 
        id: (Date.now() + 1).toString(), 
        role: 'assistant', 
        content: `I analyzed the repository for your query: "${input}". Based on the graph, this functionality is primarily implemented in the core modules.` 
      };
      setMessages(prev => [...prev, assistantMsg]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="absolute bottom-12 right-12 w-96 h-[500px] bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl flex flex-col z-50 overflow-hidden ring-1 ring-white/5 backdrop-blur-xl">
      {/* Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/50">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
            <Bot size={18} className="text-blue-400" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Interactive Reasoning</h3>
            <p className="text-[10px] text-slate-500 font-medium">Repo Rosetta V3</p>
          </div>
        </div>
        <button onClick={onClose} className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-400 transition-colors">
          <X size={18} />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide">
        {messages.map((msg) => (
          <div key={msg.id} className={clsx(
            "flex gap-3 max-w-[85%]",
            msg.role === 'user' ? "ml-auto flex-row-reverse" : "mr-auto"
          )}>
            <div className={clsx(
              "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
              msg.role === 'user' ? "bg-slate-800" : "bg-blue-600 shadow-lg shadow-blue-500/20"
            )}>
              {msg.role === 'user' ? <User size={14} className="text-slate-400" /> : <Bot size={14} className="text-white" />}
            </div>
            <div className={clsx(
              "p-3 rounded-2xl text-sm leading-relaxed",
              msg.role === 'user' ? "bg-slate-800 text-slate-100 rounded-tr-none" : "bg-slate-700/50 text-slate-200 rounded-tl-none border border-slate-700/30"
            )}>
              {msg.content}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex gap-3 mr-auto items-baseline">
             <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center shrink-0">
                <Bot size={14} className="text-white" />
             </div>
             <div className="p-3 rounded-2xl bg-slate-700/50 text-slate-400 flex gap-1 h-10 items-center px-4 rounded-tl-none">
                <span className="w-1 h-1 bg-slate-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
                <span className="w-1 h-1 bg-slate-500 rounded-full animate-bounce [animation-delay:-0.15s]" />
                <span className="w-1 h-1 bg-slate-500 rounded-full animate-bounce" />
             </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-slate-800 bg-slate-900/50">
        <div className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask Rosetta about the code..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all pr-12"
          />
          <button 
            onClick={sendMessage}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors shadow-lg shadow-blue-500/20"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};
