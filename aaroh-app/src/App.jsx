import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import VoiceModalityCard from './components/VoiceModalityCard';
import MotorModalityCard from './components/MotorModalityCard';
import ClinicalPhenotypeCard from './components/ClinicalPhenotypeCard';
import QuantumEngineCard from './components/QuantumEngineCard';
import AgentStream from './components/AgentStream';
import ScreeningResult from './components/ScreeningResult';
import ShapExplainability from './components/ShapExplainability';
import LongitudinalHistory from './components/LongitudinalHistory';
import ClinicalMemo from './components/ClinicalMemo';
import MetricsModal from './components/MetricsModal';

const API_BASE_URL = 'http://127.0.0.1:8000';

const DEFAULT_PRESETS = [
  {
    preset_id: 'case_high_pd',
    patient_id: 'P-001',
    label: "Elevated Parkinson's Phonation (High Risk)",
    ground_truth: "Parkinson's Disease",
    description: "Marked vocal jitter, elevated PPE, and reduced HNR indicating advanced cycle-to-cycle frequency instability.",
    features: [119.992, 157.302, 74.997, 0.00784, 0.00007, 0.00370, 0.00554, 0.01109, 0.04374, 0.426, 0.02182, 0.03130, 0.02971, 0.06545, 0.02211, 21.033, 0.414783, 0.815285, -4.813031, 0.266482, 2.301442, 0.284654],
    clinical_metadata: { age: 68, sex: 'Male', moca: 23, tremor_freq_hz: 5.4, symptom_months: 24 }
  },
  {
    preset_id: 'case_moderate_pd',
    patient_id: 'P-002',
    label: "Moderate / Borderline Microperturbation",
    ground_truth: "Parkinson's Disease",
    description: "Intermediate acoustic features near clinical boundary with subtle tremor characteristics.",
    features: [197.076, 206.896, 192.055, 0.00289, 0.00001, 0.00166, 0.00168, 0.00498, 0.01098, 0.097, 0.00563, 0.00680, 0.00802, 0.01689, 0.00339, 26.775, 0.422229, 0.741367, -7.348300, 0.177551, 1.743867, 0.085569],
    clinical_metadata: { age: 62, sex: 'Female', moca: 26, tremor_freq_hz: 4.8, symptom_months: 12 }
  },
  {
    preset_id: 'case_therapy_response',
    patient_id: 'P-003',
    label: "Post-Therapy Improvement (Longitudinal)",
    ground_truth: "Parkinson's Disease (On Medication)",
    description: "Phonation metrics demonstrating stabilization post-Levodopa administration over repeated visits.",
    features: [152.845, 163.305, 75.836, 0.00294, 0.00002, 0.00121, 0.00149, 0.00364, 0.01828, 0.158, 0.01064, 0.00972, 0.01591, 0.03191, 0.00609, 24.922, 0.474791, 0.654027, -6.105098, 0.203502, 2.198672, 0.152481],
    clinical_metadata: { age: 71, sex: 'Male', moca: 25, tremor_freq_hz: 3.9, symptom_months: 36 }
  },
  {
    preset_id: 'case_healthy_control',
    patient_id: 'P-004',
    label: "Healthy Control Baseline (Normative)",
    ground_truth: "Healthy Control",
    description: "High harmonicity (HNR > 25 dB), low jitter/shimmer, regular fundamental frequency periodicity.",
    features: [241.409, 260.655, 237.261, 0.00174, 0.000007, 0.00086, 0.00115, 0.00258, 0.01170, 0.106, 0.00580, 0.00685, 0.00987, 0.01739, 0.00454, 28.184, 0.384377, 0.658721, -7.026421, 0.181812, 1.397577, 0.105872],
    clinical_metadata: { age: 59, sex: 'Female', moca: 29, tremor_freq_hz: 0.0, symptom_months: 0 }
  }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('screening'); // 'screening', 'history', 'memo'
  const [isMetricsModalOpen, setIsMetricsModalOpen] = useState(false);
  const [backendStatus, setBackendStatus] = useState('offline');

  // Clinical Patient State
  const [presets, setPresets] = useState(DEFAULT_PRESETS);
  const [selectedPresetId, setSelectedPresetId] = useState('case_high_pd');
  const [patientId, setPatientId] = useState('P-001');
  const [features, setFeatures] = useState(DEFAULT_PRESETS[0].features);
  const [featureNames, setFeatureNames] = useState([]);
  const [clinicalMetadata, setClinicalMetadata] = useState(DEFAULT_PRESETS[0].clinical_metadata);

  // Screening Execution & SSE State
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [completedStages, setCompletedStages] = useState([]);
  const [activeStage, setActiveStage] = useState(null);
  const [resultData, setResultData] = useState(null);

  // Benchmarking & Global Data
  const [metricsData, setMetricsData] = useState(null);
  const [globalImportance, setGlobalImportance] = useState([]);
  const [historyRecords, setHistoryRecords] = useState([]);
  const [isHistoryLoading, setIsHistoryLoading] = useState(false);

  // 1. Initial Data Fetch (Health, Presets, Metrics, Global Importance)
  useEffect(() => {
    async function initPlatform() {
      try {
        // Health check
        const healthRes = await fetch(`${API_BASE_URL}/api/health`);
        if (healthRes.ok) setBackendStatus('online');

        // Demo Patients
        const presetsRes = await fetch(`${API_BASE_URL}/api/demo-patients`);
        if (presetsRes.ok) {
          const pData = await presetsRes.json();
          setPresets(pData.patients || []);
          setFeatureNames(pData.feature_names || []);
          if (pData.patients && pData.patients.length > 0) {
            const firstPreset = pData.patients[0];
            setSelectedPresetId(firstPreset.preset_id);
            setPatientId(firstPreset.patient_id);
            setFeatures(firstPreset.features);
            if (firstPreset.clinical_metadata) {
              setClinicalMetadata(firstPreset.clinical_metadata);
            }
          }
        }

        // Metrics
        const metricsRes = await fetch(`${API_BASE_URL}/api/metrics`);
        if (metricsRes.ok) {
          setMetricsData(await metricsRes.json());
        }

        // Global Importance
        const giRes = await fetch(`${API_BASE_URL}/api/global-importance`);
        if (giRes.ok) {
          const giData = await giRes.json();
          setGlobalImportance(giData.all_rankings || giData.top_10_biomarkers || []);
        }
      } catch (err) {
        console.warn('Initial backend fetch error (Backend may still be starting):', err);
      }
    }
    initPlatform();
  }, []);

  // 2. Fetch History on Patient ID change
  useEffect(() => {
    async function fetchHistory() {
      if (!patientId) return;
      setIsHistoryLoading(true);
      try {
        const res = await fetch(`${API_BASE_URL}/api/patient/${patientId}/history`);
        if (res.ok) {
          const data = await res.json();
          setHistoryRecords(data.history || []);
        }
      } catch (err) {
        console.error('Failed to load history:', err);
      } finally {
        setIsHistoryLoading(false);
      }
    }
    fetchHistory();
  }, [patientId]);

  // Handle Preset Selection
  const handleSelectPreset = (presetId) => {
    setSelectedPresetId(presetId);
    const found = presets.find((p) => p.preset_id === presetId);
    if (found) {
      setPatientId(found.patient_id);
      setFeatures([...found.features]);
      if (found.clinical_metadata) {
        setClinicalMetadata({ ...found.clinical_metadata });
      }
      setResultData(null);
      setCompletedStages([]);
      setActiveStage(null);
    }
  };

  // Handle Individual Feature Adjustment
  const handleFeatureChange = (index, value) => {
    const updated = [...features];
    updated[index] = value;
    setFeatures(updated);
  };

  // Handle Tremor Adjustment
  const handleTremorChange = (val) => {
    setClinicalMetadata((prev) => ({ ...prev, tremor_freq_hz: val }));
  };

  // 3. Live SSE Streaming Execution
  const handleRunAnalysis = async () => {
    if (isAnalyzing) return;
    setIsAnalyzing(true);
    setCompletedStages([]);
    setActiveStage('data_ingestion');
    setResultData(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/screen/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: patientId,
          features: features,
        }),
      });

      if (!response.ok) {
        throw new Error(`Screening request failed with status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop(); // Keep incomplete fragment

        for (const block of lines) {
          if (!block.trim()) continue;

          let eventType = 'message';
          let jsonData = null;

          for (const line of block.split('\n')) {
            if (line.startsWith('event:')) {
              eventType = line.replace('event:', '').trim();
            } else if (line.startsWith('data:')) {
              try {
                jsonData = JSON.parse(line.replace('data:', '').trim());
              } catch (e) {
                console.error('Failed to parse SSE data block:', line);
              }
            }
          }

          if (eventType === 'stage_start' && jsonData) {
            setActiveStage(jsonData.stage);
          } else if (eventType === 'stage_complete' && jsonData) {
            setCompletedStages((prev) => [...prev, jsonData]);
          } else if (eventType === 'final_result' && jsonData) {
            setResultData(jsonData);
            setActiveStage(null);
          }
        }
      }
    } catch (err) {
      console.error('Screening pipeline execution error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Save current assessment to SQLite
  const handleSaveAssessment = async () => {
    if (!resultData) return;
    const fusion = resultData.fusion || {};
    const memo = resultData.memo || {};
    try {
      const res = await fetch(`${API_BASE_URL}/api/patient/${patientId}/save-assessment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: patientId,
          classical_score: fusion.classical_probability || 0.0,
          quantum_score: fusion.quantum_probability || 0.0,
          hybrid_score: fusion.hybrid_probability || 0.0,
          risk_tier: memo.risk_tier || 'MODERATE',
          consensus_status: fusion.consensus_status || 'CONCORDANT',
          feature_json: JSON.stringify(features),
          shap_json: JSON.stringify(resultData.classical?.top_features || []),
          clinical_memo_json: JSON.stringify(memo),
        }),
      });

      if (res.ok) {
        // Refresh history
        const hRes = await fetch(`${API_BASE_URL}/api/patient/${patientId}/history`);
        if (hRes.ok) {
          const hData = await hRes.json();
          setHistoryRecords(hData.history || []);
        }
        alert(`Assessment for patient ${patientId} saved to database!`);
      }
    } catch (e) {
      console.error('Error saving assessment:', e);
    }
  };

  const quantumTelemetry = resultData?.quantum || {
    quantum_angles_rad: [1.42, 0.85, 2.15, 0.64],
    expectation_value: -0.1238,
    backend: 'Qiskit Aer / Statevector',
    latency_ms: 9.8,
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 pb-12">
      
      {/* Navbar */}
      <Navbar
        selectedPresetId={selectedPresetId}
        presets={presets}
        onSelectPreset={handleSelectPreset}
        onRunAnalysis={handleRunAnalysis}
        isAnalyzing={isAnalyzing}
        onOpenMetrics={() => setIsMetricsModalOpen(true)}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        backendStatus={backendStatus}
      />

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        
        {/* Tab 1: Screening & Telemetry */}
        {activeTab === 'screening' && (
          <div className="space-y-6">
            
            {/* Top Grid: 3 Multimodal Modality Cards */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
              
              {/* Voice Acoustic Card */}
              <VoiceModalityCard
                features={features}
                featureNames={featureNames}
                onFeatureChange={handleFeatureChange}
                patientId={patientId}
              />

              {/* Motor Kinematics Card */}
              <MotorModalityCard
                tremorFreqHz={clinicalMetadata.tremor_freq_hz || 5.2}
                bradykinesiaScore={2}
                posturalScore={1}
                onTremorChange={handleTremorChange}
              />

              {/* Clinical Phenotype Card */}
              <ClinicalPhenotypeCard
                patientId={patientId}
                presets={presets}
                selectedPresetId={selectedPresetId}
                onSelectPreset={handleSelectPreset}
                clinicalMetadata={clinicalMetadata}
                onMetadataChange={setClinicalMetadata}
              />

            </div>

            {/* Middle Grid: Quantum Telemetry Engine + Live SSE Agent Stream */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
              
              {/* 4-Qubit Quantum Engine Card */}
              <QuantumEngineCard
                quantumTelemetry={quantumTelemetry}
                classicalScore={resultData?.fusion?.classical_probability ?? 0.0}
                quantumScore={resultData?.fusion?.quantum_probability ?? 0.0}
                hybridScore={resultData?.fusion?.hybrid_probability ?? 0.0}
                alpha={resultData?.fusion?.alpha_weight ?? 0.31}
                beta={resultData?.fusion?.beta_weight ?? 0.69}
                consensusStatus={resultData?.fusion?.consensus_status ?? "CONCORDANT"}
                isAnalyzing={isAnalyzing}
              />

              {/* 6-Stage Deterministic Agent Pipeline Stream */}
              <AgentStream
                stages={completedStages}
                activeStage={activeStage}
                isStreaming={isAnalyzing}
              />

            </div>

            {/* Bottom Grid: Screening Assessment Result + TreeSHAP Explainability */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
              
              {/* Screening Result Outcome */}
              <ScreeningResult
                resultData={resultData}
                isAnalyzing={isAnalyzing}
                onViewMemo={() => setActiveTab('memo')}
                onSaveAssessment={handleSaveAssessment}
              />

              {/* TreeSHAP Explainability */}
              <ShapExplainability
                shapData={resultData?.classical}
                globalImportance={globalImportance}
              />

            </div>

          </div>
        )}

        {/* Tab 2: Longitudinal Disease Monitoring & History */}
        {activeTab === 'history' && (
          <div className="max-w-5xl mx-auto space-y-6">
            <LongitudinalHistory
              patientId={patientId}
              historyRecords={historyRecords}
              isLoading={isHistoryLoading}
            />
          </div>
        )}

        {/* Tab 3: Formal Consultation Memo */}
        {activeTab === 'memo' && (
          <div className="max-w-4xl mx-auto space-y-6">
            <ClinicalMemo
              memoData={resultData?.memo}
              onBack={() => setActiveTab('screening')}
            />
          </div>
        )}

      </main>

      {/* Multi-Model Benchmark Comparison Modal */}
      <MetricsModal
        isOpen={isMetricsModalOpen}
        onClose={() => setIsMetricsModalOpen(false)}
        metricsData={metricsData}
      />

    </div>
  );
}
