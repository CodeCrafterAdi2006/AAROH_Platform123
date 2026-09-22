import React from 'react';
import { Mic, Volume2, Waves, Sliders, Play, RotateCcw } from 'lucide-react';

export default function VoiceModalityCard({
  features,
  featureNames,
  onFeatureChange,
  patientId,
  onResetDemo
}) {
  // Extract key acoustic biomarkers from the 22-feature vector
  // MDVP:Fo(0), MDVP:Fhi(1), MDVP:Flo(2), MDVP:Jitter(%)(3), MDVP:Jitter(Abs)(4),
  // MDVP:Shimmer(8), HNR(15), RPDE(16), DFA(17), spread1(18), spread2(19), PPE(21)
  const fo = features[0] ?? 120.0;
  const fhi = features[1] ?? 157.0;
  const jitterPct = (features[3] ?? 0.007) * 100;
  const shimmer = features[8] ?? 0.043;
  const hnr = features[15] ?? 21.0;
  const ppe = features[21] ?? 0.28;
  const rpde = features[16] ?? 0.44;

  const barHeights = [25, 45, 75, 90, 60, 80, 100, 70, 50, 85, 95, 65, 40, 70, 85, 55, 30, 65, 80, 50];

  return (
    <div className="card-clean p-5 hover:shadow-md transition-shadow">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
            <Mic className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-slate-900 text-sm">Voice Acoustic Telemonitoring</h3>
            <p className="text-xs text-slate-500">22 MDVP Phonation & Perturbation Features</p>
          </div>
        </div>
        <span className="px-2 py-0.5 text-xs font-semibold bg-slate-100 text-slate-700 rounded-md border border-slate-200">
          Sustained Vowel /a/
        </span>
      </div>

      {/* Audio Waveform Visualization Bar */}
      <div className="bg-slate-900 rounded-xl p-4 mb-4 text-white relative overflow-hidden">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2 text-xs text-slate-400">
            <Volume2 className="w-3.5 h-3.5 text-teal-400" />
            <span>Phonation Signal: <strong className="text-teal-300">44.1 kHz / 16-bit</strong></span>
          </div>
          <span className="text-[10px] font-mono uppercase bg-teal-950 text-teal-400 border border-teal-800 px-2 py-0.5 rounded">
            Live Stream Ready
          </span>
        </div>

        {/* Animated Bar Visualizer */}
        <div className="h-12 flex items-end justify-between gap-1 px-1 py-1">
          {barHeights.map((h, i) => (
            <div
              key={i}
              className="w-full bg-gradient-to-t from-teal-600 to-teal-300 rounded-xs transition-all duration-300"
              style={{
                height: `${h}%`,
                animation: `audio-wave 1.4s ease-in-out infinite alternate ${i * 0.06}s`,
                opacity: 0.75 + (h / 400),
              }}
            />
          ))}
        </div>

        <div className="flex items-center justify-between mt-2 text-[11px] text-slate-400 font-mono">
          <span>Fo: {fo.toFixed(1)} Hz</span>
          <span>Fhi: {fhi.toFixed(1)} Hz</span>
          <span>HNR: {hnr.toFixed(1)} dB</span>
        </div>
      </div>

      {/* Key Biomarker Metric Chips */}
      <div className="grid grid-cols-3 gap-2 mb-4 text-xs">
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
          <span className="text-slate-500 block text-[11px]">Jitter (%)</span>
          <span className={`font-bold text-sm ${jitterPct > 0.5 ? 'text-rose-600' : 'text-slate-800'}`}>
            {jitterPct.toFixed(3)}%
          </span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Norm: &lt; 0.5%</span>
        </div>

        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
          <span className="text-slate-500 block text-[11px]">Shimmer</span>
          <span className={`font-bold text-sm ${shimmer > 0.04 ? 'text-amber-600' : 'text-slate-800'}`}>
            {shimmer.toFixed(3)}
          </span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Norm: &lt; 0.038</span>
        </div>

        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
          <span className="text-slate-500 block text-[11px]">PPE (Entropy)</span>
          <span className={`font-bold text-sm ${ppe > 0.25 ? 'text-rose-600' : 'text-emerald-600'}`}>
            {ppe.toFixed(3)}
          </span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Norm: &lt; 0.20</span>
        </div>
      </div>

      {/* Interactive Micro-Sliders for Feature Exploration */}
      <div className="space-y-2.5 pt-2 border-t border-slate-100">
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-600 font-medium">Harmonics-to-Noise Ratio (HNR)</span>
            <span className="font-mono text-slate-900 font-semibold">{hnr.toFixed(1)} dB</span>
          </div>
          <input
            type="range"
            min="8"
            max="35"
            step="0.1"
            value={hnr}
            onChange={(e) => onFeatureChange && onFeatureChange(15, parseFloat(e.target.value))}
            className="w-full accent-teal-600 h-1.5 bg-slate-200 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-600 font-medium">Pitch Period Entropy (PPE)</span>
            <span className="font-mono text-slate-900 font-semibold">{ppe.toFixed(3)}</span>
          </div>
          <input
            type="range"
            min="0.05"
            max="0.55"
            step="0.005"
            value={ppe}
            onChange={(e) => onFeatureChange && onFeatureChange(21, parseFloat(e.target.value))}
            className="w-full accent-teal-600 h-1.5 bg-slate-200 rounded-lg cursor-pointer"
          />
        </div>
      </div>

    </div>
  );
}
