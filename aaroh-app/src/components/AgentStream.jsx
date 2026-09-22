import React from 'react';
import { CheckCircle2, Circle, Clock, Terminal, AlertTriangle, ShieldCheck, Cpu, Database, BarChart3, FileText, Sparkles } from 'lucide-react';

export default function AgentStream({ stages = [], activeStage = null, isStreaming = false, logs = [] }) {
  const stageDefinitions = [
    {
      id: 'data_ingestion',
      name: 'Data Ingestion & QC Agent',
      desc: 'Validating 22 acoustic features & signal SNR bounds',
      icon: Database,
    },
    {
      id: 'classical_inference',
      name: 'Classical Inference Agent',
      desc: 'XGBoost gradient-boosted decision trees evaluation',
      icon: BarChart3,
    },
    {
      id: 'quantum_encoding',
      name: 'Quantum Encoding Agent',
      desc: '4D PCA reduction & 4-qubit Hilbert statevector evaluation',
      icon: Cpu,
    },
    {
      id: 'hybrid_fusion',
      name: 'Hybrid Consensus Fusion Agent',
      desc: 'Applying 0.31 Classical + 0.69 Quantum weights & discordance check',
      icon: ShieldCheck,
    },
    {
      id: 'explainability_synthesis',
      name: 'Explainability Synthesis Agent',
      desc: 'Exact TreeSHAP attribution & acoustic biomarker ranking',
      icon: Sparkles,
    },
    {
      id: 'clinical_memo',
      name: 'Clinical Memo & Action Agent',
      desc: 'ICD-10 coding (G20/R47.81) & formal consultation report synthesis',
      icon: FileText,
    },
  ];

  return (
    <div className="card-clean p-5 hover:shadow-md transition-shadow">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
            <Terminal className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-slate-900 text-sm">Deterministic 6-Stage Agent Pipeline</h3>
            <p className="text-xs text-slate-500">Real-time Server-Sent Events (SSE) Execution Log</p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono">
          {isStreaming ? (
            <span className="flex items-center space-x-1.5 text-teal-600 font-semibold px-2.5 py-1 bg-teal-50 rounded-full border border-teal-200">
              <span className="w-2 h-2 rounded-full bg-teal-500 animate-ping" />
              <span>Streaming Live</span>
            </span>
          ) : (
            <span className="text-slate-500 px-2.5 py-1 bg-slate-100 rounded-full border border-slate-200">
              Pipeline Ready
            </span>
          )}
        </div>
      </div>

      {/* Stage Flow Grid */}
      <div className="space-y-2.5">
        {stageDefinitions.map((def, idx) => {
          const isDone = stages.some(s => s.stage === def.id && s.status === 'COMPLETED' || s.status === 'VALIDATED' || s.status === 'COMPUTED' || s.status === 'FUSED');
          const isRunning = activeStage === def.id;
          const stageData = stages.find(s => s.stage === def.id);
          const IconComponent = def.icon;

          return (
            <div
              key={def.id}
              className={`p-3 rounded-xl border transition-all ${
                isRunning
                  ? 'bg-teal-50/80 border-teal-400 shadow-xs'
                  : isDone
                  ? 'bg-white border-slate-200'
                  : 'bg-slate-50/60 border-slate-100 opacity-60'
              }`}
            >
              <div className="flex items-center justify-between">
                
                {/* Left: Icon & Title */}
                <div className="flex items-center space-x-3">
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold ${
                    isDone
                      ? 'bg-emerald-100 text-emerald-700'
                      : isRunning
                      ? 'bg-teal-600 text-white animate-pulse'
                      : 'bg-slate-200 text-slate-500'
                  }`}>
                    {isDone ? <CheckCircle2 className="w-4 h-4" /> : <IconComponent className="w-3.5 h-3.5" />}
                  </div>

                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-bold text-slate-900">
                        {idx + 1}. {def.name}
                      </span>
                      {stageData?.latency_ms && (
                        <span className="text-[10px] font-mono text-slate-400 bg-slate-100 px-1.5 py-0.2 rounded">
                          {stageData.latency_ms}ms
                        </span>
                      )}
                    </div>
                    <p className="text-[11px] text-slate-500 line-clamp-1">{def.desc}</p>
                  </div>
                </div>

                {/* Right Status Badge */}
                <div>
                  {isDone ? (
                    <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-md">
                      Done
                    </span>
                  ) : isRunning ? (
                    <span className="text-[11px] font-semibold text-teal-700 bg-teal-100 border border-teal-300 px-2 py-0.5 rounded-md animate-pulse">
                      Running...
                    </span>
                  ) : (
                    <span className="text-[11px] font-medium text-slate-400">
                      Queued
                    </span>
                  )}
                </div>

              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
}
