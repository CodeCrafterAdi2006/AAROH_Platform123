import React from 'react';
import { Cpu, Zap, Activity, Radio, Scale, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function QuantumEngineCard({
  quantumTelemetry = {},
  classicalScore = 0.0,
  quantumScore = 0.0,
  hybridScore = 0.0,
  alpha = 0.31,
  beta = 0.69,
  consensusStatus = "CONCORDANT",
  isAnalyzing = false
}) {
  const angles = quantumTelemetry.quantum_angles_rad || [1.42, 0.85, 2.15, 0.64];
  const ev = quantumTelemetry.expectation_value ?? -0.1238;
  const backend = quantumTelemetry.backend || "Qiskit Aer / Statevector";
  const latency = quantumTelemetry.latency_ms ?? 9.8;
  const isDiscordant = consensusStatus === "DISCORDANT_REVIEW";

  return (
    <div className="engine-dark p-5 rounded-2xl relative overflow-hidden border border-teal-500/30">
      
      {/* Background Subtle Gradient Glow */}
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-teal-950 text-teal-400 flex items-center justify-center border border-teal-800">
            <Cpu className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-heading font-bold text-white text-sm">4-Qubit Variational Quantum Engine (VQC)</h3>
              <span className="px-1.5 py-0.5 text-[10px] font-mono bg-teal-900/50 text-teal-300 border border-teal-700/50 rounded">
                Hilbert Space (2⁴=16 Dim)
              </span>
            </div>
            <p className="text-xs text-slate-400">ZZFeatureMap (reps=1) + RealAmplitudes Ansatz (8θ)</p>
          </div>
        </div>

        {/* Discordance / Concordance Pill */}
        <div className={`px-2.5 py-1 rounded-full text-xs font-semibold flex items-center space-x-1.5 ${
          isDiscordant
            ? 'bg-amber-950/80 text-amber-300 border border-amber-700/50'
            : 'bg-teal-950/80 text-teal-300 border border-teal-700/50'
        }`}>
          {isDiscordant ? (
            <>
              <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
              <span>Discordance Flagged</span>
            </>
          ) : (
            <>
              <CheckCircle2 className="w-3.5 h-3.5 text-teal-400" />
              <span>Concordant Output</span>
            </>
          )}
        </div>
      </div>

      {/* 4 Qubit Orbital State Indicators */}
      <div className="grid grid-cols-4 gap-3 mb-4">
        {angles.map((angle, idx) => (
          <div
            key={idx}
            className="bg-slate-900/80 border border-slate-800 rounded-xl p-3 text-center relative overflow-hidden group hover:border-teal-500/50 transition-colors"
          >
            {/* Pulsing animation when running */}
            <div className={`w-3 h-3 rounded-full mx-auto mb-1.5 ${
              isAnalyzing ? 'bg-teal-400 animate-ping' : 'bg-teal-500 shadow-xs shadow-teal-400/50'
            }`} />

            <span className="text-[11px] font-mono font-bold text-slate-300 block">q[{idx}]</span>
            <span className="text-xs font-mono font-semibold text-teal-300 block mt-0.5">
              {typeof angle === 'number' ? angle.toFixed(3) : '0.000'} rad
            </span>
            <span className="text-[9px] text-slate-500 block mt-0.5">
              θ = {(angle * 180 / Math.PI).toFixed(0)}°
            </span>
          </div>
        ))}
      </div>

      {/* Tri-Model Fusion Telemetry Strip */}
      <div className="bg-slate-950/80 border border-slate-800/80 rounded-xl p-3.5 mb-3">
        <div className="grid grid-cols-3 gap-3 text-center">
          
          <div className="border-r border-slate-800 pr-2">
            <span className="text-[11px] text-slate-400 block mb-1">Classical (XGBoost)</span>
            <span className="text-base font-bold font-mono text-slate-100">
              {(classicalScore * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] text-slate-500 block mt-0.5">Weight α = {alpha}</span>
          </div>

          <div className="border-r border-slate-800 pr-2">
            <span className="text-[11px] text-slate-400 block mb-1">Quantum (VQC)</span>
            <span className="text-base font-bold font-mono text-teal-300">
              {(quantumScore * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] text-slate-500 block mt-0.5">Weight β = {beta}</span>
          </div>

          <div>
            <span className="text-[11px] text-slate-400 block mb-1">Hybrid Score (P_h)</span>
            <span className={`text-base font-bold font-mono ${hybridScore >= 0.65 ? 'text-rose-400' : hybridScore >= 0.45 ? 'text-amber-400' : 'text-emerald-400'}`}>
              {(hybridScore * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] text-teal-400/80 block mt-0.5">Optimal Late Fusion</span>
          </div>

        </div>
      </div>

      {/* Telemetry Footer */}
      <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono pt-1">
        <span className="flex items-center space-x-1.5">
          <Radio className="w-3 h-3 text-teal-400" />
          <span>Backend: {backend}</span>
        </span>
        <span>Expectation ⟨IIIZ⟩: <strong className="text-slate-200">{typeof ev === 'number' ? ev.toFixed(4) : '0.000'}</strong></span>
        <span>Latency: <strong className="text-slate-200">{latency}ms</strong></span>
      </div>

    </div>
  );
}
