import React from 'react';
import { AlertCircle, CheckCircle2, AlertTriangle, ShieldCheck, ArrowRight, HeartPulse, FileText } from 'lucide-react';

export default function ScreeningResult({
  resultData = null,
  isAnalyzing = false,
  onViewMemo,
  onSaveAssessment
}) {
  if (!resultData && !isAnalyzing) {
    return (
      <div className="card-clean p-8 text-center text-slate-500">
        <HeartPulse className="w-10 h-10 text-slate-300 mx-auto mb-3" />
        <h4 className="font-heading font-bold text-slate-700 text-base mb-1">No Screening Results Generated Yet</h4>
        <p className="text-xs text-slate-500 max-w-sm mx-auto mb-4">
          Select a patient preset or adjust voice and motor biomarkers, then click <strong>"Run Screening"</strong> to orchestrate the 6-stage pipeline.
        </p>
      </div>
    );
  }

  const fusion = resultData?.fusion || {};
  const classical = resultData?.classical || {};
  const quantum = resultData?.quantum || {};
  const memo = resultData?.memo || {};

  const hybridProb = fusion.hybrid_probability ?? 0.696;
  const classicalProb = fusion.classical_probability ?? 0.995;
  const quantumProb = fusion.quantum_probability ?? 0.562;
  const riskTier = memo.risk_tier || "ELEVATED SCREENING SIGNAL";
  const icd10 = memo.icd10_code || "G20";
  const diagnosis = memo.diagnosis || "Elevated Parkinsonian Phonation Signal";
  const recommendation = memo.recommended_action || "Movement Disorder Specialist referral recommended.";

  const isElevated = hybridProb >= 0.70;
  const isModerate = hybridProb >= 0.45 && hybridProb < 0.70;

  return (
    <div className="card-elevated p-6 border-t-4 border-t-teal-600">
      
      {/* Top Header & Risk Badge */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-4 mb-5 border-b border-slate-100">
        <div>
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
            Synthesized Screening Assessment
          </span>
          <h2 className="font-heading font-extrabold text-xl text-slate-900 mt-0.5">
            {diagnosis}
          </h2>
        </div>

        <div className="flex items-center space-x-2">
          <span className="px-2.5 py-1 text-xs font-mono font-bold bg-slate-100 text-slate-700 border border-slate-200 rounded-lg">
            ICD-10: {icd10}
          </span>
          <span className={`px-3 py-1 text-xs font-bold rounded-lg border ${
            isElevated
              ? 'bg-rose-50 text-rose-700 border-rose-200'
              : isModerate
              ? 'bg-amber-50 text-amber-700 border-amber-200'
              : 'bg-emerald-50 text-emerald-700 border-emerald-200'
          }`}>
            {riskTier}
          </span>
        </div>
      </div>

      {/* Main Score Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        
        {/* Classical XGBoost */}
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-center">
          <span className="text-xs text-slate-500 font-medium block mb-1">Classical Model (XGBoost)</span>
          <span className="text-2xl font-bold font-mono text-slate-800">
            {(classicalProb * 100).toFixed(1)}%
          </span>
          <span className="text-[11px] text-slate-400 block mt-1">22 Acoustic Features (5-Fold CV)</span>
        </div>

        {/* Quantum VQC */}
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-center">
          <span className="text-xs text-slate-500 font-medium block mb-1">Quantum Engine (4-Qubit VQC)</span>
          <span className="text-2xl font-bold font-mono text-teal-700">
            {(quantumProb * 100).toFixed(1)}%
          </span>
          <span className="text-[11px] text-slate-400 block mt-1">ZZFeatureMap + RealAmplitudes</span>
        </div>

        {/* Hybrid Fusion Master Score */}
        <div className={`rounded-xl p-4 text-center border-2 ${
          isElevated
            ? 'bg-rose-50/70 border-rose-300'
            : isModerate
            ? 'bg-amber-50/70 border-amber-300'
            : 'bg-emerald-50/70 border-emerald-300'
        }`}>
          <span className="text-xs font-bold text-slate-700 block mb-1">Optimal Hybrid Consensus (P_h)</span>
          <span className={`text-3xl font-extrabold font-mono ${
            isElevated ? 'text-rose-700' : isModerate ? 'text-amber-700' : 'text-emerald-700'
          }`}>
            {(hybridProb * 100).toFixed(1)}%
          </span>
          <span className="text-[11px] font-medium text-slate-600 block mt-1">
            0.31 Classical + 0.69 Quantum
          </span>
        </div>

      </div>

      {/* Recommended Clinical Action Box */}
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-5">
        <div className="flex items-start space-x-3">
          <div className="w-8 h-8 rounded-lg bg-teal-100 text-teal-700 flex items-center justify-center shrink-0 mt-0.5">
            <HeartPulse className="w-4 h-4" />
          </div>
          <div>
            <h4 className="font-heading font-bold text-slate-900 text-xs mb-1">
              Recommended Next Clinical Steps (Decision Support Protocol)
            </h4>
            <p className="text-xs text-slate-600 leading-relaxed">
              {recommendation}
            </p>
          </div>
        </div>
      </div>

      {/* Action CTA Buttons: View Full Clinical Memo / Save Assessment */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100">
        <span className="text-[11px] text-slate-400 italic">
          Decision Support Aid • Not an Autonomous Diagnostic Device
        </span>

        <div className="flex items-center space-x-2">
          {onSaveAssessment && (
            <button
              onClick={onSaveAssessment}
              className="px-3 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 rounded-lg shadow-xs transition-colors"
            >
              Save to Patient History
            </button>
          )}

          {onViewMemo && (
            <button
              onClick={onViewMemo}
              className="flex items-center space-x-1.5 px-3.5 py-1.5 text-xs font-semibold text-white bg-teal-600 hover:bg-teal-700 rounded-lg shadow-xs transition-colors"
            >
              <FileText className="w-3.5 h-3.5" />
              <span>View Consultation Memo</span>
            </button>
          )}
        </div>
      </div>

    </div>
  );
}
