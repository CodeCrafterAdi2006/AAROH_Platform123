import React, { useState } from 'react';
import { 
  FileText, Printer, Copy, Check, X, ShieldAlert, 
  Activity, AlertTriangle, CheckCircle2, Hospital
} from 'lucide-react';

export default function ClinicalMemo({ memoData, isOpen, onClose }) {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !memoData) return null;

  const handleCopy = () => {
    if (memoData?.memo_markdown) {
      navigator.clipboard.writeText(memoData.memo_markdown);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const isMalignant = memoData.diagnosis?.includes('MALIGNANT');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm overflow-y-auto">
      
      {/* Modal Dialog Card */}
      <div className="relative w-full max-w-4xl max-h-[90vh] glass-panel-elevated bg-slate-900 rounded-2xl border border-slate-700 shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Modal Action Bar (Hidden on print) */}
        <div className="no-print flex items-center justify-between p-4 border-b border-slate-800 bg-slate-950/60">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">Clinical Pathology Memorandum</h3>
              <p className="text-xs text-slate-400">Deterministic Multi-Agent Diagnostic Summary</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium transition-all"
              title="Copy memo Markdown"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>

            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-md shadow-cyan-600/20 transition-all active:scale-95"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Print / Export PDF</span>
            </button>

            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all ml-1"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Printable Memo Content */}
        <div className="p-6 sm:p-8 overflow-y-auto space-y-6 text-slate-200 print-container font-sans">
          
          {/* Hospital / Pathology Header */}
          <div className="border-b-2 border-slate-700 pb-4 flex flex-col sm:flex-row sm:items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <Hospital className="w-5 h-5 text-cyan-400" />
                <h1 className="text-lg font-bold text-white uppercase tracking-tight">
                  AAROH CLINICAL PATHOLOGY INTELLIGENCE
                </h1>
              </div>
              <p className="text-xs text-slate-400">
                Department of Cytopathology & Quantum Benchmarking Division
              </p>
            </div>
            
            <div className="text-left sm:text-right font-mono text-xs text-slate-400 space-y-0.5">
              <div>Case ID: <strong className="text-cyan-300">{memoData.case_id}</strong></div>
              <div>Date: {memoData.timestamp}</div>
              <div>Specimen: {memoData.specimen}</div>
            </div>
          </div>

          {/* Section 1: Impression & ICD-10 */}
          <div className={`p-4 rounded-xl border ${
            isMalignant 
              ? 'bg-rose-950/20 border-rose-800/40 text-rose-200' 
              : 'bg-emerald-950/20 border-emerald-800/40 text-emerald-200'
          }`}>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider block opacity-80">
                  PRIMARY PATHOLOGICAL IMPRESSION
                </span>
                <h2 className="text-xl font-black tracking-tight">
                  {memoData.diagnosis}
                </h2>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <span className="px-2.5 py-1 rounded-md bg-slate-900/80 border border-slate-700 text-xs font-mono font-bold text-white">
                  ICD-10: {memoData.icd10_code}
                </span>
                <span className={`px-2.5 py-1 rounded-md text-xs font-mono font-bold border ${
                  isMalignant 
                    ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' 
                    : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                }`}>
                  {memoData.risk_tier}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-3 border-t border-slate-700/50 text-xs font-mono">
              <div>
                <span className="text-slate-400 block text-[10px]">XGBoost Confidence</span>
                <strong className="text-white text-sm">{(memoData.classical_xgb_confidence * 100).toFixed(1)}%</strong>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Quantum VQC State Prob</span>
                <strong className="text-cyan-300 text-sm">{(memoData.quantum_vqc_probability * 100).toFixed(1)}%</strong>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Model Concordance</span>
                <strong className="text-emerald-400 text-sm">{memoData.concordance}</strong>
              </div>
            </div>
          </div>

          {/* Section 2: Key Biomarker Drivers */}
          <div>
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2.5 flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              Primary Nuclear Biomarker Drivers (TreeSHAP Attributions)
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left font-mono">
                <thead className="bg-slate-950/80 text-slate-400 uppercase text-[10px]">
                  <tr>
                    <th className="py-2 px-3">Biomarker Feature</th>
                    <th className="py-2 px-3">Raw Value</th>
                    <th className="py-2 px-3">Z-Score</th>
                    <th className="py-2 px-3">SHAP Force</th>
                    <th className="py-2 px-3">Clinical Impact</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {(memoData.key_biomarker_drivers || []).map((b, i) => (
                    <tr key={i} className="hover:bg-slate-800/30">
                      <td className="py-2 px-3 font-semibold text-white capitalize">{b.feature_name}</td>
                      <td className="py-2 px-3 text-slate-300">{b.raw_value}</td>
                      <td className="py-2 px-3 text-cyan-300">{b.z_score > 0 ? '+' : ''}{b.z_score.toFixed(2)}σ</td>
                      <td className="py-2 px-3 font-bold text-slate-100">{b.shap_attribution}</td>
                      <td className="py-2 px-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          b.direction === 'malignant' 
                            ? 'bg-rose-500/20 text-rose-300' 
                            : 'bg-emerald-500/20 text-emerald-300'
                        }`}>
                          {b.clinical_interpretation}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Section 3: Pathology Synthesis */}
          <div className="space-y-1.5">
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Pathology Cytomorphometry Synthesis
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/40 p-3.5 rounded-xl border border-slate-800">
              {memoData.clinical_narrative}
            </p>
          </div>

          {/* Section 4: Recommended Action */}
          <div className="space-y-1.5">
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Recommended Next Clinical Action
            </h3>
            <div className="p-3.5 rounded-xl bg-cyan-950/20 border border-cyan-800/40 text-xs text-cyan-200 leading-relaxed">
              {memoData.recommended_action}
            </div>
          </div>

          {/* Regulatory Disclaimer */}
          <div className="pt-4 border-t border-slate-800 text-[10px] text-slate-500 leading-relaxed space-y-1">
            <div className="flex items-center gap-1.5 text-slate-400 font-bold uppercase tracking-wider">
              <ShieldAlert className="w-3.5 h-3.5" />
              Regulatory & Decision-Support Disclaimer
            </div>
            <p>{memoData.disclaimer}</p>
            <div className="text-slate-600 font-mono pt-1">
              Audit Hash: SHA256-AAROH-GATE2 | Execution Time: {memoData.execution_time_ms}ms
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
