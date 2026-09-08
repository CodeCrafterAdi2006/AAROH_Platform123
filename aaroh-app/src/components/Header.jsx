import React from 'react';
import { Activity, Cpu, ShieldCheck, BarChart3, Database, FileText } from 'lucide-react';

export default function Header({ 
  backendOnline, 
  healthData, 
  onOpenMetrics, 
  onOpenMemo, 
  hasDiagnostic 
}) {
  return (
    <header className="no-print sticky top-0 z-40 w-full glass-panel border-b border-slate-800/80 px-4 lg:px-8 py-3.5 transition-all">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Brand & Subtitle */}
        <div className="flex items-center gap-3.5">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 text-white shadow-lg shadow-cyan-500/20">
            <Activity className="w-5 h-5 text-white" />
            <span className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-400 border-2 border-dark-bg rounded-full"></span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-1.5">
                AAROH
                <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 tracking-normal">
                  v2.0 Hybrid
                </span>
              </h1>
            </div>
            <p className="text-xs text-slate-400 font-medium">
              Hybrid Classical-Quantum Clinical Decision Support & Benchmarking
            </p>
          </div>
        </div>

        {/* Live Architecture Status Badges */}
        <div className="flex flex-wrap items-center gap-2.5">
          
          {/* Health status */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs">
            <span className={`w-2 h-2 rounded-full ${backendOnline ? 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]' : 'bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.8)] animate-pulse'}`}></span>
            <span className="text-slate-300 font-mono text-[11px]">
              API: {backendOnline ? 'ONLINE' : 'CONNECTING...'}
            </span>
          </div>

          {/* Engine indicator */}
          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-950/40 border border-cyan-800/40 text-cyan-300 text-xs font-medium">
            <Cpu className="w-3.5 h-3.5 text-cyan-400" />
            <span>4-Qubit VQC (ZZ-Map)</span>
          </div>

          {/* Classical indicator */}
          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-950/40 border border-indigo-800/40 text-indigo-300 text-xs font-medium">
            <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
            <span>XGBoost (5-Fold CV)</span>
          </div>

          {/* Metrics Modal Trigger */}
          <button
            onClick={onOpenMetrics}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium transition-all shadow-sm active:scale-95"
            title="View Empirical CV & Test Split Benchmark Comparisons"
          >
            <BarChart3 className="w-3.5 h-3.5 text-cyan-400" />
            <span>Benchmarks</span>
          </button>

          {/* Report Button (if diagnostic ready) */}
          {hasDiagnostic && (
            <button
              onClick={onOpenMemo}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-white text-xs font-medium transition-all shadow-md shadow-cyan-500/20 active:scale-95"
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Clinical Memo</span>
            </button>
          )}

        </div>

      </div>
    </header>
  );
}
