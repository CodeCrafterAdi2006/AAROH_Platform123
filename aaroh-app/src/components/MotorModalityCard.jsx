import React from 'react';
import { Activity, Gauge, Compass, Zap } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';

export default function MotorModalityCard({
  tremorFreqHz = 5.2,
  bradykinesiaScore = 2,
  posturalScore = 1,
  onTremorChange
}) {
  // Generate a simulated tremor power spectral density curve (peaks between 3-7 Hz for PD)
  const freqData = [
    { freq: '1 Hz', power: 0.1 },
    { freq: '2 Hz', power: 0.3 },
    { freq: '3 Hz', power: 0.9 },
    { freq: '4 Hz', power: tremorFreqHz >= 4 ? 2.8 : 0.6 },
    { freq: '5 Hz', power: tremorFreqHz >= 5 ? 4.6 : 0.4 },
    { freq: '6 Hz', power: tremorFreqHz >= 6 ? 3.1 : 0.2 },
    { freq: '7 Hz', power: 1.1 },
    { freq: '8 Hz', power: 0.4 },
    { freq: '9 Hz', power: 0.2 },
    { freq: '10 Hz', power: 0.1 },
  ];

  return (
    <div className="card-clean p-5 hover:shadow-md transition-shadow">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-slate-900 text-sm">Motor & Biometric Kinematics</h3>
            <p className="text-xs text-slate-500">MDS-UPDRS Part III & Accelerometry Sensor Spectrum</p>
          </div>
        </div>
        <span className="px-2 py-0.5 text-xs font-semibold bg-slate-100 text-slate-700 rounded-md border border-slate-200">
          3-Axis IMU (100 Hz)
        </span>
      </div>

      {/* Tremor Spectral Density Chart */}
      <div className="bg-slate-900 rounded-xl p-3 mb-4 text-white">
        <div className="flex items-center justify-between mb-1 px-1">
          <span className="text-xs text-slate-400 font-mono">Tremor Power Spectral Density (PSD)</span>
          <span className="text-[10px] font-mono bg-teal-950 text-teal-400 border border-teal-800 px-2 py-0.5 rounded">
            Peak: {tremorFreqHz.toFixed(1)} Hz
          </span>
        </div>

        <div className="h-28 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={freqData} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
              <defs>
                <linearGradient id="tremorGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#14B8A6" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#0D9488" stopOpacity={0.0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="freq" stroke="#64748B" tick={{ fontSize: 10 }} />
              <YAxis stroke="#64748B" tick={{ fontSize: 9 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }}
                itemStyle={{ color: '#2DD4BF' }}
              />
              <Area type="monotone" dataKey="power" stroke="#2DD4BF" strokeWidth={2} fillOpacity={1} fill="url(#tremorGradient)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Motor Metric Chips */}
      <div className="grid grid-cols-3 gap-2 mb-3 text-xs">
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
          <div className="flex items-center space-x-1 text-slate-500 mb-1">
            <Zap className="w-3 h-3 text-teal-600" />
            <span className="text-[11px]">Tremor Freq</span>
          </div>
          <span className={`font-bold text-sm ${tremorFreqHz >= 3.5 && tremorFreqHz <= 7.0 ? 'text-amber-600' : 'text-slate-800'}`}>
            {tremorFreqHz.toFixed(1)} Hz
          </span>
          <span className="text-[10px] text-slate-400 block mt-0.5">PD Range: 3–7 Hz</span>
        </div>

        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
          <div className="flex items-center space-x-1 text-slate-500 mb-1">
            <Gauge className="w-3 h-3 text-teal-600" />
            <span className="text-[11px]">Bradykinesia</span>
          </div>
          <span className="font-bold text-sm text-slate-800">
            Score: {bradykinesiaScore}/4
          </span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Finger Tapping Subscore</span>
        </div>

        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
          <div className="flex items-center space-x-1 text-slate-500 mb-1">
            <Compass className="w-3 h-3 text-teal-600" />
            <span className="text-[11px]">Postural Sway</span>
          </div>
          <span className="font-bold text-sm text-slate-800">
            Grade: {posturalScore}/4
          </span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Pull Test Score</span>
        </div>
      </div>

      {/* Micro Slider for Tremor Frequency Exploration */}
      <div className="pt-2 border-t border-slate-100">
        <div className="flex justify-between text-xs mb-1">
          <span className="text-slate-600 font-medium">Resting Tremor Frequency Adjust</span>
          <span className="font-mono text-slate-900 font-semibold">{tremorFreqHz.toFixed(1)} Hz</span>
        </div>
        <input
          type="range"
          min="0"
          max="9"
          step="0.1"
          value={tremorFreqHz}
          onChange={(e) => onTremorChange && onTremorChange(parseFloat(e.target.value))}
          className="w-full accent-teal-600 h-1.5 bg-slate-200 rounded-lg cursor-pointer"
        />
      </div>

    </div>
  );
}
