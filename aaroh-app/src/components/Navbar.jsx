import React from 'react';
import { Activity, Shield, Sparkles, BarChart2, CheckCircle, AlertCircle } from 'lucide-react';

export default function Navbar({
  selectedPresetId,
  presets,
  onSelectPreset,
  onRunAnalysis,
  isAnalyzing,
  onOpenMetrics,
  activeTab,
  setActiveTab,
  backendStatus = "online"
}) {
  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Title */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-600 to-teal-400 flex items-center justify-center text-white shadow-md shadow-teal-500/20">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-heading font-extrabold text-xl tracking-tight text-slate-900">AAROH</span>
                <span className="px-2 py-0.5 text-xs font-semibold bg-teal-50 text-teal-700 border border-teal-200 rounded-full">
                  v2.0 Parkinson's CDSS
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium hidden sm:block">
                Multimodal Hybrid Classical–Quantum Early Screening Platform
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex items-center space-x-1 bg-slate-100 p-1 rounded-xl border border-slate-200 text-sm">
            <button
              onClick={() => setActiveTab('screening')}
              className={`px-3.5 py-1.5 rounded-lg font-medium transition-all ${
                activeTab === 'screening'
                  ? 'bg-white text-teal-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Screening & Telemetry
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`px-3.5 py-1.5 rounded-lg font-medium transition-all ${
                activeTab === 'history'
                  ? 'bg-white text-teal-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Longitudinal History
            </button>
            <button
              onClick={() => setActiveTab('memo')}
              className={`px-3.5 py-1.5 rounded-lg font-medium transition-all ${
                activeTab === 'memo'
                  ? 'bg-white text-teal-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Clinical Memo
            </button>
          </nav>

          {/* Right Controls: Preset Selector, Backend Status, Benchmark Button, Analyze CTA */}
          <div className="flex items-center space-x-3">
            
            {/* Backend Online Status Dot */}
            <div className="hidden lg:flex items-center space-x-1.5 px-2.5 py-1 bg-slate-100 rounded-full border border-slate-200 text-xs text-slate-600">
              <span className={`w-2 h-2 rounded-full ${backendStatus === 'online' ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`}></span>
              <span>{backendStatus === 'online' ? 'API Online' : 'Offline'}</span>
            </div>

            {/* Model Comparison / Metrics Modal trigger */}
            <button
              onClick={onOpenMetrics}
              className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg border border-slate-300 transition-colors"
              title="View multi-model benchmarks (XGBoost, VQC, Hybrid)"
            >
              <BarChart2 className="w-3.5 h-3.5 text-teal-600" />
              <span className="hidden sm:inline">Benchmark Table</span>
            </button>

            {/* Analyze Action Button */}
            <button
              onClick={onRunAnalysis}
              disabled={isAnalyzing}
              className="flex items-center space-x-2 px-4 py-2 text-sm font-semibold text-white bg-gradient-to-r from-teal-600 to-teal-500 hover:from-teal-700 hover:to-teal-600 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl shadow-md shadow-teal-600/20 transition-all"
            >
              {isAnalyzing ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Orchestrating...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-teal-100" />
                  <span>Run Screening</span>
                </>
              )}
            </button>
          </div>

        </div>
      </div>
    </header>
  );
}
