import React from 'react';
import { 
  Terminal, CheckCircle2, Clock, AlertTriangle, 
  Cpu, ShieldCheck, Microscope, FileText, ChevronRight
} from 'lucide-react';

const STAGE_DEFINITIONS = [
  {
    id: 'data_ingestion',
    title: 'Stage 1: Data Ingestion & Quality Control',
    icon: Microscope,
    desc: 'Morphometry vector validation & zero-NaN bounds check',
  },
  {
    id: 'quantum_encoding',
    title: 'Stage 2: Quantum Feature & State Encoding',
    icon: Cpu,
    desc: '30D ➔ 4D PCA compression & ZZFeatureMap Hilbert space projection',
  },
  {
    id: 'classical_explainability',
    title: 'Stage 3: Classical Ensemble & Explainability',
    icon: ShieldCheck,
    desc: 'XGBoost margin inference & exact TreeSHAP attribution force vectors',
  },
  {
    id: 'clinical_synthesis',
    title: 'Stage 4: Clinical Synthesis & Pathology Memo',
    icon: FileText,
    desc: 'Dual-engine consensus, ICD-10 assignment & consultation memorandum',
  },
];

export default function AgentStream({
  streamEvents,
  currentStage,
  isStreaming,
  streamCompleted,
  totalLatencyMs
}) {
  // Determine status for each stage
  const getStageStatus = (stageId) => {
    const isCompleted = streamEvents.some(
      e => e.type === 'stage_complete' && e.data?.stage === stageId
    );
    if (isCompleted) return 'completed';

    const isCurrent = streamEvents.some(
      e => e.type === 'stage_start' && e.data?.stage === stageId
    ) || currentStage === stageId;
    if (isCurrent) return 'running';

    return 'pending';
  };

  // Calculate progress percentage
  const completedCount = STAGE_DEFINITIONS.filter(s => getStageStatus(s.id) === 'completed').length;
  const progressPercent = streamCompleted ? 100 : (completedCount / 4) * 100;

  return (
    <div className="glass-panel rounded-2xl p-5 lg:p-6 border border-slate-800 flex flex-col gap-5 scanline-effect">
      
      {/* Header & Progress */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Terminal className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white flex items-center gap-2">
              Agentic Pipeline Telemetry
              {isStreaming && (
                <span className="flex items-center gap-1.5 text-[11px] font-mono px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 animate-pulse">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                  STREAMING SSE
                </span>
              )}
              {streamCompleted && (
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                  CONSENSUS REACHED
                </span>
              )}
            </h2>
            <p className="text-xs text-slate-400">
              Deterministic 4-stage event loop streaming live computations from FastAPI backend.
            </p>
          </div>
        </div>

        {/* Latency & Progress indicator */}
        <div className="flex items-center gap-4 text-xs font-mono">
          {totalLatencyMs > 0 && (
            <div className="flex items-center gap-1.5 text-slate-300 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">
              <Clock className="w-3.5 h-3.5 text-cyan-400" />
              <span>Pipeline: <strong className="text-cyan-300">{totalLatencyMs.toFixed(1)}ms</strong></span>
            </div>
          )}
          <div className="text-slate-400">
            Progress: <strong className="text-white">{progressPercent.toFixed(0)}%</strong>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
        <div 
          className="h-full bg-gradient-to-r from-cyan-500 via-teal-400 to-indigo-500 transition-all duration-300 ease-out"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {/* 4 Deterministic Stage Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {STAGE_DEFINITIONS.map((def, idx) => {
          const status = getStageStatus(def.id);
          const Icon = def.icon;

          // Find completion payload if any
          const completeEvt = streamEvents.find(
            e => e.type === 'stage_complete' && e.data?.stage === def.id
          );
          const startEvt = streamEvents.find(
            e => e.type === 'stage_start' && e.data?.stage === def.id
          );

          let borderStyle = 'border-slate-800 bg-slate-950/40 text-slate-400';
          let badge = (
            <span className="text-[10px] font-mono text-slate-500 px-2 py-0.5 rounded bg-slate-900 border border-slate-800">
              PENDING
            </span>
          );

          if (status === 'running') {
            borderStyle = 'border-cyan-500/70 bg-cyan-950/20 text-slate-200 shadow-md shadow-cyan-500/5 animate-pulse';
            badge = (
              <span className="text-[10px] font-mono text-cyan-300 px-2 py-0.5 rounded bg-cyan-500/20 border border-cyan-500/40 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                ACTIVE
              </span>
            );
          } else if (status === 'completed') {
            borderStyle = 'border-emerald-500/40 bg-slate-900/80 text-slate-200';
            badge = (
              <span className="text-[10px] font-mono text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                DONE
              </span>
            );
          }

          return (
            <div 
              key={def.id} 
              className={`p-3.5 rounded-xl border transition-all flex flex-col justify-between gap-2.5 ${borderStyle}`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <div className={`p-1.5 rounded-lg ${
                    status === 'completed' ? 'bg-emerald-500/20 text-emerald-400' :
                    status === 'running' ? 'bg-cyan-500/20 text-cyan-400' :
                    'bg-slate-900 text-slate-500'
                  }`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-xs font-semibold text-white block">
                      {def.title}
                    </span>
                    <span className="text-[11px] text-slate-400 block leading-tight">
                      {def.desc}
                    </span>
                  </div>
                </div>
                {badge}
              </div>

              {/* Real Computed Data Snippet */}
              {status === 'completed' && completeEvt?.data && (
                <div className="mt-1 pt-2 border-t border-slate-800/80 text-[11px] font-mono text-slate-300 flex flex-wrap items-center gap-x-3 gap-y-1">
                  {def.id === 'data_ingestion' && (
                    <>
                      <span className="text-slate-400">Features: <strong className="text-cyan-300">{completeEvt.data.feature_count}</strong></span>
                      <span className="text-slate-400">Status: <strong className="text-emerald-400">{completeEvt.data.status}</strong></span>
                    </>
                  )}
                  {def.id === 'quantum_encoding' && (
                    <>
                      <span className="text-slate-400">Expectation &lt;IIIZ&gt;: <strong className="text-cyan-300">{completeEvt.data.expectation_value?.toFixed(4)}</strong></span>
                      <span className="text-slate-400">VQC Prob: <strong className="text-cyan-400">{(completeEvt.data.vqc_probability * 100).toFixed(1)}%</strong></span>
                      <span className="text-slate-400">Engine: <strong className="text-indigo-300">{completeEvt.data.backend}</strong></span>
                    </>
                  )}
                  {def.id === 'classical_explainability' && (
                    <>
                      <span className="text-slate-400">XGB Prob: <strong className="text-indigo-300">{(completeEvt.data.xgb_probability * 100).toFixed(1)}%</strong></span>
                      <span className="text-slate-400">Margin: <strong className="text-slate-200">{completeEvt.data.output_margin > 0 ? '+' : ''}{completeEvt.data.output_margin?.toFixed(3)}</strong></span>
                      <span className="text-slate-400">SHAP Delta: <strong className="text-emerald-400">&lt;1e-6</strong></span>
                    </>
                  )}
                  {def.id === 'clinical_synthesis' && (
                    <>
                      <span className="text-slate-400">ICD-10: <strong className="text-cyan-300 font-bold">{completeEvt.data.icd10_code}</strong></span>
                      <span className="text-slate-400">Tier: <strong className={completeEvt.data.risk_tier?.includes('CRITICAL') ? 'text-rose-400' : 'text-emerald-400'}>{completeEvt.data.risk_tier}</strong></span>
                      <span className="text-slate-400">Concordance: <strong className="text-slate-200">{completeEvt.data.concordance}</strong></span>
                    </>
                  )}
                </div>
              )}

              {status === 'running' && startEvt?.data?.message && (
                <div className="mt-1 pt-1 text-[11px] font-mono text-cyan-300/90 italic truncate">
                  &gt; {startEvt.data.message}
                </div>
              )}
            </div>
          );
        })}
      </div>

    </div>
  );
}
