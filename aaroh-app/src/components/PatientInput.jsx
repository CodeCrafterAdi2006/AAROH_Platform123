import React, { useState } from 'react';
import { 
  User, Database, Play, RefreshCw, ChevronDown, ChevronUp, 
  Sliders, ShieldAlert, CheckCircle2, AlertCircle, HelpCircle, ToggleLeft, ToggleRight
} from 'lucide-react';

export default function PatientInput({
  presets,
  selectedPresetId,
  onSelectPreset,
  patientFeatures,
  featureNames,
  onUpdateFeature,
  isStreaming,
  onRunDiagnosis,
  forceFallback,
  setForceFallback
}) {
  const [showAll30, setShowAll30] = useState(false);

  // Group features into Mean (0-9), SE (10-19), Worst (20-29)
  const primaryFeatures = patientFeatures.slice(0, 10);
  const seFeatures = patientFeatures.slice(10, 20);
  const worstFeatures = patientFeatures.slice(20, 30);

  const selectedPreset = presets.find(p => p.preset_id === selectedPresetId) || presets[0];

  return (
    <div className="glass-panel rounded-2xl p-5 lg:p-6 border border-slate-800 flex flex-col gap-5">
      
      {/* Section Header */}
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <User className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white flex items-center gap-2">
              Clinical Case & Biopsy Ingestion
              <span className="text-[11px] font-mono font-normal px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                WBCD 30D FNA
              </span>
            </h2>
            <p className="text-xs text-slate-400">
              Select an authentic benchmark patient or adjust fine-needle morphometry measurements.
            </p>
          </div>
        </div>

        {/* Fallback Switch */}
        <button
          onClick={() => setForceFallback(!forceFallback)}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-mono transition-all border ${
            forceFallback
              ? 'bg-amber-950/40 border-amber-600/50 text-amber-300'
              : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
          }`}
          title="Toggle pure NumPy matrix simulator vs Qiskit Aer"
        >
          {forceFallback ? (
            <ToggleRight className="w-4 h-4 text-amber-400" />
          ) : (
            <ToggleLeft className="w-4 h-4 text-slate-500" />
          )}
          <span>Fallback: {forceFallback ? 'FORCE NUMPY' : 'AUTO QISKIT'}</span>
        </button>
      </div>

      {/* Preset Selector Cards */}
      <div>
        <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2.5 block">
          Reference Benchmark Presets (Standardized WBCD)
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {presets.map((p) => {
            const isSelected = p.preset_id === selectedPresetId;
            const isMalignant = p.ground_truth === 'Malignant';
            const isBorderline = p.preset_id.includes('borderline');

            let badgeColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
            if (isMalignant) badgeColor = 'bg-rose-500/10 text-rose-400 border-rose-500/20';
            if (isBorderline) badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/20';

            return (
              <button
                key={p.preset_id}
                onClick={() => onSelectPreset(p.preset_id)}
                disabled={isStreaming}
                className={`flex flex-col text-left p-3.5 rounded-xl border transition-all relative overflow-hidden ${
                  isSelected
                    ? 'bg-slate-800/90 border-cyan-500 shadow-md shadow-cyan-500/10'
                    : 'bg-slate-900/50 border-slate-800 hover:border-slate-700 hover:bg-slate-800/40'
                } ${isStreaming ? 'opacity-60 cursor-not-allowed' : ''}`}
              >
                {isSelected && (
                  <div className="absolute top-0 right-0 w-12 h-12 overflow-hidden pointer-events-none">
                    <div className="bg-cyan-500 text-[9px] font-bold text-dark-bg py-0.5 text-center transform rotate-45 translate-x-3 -translate-y-1 w-16">
                      ACTIVE
                    </div>
                  </div>
                )}
                <div className="flex items-center justify-between mb-1.5 pr-4">
                  <span className="text-xs font-semibold text-white">{p.label}</span>
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-[10px] font-mono font-medium px-2 py-0.5 rounded border ${badgeColor}`}>
                    Truth: {p.ground_truth}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400">{p.patient_id}</span>
                </div>
                <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                  {p.description}
                </p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Primary Nuclear Biomarkers Preview */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            Primary Nuclear Biomarkers (Mean Values)
            <span className="text-[10px] font-normal text-slate-500">(10 of 30 Features)</span>
          </label>
          <button
            onClick={() => setShowAll30(!showAll30)}
            className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-medium transition-colors"
          >
            {showAll30 ? (
              <><span>Hide SE & Worst</span><ChevronUp className="w-3.5 h-3.5" /></>
            ) : (
              <><span>Inspect Full 30D Vector</span><ChevronDown className="w-3.5 h-3.5" /></>
            )}
          </button>
        </div>

        {/* 10 Primary Features Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
          {primaryFeatures.map((val, idx) => {
            const name = featureNames[idx] || `Feature ${idx+1}`;
            const cleanName = name.replace('mean ', '');
            return (
              <div 
                key={idx} 
                className="bg-slate-900/70 border border-slate-800 rounded-lg p-2.5 flex flex-col justify-between hover:border-slate-700 transition-all"
              >
                <span className="text-[11px] font-medium text-slate-400 capitalize truncate" title={name}>
                  {cleanName}
                </span>
                <div className="flex items-baseline justify-between mt-1">
                  <span className="text-sm font-mono font-semibold text-cyan-300">
                    {typeof val === 'number' ? val.toFixed(val > 10 ? 1 : 4) : val}
                  </span>
                  <span className="text-[10px] text-slate-500 font-mono">f_{idx}</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Expandable 20 Features (SE & Worst) */}
        {showAll30 && (
          <div className="mt-4 pt-4 border-t border-slate-800 flex flex-col gap-3 animate-in fade-in duration-200">
            <div>
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 block">
                Standard Error Biomarkers (Indices 10–19)
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
                {seFeatures.map((val, idx) => {
                  const trueIdx = idx + 10;
                  const name = (featureNames[trueIdx] || '').replace('error', 'SE');
                  return (
                    <div key={trueIdx} className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-2 text-xs">
                      <div className="text-[10px] text-slate-400 truncate capitalize">{name}</div>
                      <div className="font-mono text-slate-200 font-medium">{val.toFixed(val > 1 ? 2 : 4)}</div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div>
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 block">
                Worst / Extreme Nuclear Morphology (Indices 20–29)
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
                {worstFeatures.map((val, idx) => {
                  const trueIdx = idx + 20;
                  const name = (featureNames[trueIdx] || '').replace('worst', 'Worst');
                  return (
                    <div key={trueIdx} className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-2 text-xs">
                      <div className="text-[10px] text-slate-400 truncate capitalize">{name}</div>
                      <div className="font-mono text-cyan-400 font-medium">{val.toFixed(val > 10 ? 1 : 4)}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Trigger Execution Button */}
      <div className="pt-2 flex items-center justify-between gap-4">
        <div className="text-xs text-slate-400 flex items-center gap-1.5">
          <Database className="w-3.5 h-3.5 text-cyan-400" />
          <span>Case: <strong className="text-slate-200 font-mono">{selectedPreset.patient_id}</strong></span>
        </div>

        <button
          onClick={onRunDiagnosis}
          disabled={isStreaming}
          className={`flex items-center gap-2.5 px-6 py-3 rounded-xl font-semibold text-sm transition-all shadow-lg ${
            isStreaming
              ? 'bg-slate-800 text-cyan-300 border border-cyan-500/40 cursor-wait'
              : 'bg-gradient-to-r from-cyan-500 via-teal-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white shadow-cyan-500/25 hover:shadow-cyan-500/40 active:scale-98'
          }`}
        >
          {isStreaming ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin text-cyan-300" />
              <span>Orchestrating Live SSE Agents...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4 fill-white" />
              <span>Run Hybrid Diagnostic Pipeline</span>
            </>
          )}
        </button>
      </div>

    </div>
  );
}
