import React from 'react';
import { Calendar, History, TrendingUp, TrendingDown, ArrowRight, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine } from 'recharts';

export default function LongitudinalHistory({
  patientId = "P-001",
  historyRecords = [],
  isLoading = false
}) {
  if (isLoading) {
    return (
      <div className="card-clean p-8 text-center text-slate-500">
        <div className="w-6 h-6 border-2 border-teal-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p className="text-xs">Loading longitudinal trajectory...</p>
      </div>
    );
  }

  if (!historyRecords || historyRecords.length === 0) {
    return (
      <div className="card-clean p-8 text-center text-slate-500">
        <History className="w-8 h-8 text-slate-300 mx-auto mb-2" />
        <h4 className="font-heading font-bold text-slate-700 text-sm mb-1">No Assessment History Found</h4>
        <p className="text-xs text-slate-400">Run a screening assessment to record the first longitudinal visit.</p>
      </div>
    );
  }

  // Format chart points
  const chartPoints = historyRecords.map((r, idx) => ({
    visit: `Visit #${idx + 1}`,
    date: r.assessed_at ? new Date(r.assessed_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : `V${idx+1}`,
    hybridScore: Math.round(r.hybrid_score * 100),
    classicalScore: Math.round(r.classical_score * 100),
    quantumScore: Math.round(r.quantum_score * 100),
    riskTier: r.risk_tier,
    consensus: r.consensus_status,
  }));

  const firstScore = chartPoints[0]?.hybridScore ?? 0;
  const latestScore = chartPoints[chartPoints.length - 1]?.hybridScore ?? 0;
  const scoreDelta = latestScore - firstScore;

  return (
    <div className="card-clean p-5 hover:shadow-md transition-shadow">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
            <History className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-slate-900 text-sm">Longitudinal Disease Trajectory & Monitoring</h3>
            <p className="text-xs text-slate-500">Multi-Visit Screening Signal Progression for Patient <strong>{patientId}</strong></p>
          </div>
        </div>

        {/* Trajectory Delta Pill */}
        <div className={`px-2.5 py-1 rounded-lg text-xs font-bold flex items-center space-x-1 ${
          scoreDelta > 5
            ? 'bg-rose-50 text-rose-700 border border-rose-200'
            : scoreDelta < -5
            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
            : 'bg-slate-100 text-slate-700 border border-slate-200'
        }`}>
          {scoreDelta > 5 ? (
            <>
              <TrendingUp className="w-3.5 h-3.5 text-rose-600" />
              <span>+{scoreDelta}% Disease Progression Signal</span>
            </>
          ) : scoreDelta < -5 ? (
            <>
              <TrendingDown className="w-3.5 h-3.5 text-emerald-600" />
              <span>{scoreDelta}% Post-Therapy Improvement</span>
            </>
          ) : (
            <span>Stable Trajectory (Δ {scoreDelta}%)</span>
          )}
        </div>
      </div>

      {/* Trajectory Line Chart */}
      <div className="h-60 w-full mb-5">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartPoints} margin={{ top: 10, right: 20, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
            <XAxis dataKey="date" stroke="#64748B" tick={{ fontSize: 11 }} />
            <YAxis domain={[0, 100]} stroke="#64748B" tick={{ fontSize: 10 }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', color: '#fff', fontSize: '11px' }}
              formatter={(value, name) => [`${value}%`, name]}
            />
            <ReferenceLine y={50} stroke="#CBD5E1" strokeDasharray="4 4" label={{ value: 'Screening Threshold', fill: '#94A3B8', fontSize: 10 }} />
            <Line
              type="monotone"
              dataKey="hybridScore"
              name="Hybrid Consensus (P_h)"
              stroke="#0D9488"
              strokeWidth={3}
              dot={{ r: 5, fill: '#0D9488', stroke: '#fff', strokeWidth: 2 }}
              activeDot={{ r: 7 }}
            />
            <Line
              type="monotone"
              dataKey="classicalScore"
              name="Classical XGBoost"
              stroke="#64748B"
              strokeWidth={1.5}
              strokeDasharray="4 4"
              dot={{ r: 3, fill: '#64748B' }}
            />
            <Line
              type="monotone"
              dataKey="quantumScore"
              name="Quantum VQC"
              stroke="#2DD4BF"
              strokeWidth={1.5}
              strokeDasharray="2 2"
              dot={{ r: 3, fill: '#2DD4BF' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Historical Visit Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-50 text-slate-500 font-semibold border-y border-slate-200">
            <tr>
              <th className="py-2 px-3">Visit Date</th>
              <th className="py-2 px-3">Classical</th>
              <th className="py-2 px-3">Quantum</th>
              <th className="py-2 px-3">Hybrid Score</th>
              <th className="py-2 px-3">Risk Tier</th>
              <th className="py-2 px-3">Consensus</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 font-mono">
            {historyRecords.map((rec, idx) => (
              <tr key={rec.id || idx} className="hover:bg-slate-50/50">
                <td className="py-2 px-3 text-slate-700 font-sans font-medium">
                  {rec.assessed_at ? new Date(rec.assessed_at).toLocaleDateString() : `Visit #${idx+1}`}
                </td>
                <td className="py-2 px-3 text-slate-600">{(rec.classical_score * 100).toFixed(1)}%</td>
                <td className="py-2 px-3 text-teal-600">{(rec.quantum_score * 100).toFixed(1)}%</td>
                <td className="py-2 px-3 font-bold text-slate-900">{(rec.hybrid_score * 100).toFixed(1)}%</td>
                <td className="py-2 px-3 font-sans">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    rec.risk_tier?.includes('ELEVATED')
                      ? 'bg-rose-50 text-rose-700'
                      : rec.risk_tier?.includes('MODERATE')
                      ? 'bg-amber-50 text-amber-700'
                      : 'bg-emerald-50 text-emerald-700'
                  }`}>
                    {rec.risk_tier}
                  </span>
                </td>
                <td className="py-2 px-3 font-sans">
                  <span className={`text-[10px] font-semibold ${
                    rec.consensus_status === 'DISCORDANT_REVIEW' ? 'text-amber-600' : 'text-teal-600'
                  }`}>
                    {rec.consensus_status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}
