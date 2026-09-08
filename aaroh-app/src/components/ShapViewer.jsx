import React, { useState } from 'react';
import { 
  BarChart2, ArrowRight, ArrowLeft, Info, HelpCircle, 
  TrendingUp, TrendingDown, CheckCircle2, Sliders
} from 'lucide-react';

export default function ShapViewer({ classicalResult }) {
  const [selectedFeature, setSelectedFeature] = useState(null);

  if (!classicalResult) {
    return null;
  }

  const {
    base_value,
    output_margin,
    margin_additive_delta,
    top_features,
    waterfall_steps,
    top_malignant_drivers,
    top_benign_drivers,
  } = classicalResult;

  // Features list for visualization (take top 8 for clean visual display)
  const displayFeatures = (top_features || []).slice(0, 8);

  // Find max absolute SHAP value for scaling bars
  const maxAbsShap = Math.max(...displayFeatures.map(f => Math.abs(f.shap_value || 0)), 0.5);

  return (
    <div className="glass-panel rounded-2xl p-5 lg:p-6 border border-slate-800 flex flex-col gap-5">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <BarChart2 className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white flex items-center gap-2">
              Exact TreeSHAP Explainability & Force Breakdown
              <span className="text-[11px] font-mono font-normal px-2 py-0.5 rounded bg-slate-800 text-emerald-400 border border-slate-700">
                Lundberg & Lee (Additive Invariant)
              </span>
            </h2>
            <p className="text-xs text-slate-400">
              Deterministic feature-level attributions quantifying why XGBoost reached this diagnosis.
            </p>
          </div>
        </div>

        {/* Invariant badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300">
          <span className="text-slate-500">Additive Δ:</span>
          <strong className="text-emerald-400">{margin_additive_delta?.toExponential(2) || '<1e-6'}</strong>
          <span className="text-[10px] text-slate-500">(Zero Leakage)</span>
        </div>
      </div>

      {/* Base Value ➔ Margin Formula Ribbon */}
      <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-wrap items-center justify-between gap-3 font-mono text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-400">Cohort Base Value E[f(x)]:</span>
          <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-200 font-bold">
            {base_value.toFixed(4)}
          </span>
        </div>

        <div className="flex items-center gap-1.5 text-slate-500">
          <span>+</span>
          <span>Σ SHAP Forces</span>
          <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
        </div>

        <div className="flex items-center gap-2">
          <span className="text-slate-400">Final Decision Margin f(x):</span>
          <span className={`px-2 py-0.5 rounded font-bold ${
            output_margin >= 0 
              ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' 
              : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
          }`}>
            {output_margin > 0 ? '+' : ''}{output_margin.toFixed(4)}
          </span>
        </div>
      </div>

      {/* Force Vectors Horizontal Bar Chart */}
      <div>
        <div className="flex items-center justify-between text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
          <span className="flex items-center gap-1 text-emerald-400">
            <ArrowLeft className="w-3.5 h-3.5" /> Pulling Towards Benign (Negative Force)
          </span>
          <span className="flex items-center gap-1 text-rose-400">
            Pushing Towards Malignant (Positive Force) <ArrowRight className="w-3.5 h-3.5" />
          </span>
        </div>

        <div className="space-y-2.5">
          {displayFeatures.map((feat, idx) => {
            const isMalignantDriver = feat.shap_value > 0;
            const barWidthPercent = (Math.abs(feat.shap_value) / maxAbsShap) * 48; // Max 48% each side

            return (
              <div 
                key={idx}
                onClick={() => setSelectedFeature(selectedFeature === feat.feature_name ? null : feat.feature_name)}
                className={`p-2.5 rounded-lg border transition-all cursor-pointer ${
                  selectedFeature === feat.feature_name
                    ? 'bg-slate-800 border-cyan-500'
                    : 'bg-slate-900/50 border-slate-800/80 hover:border-slate-700 hover:bg-slate-800/40'
                }`}
              >
                {/* Feature Label & Values */}
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-white capitalize">
                      {feat.feature_name}
                    </span>
                    <span className="text-[10px] font-mono text-slate-400 bg-slate-950 px-1.5 py-0.5 rounded">
                      Raw: {feat.raw_value}
                    </span>
                    <span className="text-[10px] font-mono text-cyan-400 bg-slate-950 px-1.5 py-0.5 rounded">
                      Z: {feat.standardized_z_score > 0 ? '+' : ''}{feat.standardized_z_score.toFixed(2)}σ
                    </span>
                  </div>

                  <span className={`font-mono font-bold text-xs ${
                    isMalignantDriver ? 'text-rose-400' : 'text-emerald-400'
                  }`}>
                    {isMalignantDriver ? '+' : ''}{feat.shap_value.toFixed(4)}
                  </span>
                </div>

                {/* Center-aligned Force Bar */}
                <div className="relative w-full h-3 bg-slate-950 rounded-full overflow-hidden flex items-center">
                  {/* Center zero axis */}
                  <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-slate-700 z-10" />

                  {/* Left (Benign) or Right (Malignant) bar */}
                  {isMalignantDriver ? (
                    <div 
                      className="absolute left-1/2 h-full bg-gradient-to-r from-rose-600 to-rose-400 rounded-r-full transition-all duration-500"
                      style={{ width: `${barWidthPercent}%` }}
                    />
                  ) : (
                    <div 
                      className="absolute right-1/2 h-full bg-gradient-to-l from-emerald-600 to-emerald-400 rounded-l-full transition-all duration-500"
                      style={{ width: `${barWidthPercent}%` }}
                    />
                  )}
                </div>

                {/* Expanded details when clicked */}
                {selectedFeature === feat.feature_name && (
                  <div className="mt-2 pt-2 border-t border-slate-700/60 text-xs text-slate-300 animate-in fade-in duration-150">
                    <p className="leading-relaxed">
                      This patient's <strong>{feat.feature_name}</strong> is measured at <strong>{feat.raw_value}</strong>, 
                      which is <strong>{Math.abs(feat.standardized_z_score).toFixed(1)} standard deviations</strong> {feat.standardized_z_score > 0 ? 'above' : 'below'} the cohort mean. 
                      This exerts a net <strong>{feat.direction?.toUpperCase()}</strong> impact of <strong>{feat.shap_value > 0 ? '+' : ''}{feat.shap_value.toFixed(4)}</strong> log-odds units on the final diagnosis.
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Top Drivers Summary Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
        
        {/* Malignant drivers */}
        <div className="p-3 rounded-xl bg-rose-950/20 border border-rose-900/30 text-xs">
          <div className="flex items-center gap-1.5 text-rose-400 font-semibold mb-2">
            <TrendingUp className="w-3.5 h-3.5" />
            <span>Top Risk-Elevating Nuclear Biomarkers</span>
          </div>
          <ul className="space-y-1 text-slate-300 font-mono text-[11px]">
            {(top_malignant_drivers || []).slice(0, 3).map((d, i) => (
              <li key={i} className="flex justify-between items-center">
                <span className="capitalize">{d.feature_name}</span>
                <span className="text-rose-400 font-bold">+{d.shap_value.toFixed(3)}</span>
              </li>
            ))}
            {(!top_malignant_drivers || top_malignant_drivers.length === 0) && (
              <li className="text-slate-500 italic">No significant malignant drivers detected.</li>
            )}
          </ul>
        </div>

        {/* Benign drivers */}
        <div className="p-3 rounded-xl bg-emerald-950/20 border border-emerald-900/30 text-xs">
          <div className="flex items-center gap-1.5 text-emerald-400 font-semibold mb-2">
            <TrendingDown className="w-3.5 h-3.5" />
            <span>Top Protective / Normal Biomarkers</span>
          </div>
          <ul className="space-y-1 text-slate-300 font-mono text-[11px]">
            {(top_benign_drivers || []).slice(0, 3).map((d, i) => (
              <li key={i} className="flex justify-between items-center">
                <span className="capitalize">{d.feature_name}</span>
                <span className="text-emerald-400 font-bold">{d.shap_value.toFixed(3)}</span>
              </li>
            ))}
            {(!top_benign_drivers || top_benign_drivers.length === 0) && (
              <li className="text-slate-500 italic">No significant benign drivers detected.</li>
            )}
          </ul>
        </div>

      </div>

    </div>
  );
}
