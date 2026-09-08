import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import PatientInput from './components/PatientInput';
import AgentStream from './components/AgentStream';
import ModelComparison from './components/ModelComparison';
import ShapViewer from './components/ShapViewer';
import ClinicalMemo from './components/ClinicalMemo';
import MetricsModal from './components/MetricsModal';
import { Activity, AlertCircle, FileText, Sparkles, CheckCircle2, ChevronRight } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

// Fallback presets if backend is still starting up
const DEFAULT_PRESETS = [
  {
    preset_id: 'case_malignant',
    patient_id: 'WBCD-MAL-842302',
    label: 'Malignant Carcinoma Reference',
    ground_truth: 'Malignant',
    description: 'Marked nuclear atypia, irregular margins, elevated perimeter and area.',
    features: [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189],
  },
  {
    preset_id: 'case_benign',
    patient_id: 'WBCD-BEN-8510426',
    label: 'Benign Fibroadenoma Reference',
    ground_truth: 'Benign',
    description: 'Uniform nuclear contours, regular perimeter, non-atypical cytology.',
    features: [13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766, 0.2699, 0.7886, 2.058, 23.56, 0.008462, 0.0146, 0.02387, 0.01315, 0.0198, 0.0023, 15.11, 19.26, 99.7, 711.2, 0.144, 0.1773, 0.239, 0.1288, 0.2977, 0.07259],
  },
  {
    preset_id: 'case_borderline',
    patient_id: 'WBCD-BRD-CASE19',
    label: 'Intermediate / Borderline Case',
    ground_truth: 'Benign',
    description: 'Intermediate morphometry presenting diagnostic challenge for single-modality triage.',
    features: [14.05, 27.15, 91.38, 600.4, 0.09929, 0.1126, 0.04462, 0.04304, 0.1537, 0.06171, 0.3645, 1.492, 2.888, 29.84, 0.007256, 0.02678, 0.02071, 0.01626, 0.0208, 0.005304, 15.3, 33.17, 100.2, 706.7, 0.1241, 0.2264, 0.1326, 0.1048, 0.225, 0.09424],
  }
];

const DEFAULT_FEATURE_NAMES = [
  "mean radius", "mean texture", "mean perimeter", "mean area", "mean smoothness",
  "mean compactness", "mean concavity", "mean concave points", "mean symmetry", "mean fractal dimension",
  "radius error", "texture error", "perimeter error", "area error", "smoothness error",
  "compactness error", "concavity error", "concave points error", "symmetry error", "fractal dimension error",
  "worst radius", "worst texture", "worst perimeter", "worst area", "worst smoothness",
  "worst compactness", "worst concavity", "worst concave points", "worst symmetry", "worst fractal dimension"
];

export default function App() {
  // Backend & Metadata state
  const [backendOnline, setBackendOnline] = useState(false);
  const [healthData, setHealthData] = useState(null);
  const [benchmarks, setBenchmarks] = useState(null);
  const [globalImportance, setGlobalImportance] = useState(null);

  // Patient Case state
  const [presets, setPresets] = useState(DEFAULT_PRESETS);
  const [selectedPresetId, setSelectedPresetId] = useState('case_malignant');
  const [patientFeatures, setPatientFeatures] = useState(DEFAULT_PRESETS[0].features);
  const [featureNames, setFeatureNames] = useState(DEFAULT_FEATURE_NAMES);
  const [forceFallback, setForceFallback] = useState(false);

  // Streaming & Pipeline state
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamEvents, setStreamEvents] = useState([]);
  const [currentStage, setCurrentStage] = useState(null);
  const [streamCompleted, setStreamCompleted] = useState(false);
  const [diagnosticResult, setDiagnosticResult] = useState(null);

  // Modals state
  const [isMetricsOpen, setIsMetricsOpen] = useState(false);
  const [isMemoOpen, setIsMemoOpen] = useState(false);

  const abortControllerRef = useRef(null);

  // 1. Initial Load: Ping backend health, fetch reference presets & benchmarks
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const hRes = await fetch(`${API_BASE}/api/health`);
        if (hRes.ok) {
          const hData = await hRes.json();
          setBackendOnline(true);
          setHealthData(hData);
        }

        const ptsRes = await fetch(`${API_BASE}/api/reference-patients`);
        if (ptsRes.ok) {
          const ptsData = await ptsRes.json();
          if (ptsData.patients?.length > 0) {
            setPresets(ptsData.patients);
            setFeatureNames(ptsData.feature_names || DEFAULT_FEATURE_NAMES);
            setPatientFeatures(ptsData.patients[0].features);
          }
        }

        const mRes = await fetch(`${API_BASE}/api/metrics`);
        if (mRes.ok) {
          const mData = await mRes.json();
          setBenchmarks(mData);
        }

        const giRes = await fetch(`${API_BASE}/api/global-importance`);
        if (giRes.ok) {
          const giData = await giRes.json();
          setGlobalImportance(giData);
        }
      } catch (err) {
        console.warn("FastAPI backend is offline or unreachable:", err.message);
        setBackendOnline(false);
      }
    };

    checkBackend();
    const interval = setInterval(checkBackend, 8000);
    return () => clearInterval(interval);
  }, []);

  // 2. Preset Selection Handler
  const handleSelectPreset = (presetId) => {
    setSelectedPresetId(presetId);
    const p = presets.find(item => item.preset_id === presetId);
    if (p) {
      setPatientFeatures(p.features);
    }
  };

  // 3. SSE Stream Reader
  const handleRunDiagnosis = async () => {
    if (isStreaming) return;

    setIsStreaming(true);
    setStreamCompleted(false);
    setStreamEvents([]);
    setCurrentStage('data_ingestion');
    setDiagnosticResult(null);

    const activePreset = presets.find(p => p.preset_id === selectedPresetId) || presets[0];

    try {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      abortControllerRef.current = new AbortController();

      const response = await fetch(`${API_BASE}/api/predict/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: activePreset.patient_id,
          features: patientFeatures,
          force_fallback: forceFallback,
        }),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop(); // Keep unfinished chunk in buffer

        for (const chunk of lines) {
          if (!chunk.trim()) continue;

          let eventType = 'message';
          let dataStr = '';

          const chunkLines = chunk.split('\n');
          for (const line of chunkLines) {
            if (line.startsWith('event:')) {
              eventType = line.replace('event:', '').trim();
            } else if (line.startsWith('data:')) {
              dataStr += line.replace('data:', '').trim();
            }
          }

          if (dataStr) {
            try {
              const parsedData = JSON.parse(dataStr);
              setStreamEvents(prev => [...prev, { type: eventType, data: parsedData }]);

              if (eventType === 'stage_start') {
                setCurrentStage(parsedData.stage);
              } else if (eventType === 'final_result') {
                setDiagnosticResult(parsedData);
                setStreamCompleted(true);
              }
            } catch (e) {
              console.warn("Failed to parse SSE JSON data chunk:", dataStr);
            }
          }
        }
      }

    } catch (err) {
      if (err.name === 'AbortError') {
        console.log('Diagnosis request aborted.');
      } else {
        console.error("Streaming error, falling back to synchronous predict:", err);
        // Attempt fallback synchronous request
        try {
          const syncRes = await fetch(`${API_BASE}/api/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              patient_id: activePreset.patient_id,
              features: patientFeatures,
              force_fallback: forceFallback,
            }),
          });
          if (syncRes.ok) {
            const syncData = await syncRes.json();
            setDiagnosticResult(syncData);
            setStreamCompleted(true);
          }
        } catch (syncErr) {
          alert(`Could not connect to backend at ${API_BASE}. Make sure the FastAPI service is running.`);
        }
      }
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-bg text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      
      {/* Top Clinical Header */}
      <Header 
        backendOnline={backendOnline}
        healthData={healthData}
        onOpenMetrics={() => setIsMetricsOpen(true)}
        onOpenMemo={() => setIsMemoOpen(true)}
        hasDiagnostic={!!diagnosticResult}
      />

      {/* Main Clinical Dashboard Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-8 space-y-6">
        
        {/* Offline Warning Banner if backend not reached */}
        {!backendOnline && (
          <div className="p-3.5 rounded-xl bg-amber-950/40 border border-amber-800/60 text-amber-200 text-xs flex items-center justify-between gap-3 animate-in fade-in duration-200">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
              <span>
                Backend server is connecting at <code className="font-mono bg-amber-950 px-1.5 py-0.5 rounded text-amber-300">{API_BASE}</code>. Make sure to run <code className="font-mono bg-amber-950 px-1.5 py-0.5 rounded text-amber-300">python backend/main.py</code>.
              </span>
            </div>
            <span className="text-[11px] font-mono text-amber-400">STATUS: RETRYING</span>
          </div>
        )}

        {/* 1. Patient Ingestion & Preset Selector */}
        <PatientInput 
          presets={presets}
          selectedPresetId={selectedPresetId}
          onSelectPreset={handleSelectPreset}
          patientFeatures={patientFeatures}
          featureNames={featureNames}
          isStreaming={isStreaming}
          onRunDiagnosis={handleRunDiagnosis}
          forceFallback={forceFallback}
          setForceFallback={setForceFallback}
        />

        {/* 2. Deterministic Agentic Stream Telemetry */}
        <AgentStream 
          streamEvents={streamEvents}
          currentStage={currentStage}
          isStreaming={isStreaming}
          streamCompleted={streamCompleted}
          totalLatencyMs={diagnosticResult?.total_latency_ms || 0}
        />

        {/* 3. Dual-Model Benchmarking & Inference Panel */}
        {diagnosticResult && (
          <div className="space-y-6 animate-in fade-in duration-300">
            
            {/* Quick Action Ribbon */}
            <div className="p-4 rounded-xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-700 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-lg">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${
                  diagnosticResult.memo?.diagnosis?.includes('MALIGNANT')
                    ? 'bg-rose-500/20 text-rose-400'
                    : 'bg-emerald-500/20 text-emerald-400'
                }`}>
                  <Activity className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-white">
                      Diagnostic Consensus: {diagnosticResult.memo?.diagnosis}
                    </span>
                    <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-950 text-cyan-300 border border-slate-700">
                      ICD-10: {diagnosticResult.memo?.icd10_code}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">
                    {diagnosticResult.memo?.concordance} across XGBoost & 4-Qubit VQC models.
                  </p>
                </div>
              </div>

              <button
                onClick={() => setIsMemoOpen(true)}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-md shadow-cyan-600/20 transition-all active:scale-95 whitespace-nowrap"
              >
                <FileText className="w-4 h-4" />
                <span>Open Pathology Memo & Print</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Side-by-Side Model Comparison (Classical vs Quantum) */}
            <ModelComparison 
              classicalResult={diagnosticResult.classical}
              quantumResult={diagnosticResult.quantum}
              memoData={diagnosticResult.memo}
              benchmarks={benchmarks}
            />

            {/* Interactive TreeSHAP Attribution Force Chart */}
            <ShapViewer 
              classicalResult={diagnosticResult.classical}
            />

          </div>
        )}

      </main>

      {/* Footer */}
      <footer className="no-print border-t border-slate-800/80 py-6 px-4 text-center text-xs text-slate-500 font-mono">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>AAROH v2.0 — Deterministic Multi-Agent Hybrid Clinical Decision Support</span>
          <span>Wisconsin Breast Cancer Diagnostic (WBCD) | 569 Cases | 30 Morphometry Features</span>
        </div>
      </footer>

      {/* Pathology Consultation Memorandum Modal (Supports Print/PDF Export) */}
      <ClinicalMemo 
        memoData={diagnosticResult?.memo}
        isOpen={isMemoOpen}
        onClose={() => setIsMemoOpen(false)}
      />

      {/* Scientific Benchmarks & Methodology Modal */}
      <MetricsModal 
        isOpen={isMetricsOpen}
        onClose={() => setIsMetricsOpen(false)}
        metricsData={benchmarks}
        globalImportance={globalImportance}
      />

    </div>
  );
}
