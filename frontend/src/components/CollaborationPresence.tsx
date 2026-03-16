"use client";

import React from 'react';
import { clsx } from 'clsx';

const MOCK_USERS = [
  { id: 'u1', name: 'Jane Architect', color: 'bg-emerald-500', initial: 'J' },
  { id: 'u2', name: 'Bob Dev', color: 'bg-amber-500', initial: 'B' },
  { id: 'u3', name: 'Alice Sec', color: 'bg-violet-500', initial: 'A' },
];

export const CollaborationPresence = () => {
  return (
    <div className="flex -space-x-2 overflow-hidden items-center group cursor-pointer p-2 rounded-full hover:bg-slate-800/40 transition-colors">
      {MOCK_USERS.map((user) => (
        <div 
          key={user.id}
          title={user.name}
          className={clsx(
            "inline-block h-8 w-8 rounded-full ring-2 ring-slate-950 flex items-center justify-center text-[10px] font-bold text-white transition-transform hover:-translate-y-1",
            user.color
          )}
        >
          {user.initial}
        </div>
      ))}
      <div className="ml-4 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col">
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest whitespace-nowrap">Collaborative Mode</span>
        <span className="text-[8px] text-emerald-400 font-medium">3 active users</span>
      </div>
    </div>
  );
};
