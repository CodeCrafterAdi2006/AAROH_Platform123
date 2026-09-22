import React from 'react';
import { Printer, Download, FileText, CheckCircle2, ShieldAlert, Award } from 'lucide-react';

export default function ClinicalMemo({ memoData = {}, onBack }) {
  if (!memoData || Object.keys(memoData).length === 0) {
    return (
      <div className="card-clean p-8 text-center text-slate-500">
        <FileText className="w-8 h-8 text-slate-300 mx-auto mb-2" />
        <h4 className="font-heading font-bold text-slate-700 text-sm mb-1">No Clinical Memo Available</h4>
        <p className="text-xs text-slate-400">Run a patient screening first to generate the formal consultation memorandum.</p>
      </div>
    );
  }

  const handlePrint = () => {
    window.print();
  };

  const keyDrivers = memoData.key_biomarker_drivers || [];

  return (
    <div className="space-y-4">
      
      {/* Top Action Bar (hidden on print) */}
      <div className="no-print flex items-center justify-between bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
        <div>
          <h3 className="font-heading font-bold text-slate-900 text-sm">Formal Clinical Consultation Memo</h3>
          <p className="text-xs text-slate-500">Printable A4 Neurological Screening Consultation Memorandum</p>
        </div>

        <div className="flex items-center space-x-2">
          {onBack && (
            <button
              onClick={onBack}
              className="px-3 py-1.5 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg border border-slate-300 transition-colors"
            >
              Back to Dashboard
            </button>
          )}

          <button
            onClick={handlePrint}
            className="flex items-center space-x-1.5 px-4 py-1.5 text-xs font-semibold text-white bg-teal-600 hover:bg-teal-700 rounded-lg shadow-xs transition-colors"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print / Export PDF</span>
          </button>
        </div>
      </div>

      {/* Formal Printable Document Body */}
      <div className="print-memo card-elevated p-8 max-w-4xl mx-auto bg-white text-slate-900 border border-slate-200 rounded-2xl">
        
        {/* Document Header */}
        <div className="flex items-start justify-between pb-6 mb-6 border-b-2 border-slate-900">
          <div>
            <div className="flex items-center space-x-2 mb-1">
              <span className="font-heading font-extrabold text-2xl tracking-tight text-slate-900">AAROH CLINICAL INTELLIGENCE</span>
            </div>
            <p className="text-xs text-slate-600 font-medium">Department of Movement Disorders & Computational Neurology</p>
            <p className="text-[11px] text-slate-400">Multimodal Hybrid Classical–Quantum Decision Support System (v2.0)</p>
          </div>

          <div className="text-right text-xs">
            <span className="font-mono font-bold text-sm text-slate-900 block">CASE ID: {memoData.case_id}</span>
            <span className="text-slate-500 block">{memoData.timestamp}</span>
            <span className="px-2 py-0.5 text-[10px] font-bold bg-teal-50 text-teal-700 border border-teal-200 rounded mt-1 inline-block">
              ICD-10: {memoData.icd10_code}
            </span>
          </div>
        </div>

        {/* Diagnostic Impression Summary */}
        <div className="mb-6">
          <h4 className="font-heading font-bold text-xs uppercase tracking-wider text-teal-800 mb-2">
            1. Screening Impression & Risk Categorization
          </h4>
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
            <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
              <span className="font-bold text-base text-slate-900">{memoData.diagnosis}</span>
              <span className="px-2.5 py-0.5 text-xs font-bold bg-slate-900 text-white rounded">
                {memoData.risk_tier}
              </span>
            </div>
            <div className="grid grid-cols-3 gap-3 text-xs font-mono pt-2 border-t border-slate-200 text-slate-700">
              <div>Hybrid Score: <strong>{(memoData.hybrid_screening_score * 100).toFixed(1)}%</strong></div>
              <div>Classical Confidence: <strong>{(memoData.classical_xgb_confidence * 100).toFixed(1)}%</strong></div>
              <div>Quantum Probability: <strong>{(memoData.quantum_vqc_probability * 100).toFixed(1)}%</strong></div>
            </div>
          </div>
        </div>

        {/* Primary Acoustic Biomarker Drivers */}
        <div className="mb-6">
          <h4 className="font-heading font-bold text-xs uppercase tracking-wider text-teal-800 mb-2">
            2. Primary Acoustic Biomarker Drivers (TreeSHAP Attribution)
          </h4>
          <table className="w-full text-xs text-left border border-slate-200 rounded-lg overflow-hidden">
            <thead className="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
              <tr>
                <th className="py-2 px-3">Acoustic Biomarker</th>
                <th className="py-2 px-3">Raw Measurement</th>
                <th className="py-2 px-3">Standardized Z-Score</th>
                <th className="py-2 px-3">SHAP Attribution</th>
                <th className="py-2 px-3">Clinical Interpretation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono text-slate-800">
              {keyDrivers.map((d, i) => (
                <tr key={i} className="hover:bg-slate-50/50">
                  <td className="py-2 px-3 font-sans font-semibold text-slate-900">{d.feature_name}</td>
                  <td className="py-2 px-3">{d.raw_value}</td>
                  <td className="py-2 px-3">{d.z_score}</td>
                  <td className={`py-2 px-3 font-bold ${d.shap_attribution.startsWith('+') ? 'text-rose-600' : 'text-emerald-600'}`}>
                    {d.shap_attribution}
                  </td>
                  <td className="py-2 px-3 font-sans text-slate-600">{d.clinical_interpretation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Clinical Narrative */}
        <div className="mb-6">
          <h4 className="font-heading font-bold text-xs uppercase tracking-wider text-teal-800 mb-2">
            3. Neurological Phonation Synthesis
          </h4>
          <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3.5 rounded-xl border border-slate-200">
            {memoData.clinical_narrative}
          </p>
        </div>

        {/* Recommended Action */}
        <div className="mb-6">
          <h4 className="font-heading font-bold text-xs uppercase tracking-wider text-teal-800 mb-2">
            4. Recommended Next Diagnostic Step
          </h4>
          <p className="text-xs font-semibold text-slate-900 bg-teal-50/60 p-3.5 rounded-xl border border-teal-200 leading-relaxed">
            {memoData.recommended_action}
          </p>
        </div>

        {/* Signatures and Legal Disclaimer */}
        <div className="pt-6 border-t border-slate-200">
          <div className="flex justify-between items-end mb-6 text-xs text-slate-500">
            <div>
              <p className="font-mono text-[10px]">Algorithm Execution Hash: SHA256-AAROH-PARKINSONS</p>
              <p className="text-[10px] mt-0.5">Dual-Model Consensus: {memoData.concordance}</p>
            </div>
            <div className="text-right">
              <div className="w-40 border-b border-slate-400 mb-1"></div>
              <p className="text-[11px] font-semibold text-slate-800">Attending Neurologist / Pathologist</p>
            </div>
          </div>

          <p className="text-[10px] text-slate-400 text-center leading-normal border-t border-slate-100 pt-3">
            <strong>MANDATORY REGULATORY DISCLAIMER:</strong> {memoData.disclaimer}
          </p>
        </div>

      </div>

    </div>
  );
}
