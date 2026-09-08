import React, { useState } from 'react';
import { 
  ShieldCheck, Cpu, AlertCircle, Info, ChevronDown, ChevronUp,
  Activity, ArrowRight, CheckCircle2, AlertTriangle, Layers
} from 'lucide-react';

export default function ModelComparison({
  classicalResult,
  quantumResult,
  memoData,
  benchmarks
}) {
  const [showCircuit, setShowCircuit] = useState(false);

  if (!classicalResult || !quantumResult) {
    return (
      <div className="glass-panel rounded-2xl p-8 border border-slate-800 text-center text-slate-500">
        <Activity className="w-10 h-10 mx-auto mb-3 opacity-30 text-cyan-400" />
        <p className="text-sm">Run the diagnostic pipeline above to generate dual-model comparative benchmarking.</p>
      </div>
    );
  }

  const xgbProb = classicalResult.probability_malignant;
  const xgbIsMalignant = xgbProb >= 0.5;

  const vqcProb = quantumResult.vqc_probability;
  const vqcIsMalignant = vqcProb >= 0.5;
  const vqcEv = quantumResult.expectation_value;

  const isConcordant = xgbIsMalignant === vqcIsMalignant;

  return (
    <div className="glass-panel rounded-2xl p-5 lg:p-6 border border-slate-800 flex flex-col gap-5">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white flex items-center gap-2">
              Dual-Model Benchmarking & Inference
              <span className={`text-[11px] font-mono font-medium px-2 py-0.5 rounded border ${
                isConcordant 
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                  : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
              }`}>
                {isConcordant ? 'CONCORDANT PREDICTION' : 'DISCORDANCE (FLAGGED)'}
              </span>
            </h2>
            <p className="text-xs text-slate-400">
              Synchronized inference comparing classical gradient boosting with a 4-qubit variational quantum circuit.
            </p>
          </div>
        </div>

        {/* Circuit toggle */}
        <button
          onClick={() => setShowCircuit(!showCircuit)}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-xs font-mono text-cyan-300 border border-slate-800 transition-all self-start sm:self-auto"
        >
          <Cpu className="w-3.5 h-3.5 text-cyan-400" />
          <span>{showCircuit ? 'Hide Circuit Wire' : 'View 4-Qubit Circuit'}</span>
          {showCircuit ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </button>
      </div>

      {/* Side-by-Side Model Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        
        {/* ========================================================================= */}
        {/* 1. Classical XGBoost Card */}
        {/* ========================================================================= */}
        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col justify-between gap-4">
          <div>
            {/* Title & Badge */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="p-1.5 rounded-md bg-indigo-500/20 text-indigo-400">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">Classical XGBoost Engine</h3>
                  <span className="text-[10px] text-slate-400 font-mono">Gradient Boosted Decision Trees</span>
                </div>
              </div>
              <span className={`text-xs font-bold font-mono px-2.5 py-1 rounded-md border ${
                xgbIsMalignant 
                  ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                  : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
              }`}>
                {xgbIsMalignant ? 'MALIGNANT' : 'BENIGN'}
              </span>
            </div>

            {/* Probability Gauge */}
            <div className="mb-4">
              <div className="flex items-baseline justify-between text-xs mb-1.5">
                <span className="text-slate-400">Probability of Malignancy:</span>
                <span className="font-mono text-base font-bold text-white">
                  {(xgbProb * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                <div 
                  className={`h-full transition-all duration-500 ${
                    xgbProb >= 0.5 
                      ? 'bg-gradient-to-r from-amber-500 to-rose-500'
                      : 'bg-gradient-to-r from-teal-500 to-emerald-400'
                  }`}
                  style={{ width: `${Math.max(xgbProb * 100, 2)}%` }}
                />
              </div>
            </div>

            {/* Metrics Breakdown */}
            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80">
                <span className="text-[10px] text-slate-500 block uppercase">Log-Odds Margin</span>
                <span className="text-sm font-semibold text-slate-200">
                  {classicalResult.output_margin > 0 ? '+' : ''}{classicalResult.output_margin.toFixed(3)}
                </span>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80">
                <span className="text-[10px] text-slate-500 block uppercase">TreeSHAP Base</span>
                <span className="text-sm font-semibold text-slate-200">
                  {classicalResult.base_value.toFixed(3)}
                </span>
              </div>
            </div>
          </div>

          {/* CV Baseline Label */}
          <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>5-Fold Stratified CV:</span>
            <strong className="text-indigo-300 font-semibold">0.994 ± 0.004 ROC-AUC</strong>
          </div>
        </div>

        {/* ========================================================================= */}
        {/* 2. Quantum VQC Card */}
        {/* ========================================================================= */}
        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col justify-between gap-4">
          <div>
            {/* Title & Badge */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="p-1.5 rounded-md bg-cyan-500/20 text-cyan-400">
                  <Cpu className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">4-Qubit Quantum VQC</h3>
                  <span className="text-[10px] text-cyan-400/80 font-mono">
                    {quantumResult.backend || 'Qiskit Aer'} ({quantumResult.routing || 'Primary'})
                  </span>
                </div>
              </div>
              <span className={`text-xs font-bold font-mono px-2.5 py-1 rounded-md border ${
                vqcIsMalignant 
                  ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                  : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
              }`}>
                {vqcIsMalignant ? 'MALIGNANT' : 'BENIGN'}
              </span>
            </div>

            {/* Probability Gauge */}
            <div className="mb-4">
              <div className="flex items-baseline justify-between text-xs mb-1.5">
                <span className="text-slate-400">Quantum State Probability:</span>
                <span className="font-mono text-base font-bold text-cyan-300">
                  {(vqcProb * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                <div 
                  className={`h-full transition-all duration-500 ${
                    vqcProb >= 0.5 
                      ? 'bg-gradient-to-r from-amber-500 to-rose-500'
                      : 'bg-gradient-to-r from-cyan-500 to-teal-400'
                  }`}
                  style={{ width: `${Math.max(vqcProb * 100, 2)}%` }}
                />
              </div>
            </div>

            {/* Quantum Math Breakdown */}
            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80">
                <span className="text-[10px] text-slate-500 block uppercase">Observable &lt;IIIZ&gt;</span>
                <span className="text-sm font-semibold text-cyan-300">
                  {vqcEv > 0 ? '+' : ''}{vqcEv.toFixed(4)}
                </span>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80">
                <span className="text-[10px] text-slate-500 block uppercase">PCA Dimension</span>
                <span className="text-sm font-semibold text-slate-200">
                  30D ➔ 4 Qubits
                </span>
              </div>
            </div>
          </div>

          {/* Test Split Baseline Label */}
          <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>Held-out 80/20 Test Split:</span>
            <strong className="text-cyan-300 font-semibold">0.748 ROC-AUC</strong>
          </div>
        </div>

      </div>

      {/* 4-Qubit Circuit Wire Representation (Collapsible) */}
      {showCircuit && (
        <div className="p-4 rounded-xl bg-slate-950 border border-cyan-900/40 font-mono text-xs animate-in fade-in duration-200">
          <div className="flex items-center justify-between mb-3 text-slate-300 text-[11px] font-semibold uppercase tracking-wider">
            <span className="flex items-center gap-1.5 text-cyan-400">
              <Cpu className="w-3.5 h-3.5" />
              4-Qubit Circuit Architecture: ZZFeatureMap (reps=1) ➔ RealAmplitudes (reps=1)
            </span>
            <span className="text-slate-500">8 Tuned Variational Parameters</span>
          </div>

          <div className="space-y-2 py-2 text-slate-300 text-xs overflow-x-auto">
            {['q₀', 'q₁', 'q₂', 'q₃'].map((qubit, qIdx) => {
              const angle = quantumResult.quantum_angles_rad?.[qIdx] || 0;
              return (
                <div key={qubit} className="flex items-center gap-2 whitespace-nowrap min-w-[500px]">
                  <span className="text-cyan-400 font-bold w-6">{qubit}</span>
                  <span className="text-slate-600">|0⟩─</span>
                  <span className="px-2 py-0.5 rounded bg-indigo-950 border border-indigo-700 text-indigo-300 text-[10px]">H</span>
                  <span className="text-slate-600">─</span>
                  <span className="px-2 py-0.5 rounded bg-cyan-950 border border-cyan-700 text-cyan-300 text-[10px]" title={`Angle: ${angle.toFixed(4)} rad`}>
                    Rz(φ_{qIdx}={angle.toFixed(2)})
                  </span>
                  <span className="text-slate-600">─●─</span>
                  <span className="px-2 py-0.5 rounded bg-purple-950 border border-purple-700 text-purple-300 text-[10px]">
                    Ry(θ_{qIdx})
                  </span>
                  <span className="text-slate-600">─</span>
                  {qIdx === 0 ? (
                    <span className="px-2 py-0.5 rounded bg-rose-950 border border-rose-700 text-rose-300 text-[10px] font-bold">
                      ⟨Z⟩ Measure
                    </span>
                  ) : (
                    <span className="text-slate-600">───────────</span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* The Honest Asymmetry Protocol Callout */}
      <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs flex items-start gap-3">
        <Info className="w-4 h-4 text-cyan-400 mt-0.5 flex-shrink-0" />
        <div className="text-slate-300 leading-relaxed text-[11px]">
          <strong className="text-white font-semibold block mb-0.5">
            Scientific Protocol & Evaluation Asymmetry Notice:
          </strong>
          Classical XGBoost is evaluated via 5-Fold Stratified Cross-Validation on all 569 WBCD samples (ROC-AUC 0.994 ± 0.004). 
          The 4-Qubit VQC is evaluated on a held-out 80/20 test split (n=114, ROC-AUC 0.748). 
          Direct numerical comparison reflects <em>quantum encoding viability on small-scale biological data</em>, not quantum supremacy over classical gradient boosting.
        </div>
      </div>

    </div>
  );
}
