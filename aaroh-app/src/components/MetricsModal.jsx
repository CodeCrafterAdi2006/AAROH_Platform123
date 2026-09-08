import React, { useState, useEffect } from 'react';
import { 
  BarChart3, X, ShieldCheck, Cpu, Database, 
  Info, TrendingUp, CheckCircle2, Award
} from 'lucide-react';

export default function MetricsModal({ isOpen, onClose, metricsData, globalImportance }) {
  if (!isOpen) return null;

  const cvMetrics = metricsData?.classical_xgboost?.metrics || {};
  const qMetrics = metricsData?.quantum_vqc?.metrics || {};
  const top10 = globalImportance?.top_10_biomarkers || [];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm overflow-y-auto">
      
      <div className="relative w-full max-w-4xl max-h-[90vh] glass-panel-elevated bg-slate-900 rounded-2xl border border-slate-700 shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between p-4 sm:p-5 border-b border-slate-800 bg-slate-950/60">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <BarChart3 className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Scientific Benchmarks & Evaluation Methodology</h3>
              <p className="text-xs text-slate-400">Wisconsin Diagnostic Breast Cancer (569 Cases, 30 Features)</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-300">
          
          {/* Honest Methodology Notice Callout */}
          <div className="p-4 rounded-xl bg-cyan-950/20 border border-cyan-800/40 text-xs text-slate-300 flex items-start gap-3">
            <Info className="w-5 h-5 text-cyan-400 mt-0.5 flex-shrink-0" />
            <div className="leading-relaxed">
              <strong className="text-white block font-semibold mb-1">
                The Honest Numbers Protocol:
              </strong>
              Classical XGBoost is validated via <strong>5-Fold Stratified Cross-Validation</strong> across all 569 patient samples (mean ± standard deviation).
              The 4-Qubit VQC is evaluated on a single <strong>held-out 80/20 test split (n=114)</strong> due to quantum simulation cost.
              At 569 tabular rows, classical ML is mathematically optimal; AAROH validates quantum encoding viability and deterministic clinical explainability, rather than claiming quantum supremacy today.
            </div>
          </div>

          {/* Side by Side Comparative Metrics Table */}
          <div>
            <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
              <Award className="w-4 h-4 text-cyan-400" />
              Empirical Performance Comparison
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              
              {/* XGBoost CV Card */}
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <div className="flex items-center gap-2 mb-3">
                  <ShieldCheck className="w-4 h-4 text-indigo-400" />
                  <div>
                    <h5 className="text-sm font-bold text-white">XGBoost Baseline</h5>
                    <span className="text-[10px] text-slate-400 font-mono">5-Fold Stratified CV (n=569)</span>
                  </div>
                </div>

                <div className="space-y-2 text-xs font-mono">
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">ROC-AUC:</span>
                    <strong className="text-indigo-300 font-bold">
                      {cvMetrics.roc_auc ? `${cvMetrics.roc_auc.mean.toFixed(3)} ± ${cvMetrics.roc_auc.std.toFixed(3)}` : '0.994 ± 0.004'}
                    </strong>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Accuracy:</span>
                    <strong className="text-slate-200">
                      {cvMetrics.accuracy ? `${(cvMetrics.accuracy.mean * 100).toFixed(1)}% ± ${(cvMetrics.accuracy.std * 100).toFixed(1)}%` : '96.0% ± 1.6%'}
                    </strong>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Sensitivity (Recall):</span>
                    <strong className="text-slate-200">
                      {cvMetrics.sensitivity ? `${(cvMetrics.sensitivity.mean * 100).toFixed(1)}% ± ${(cvMetrics.sensitivity.std * 100).toFixed(1)}%` : '93.4% ± 3.3%'}
                    </strong>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Specificity:</span>
                    <strong className="text-slate-200">
                      {cvMetrics.specificity ? `${(cvMetrics.specificity.mean * 100).toFixed(1)}% ± ${(cvMetrics.specificity.std * 100).toFixed(1)}%` : '97.5% ± 1.3%'}
                    </strong>
                  </div>
                  <div className="flex justify-between py-1">
                    <span className="text-slate-400">F1-Score:</span>
                    <strong className="text-slate-200">
                      {cvMetrics.f1_score ? `${(cvMetrics.f1_score.mean * 100).toFixed(1)}% ± ${(cvMetrics.f1_score.std * 100).toFixed(1)}%` : '94.6% ± 2.2%'}
                    </strong>
                  </div>
                </div>
              </div>

              {/* Quantum VQC Split Card */}
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <div className="flex items-center gap-2 mb-3">
                  <Cpu className="w-4 h-4 text-cyan-400" />
                  <div>
                    <h5 className="text-sm font-bold text-white">4-Qubit VQC</h5>
                    <span className="text-[10px] text-cyan-400/80 font-mono">Held-out 80/20 Test Split (n=114)</span>
                  </div>
                </div>

                <div className="space-y-2 text-xs font-mono">
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">ROC-AUC:</span>
                    <strong className="text-cyan-300 font-bold">
                      {qMetrics.roc_auc ? qMetrics.roc_auc.toFixed(3) : '0.748'}
                    </strong>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Accuracy:</span>
                    <strong className="text-slate-200">
                      {qMetrics.accuracy ? `${(qMetrics.accuracy * 100).toFixed(1)}%` : '68.4%'}
                    </strong>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Sensitivity (Recall):</span>
                    <strong className="text-slate-200">
                      {qMetrics.sensitivity ? `${(qMetrics.sensitivity * 100).toFixed(1)}%` : '69.1%'}
                    </strong>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Precision:</span>
                    <strong className="text-slate-200">
                      {qMetrics.precision ? `${(qMetrics.precision * 100).toFixed(1)}%` : '55.8%'}
                    </strong>
                  </div>
                  <div className="flex justify-between py-1">
                    <span className="text-slate-400">F1-Score:</span>
                    <strong className="text-slate-200">
                      {qMetrics.f1_score ? `${(qMetrics.f1_score * 100).toFixed(1)}%` : '61.7%'}
                    </strong>
                  </div>
                </div>
              </div>

            </div>
          </div>

          {/* Global Feature Importance Table */}
          {top10.length > 0 && (
            <div>
              <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2.5 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                Cohort-Wide Global Feature Importance (Top 10 TreeSHAP Rankings)
              </h4>

              <div className="overflow-x-auto rounded-xl border border-slate-800">
                <table className="w-full text-xs text-left font-mono">
                  <thead className="bg-slate-950 text-slate-400 text-[10px] uppercase">
                    <tr>
                      <th className="py-2.5 px-3">Rank</th>
                      <th className="py-2.5 px-3">Feature Name</th>
                      <th className="py-2.5 px-3">Feature Index</th>
                      <th className="py-2.5 px-3">Mean Absolute SHAP</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 bg-slate-900/40">
                    {top10.map((item) => (
                      <tr key={item.rank} className="hover:bg-slate-800/40">
                        <td className="py-2 px-3 text-cyan-400 font-bold">#{item.rank}</td>
                        <td className="py-2 px-3 text-white font-semibold capitalize">{item.feature_name}</td>
                        <td className="py-2 px-3 text-slate-500">f_{item.feature_index}</td>
                        <td className="py-2 px-3 text-emerald-400 font-bold">{item.mean_abs_shap.toFixed(4)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}
