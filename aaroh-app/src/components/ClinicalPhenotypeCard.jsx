import React from 'react';
import { User, Calendar, Brain, Clock, Award } from 'lucide-react';

export default function ClinicalPhenotypeCard({
  patientId,
  presets = [],
  selectedPresetId,
  onSelectPreset,
  clinicalMetadata = {},
  onMetadataChange
}) {
  const age = clinicalMetadata.age ?? 65;
  const sex = clinicalMetadata.sex ?? 'Male';
  const moca = clinicalMetadata.moca ?? 25;
  const symptomMonths = clinicalMetadata.symptom_months ?? 18;

  return (
    <div className="card-clean p-5 hover:shadow-md transition-shadow">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
            <User className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-slate-900 text-sm">Clinical Phenotype & History</h3>
            <p className="text-xs text-slate-500">GP2 Release 12 Harmonized Clinical Schema</p>
          </div>
        </div>
        <span className="px-2 py-0.5 text-xs font-semibold bg-teal-50 text-teal-700 border border-teal-200 rounded-md">
          {patientId}
        </span>
      </div>

      {/* Preset Patient Selectors */}
      <div className="mb-4">
        <label className="text-xs font-semibold text-slate-700 block mb-2">
          Select Clinical Cohort Reference Case:
        </label>
        <div className="grid grid-cols-2 gap-2">
          {presets.map((preset) => {
            const isSelected = selectedPresetId === preset.preset_id;
            return (
              <button
                key={preset.preset_id}
                onClick={() => onSelectPreset(preset.preset_id)}
                className={`text-left p-2.5 rounded-xl border text-xs transition-all ${
                  isSelected
                    ? 'bg-teal-50 border-teal-500 text-teal-950 font-medium ring-2 ring-teal-500/20'
                    : 'bg-white hover:bg-slate-50 border-slate-200 text-slate-700'
                }`}
              >
                <div className="flex items-center justify-between mb-0.5">
                  <span className="font-bold text-slate-900">{preset.patient_id}</span>
                  <span className={`w-2 h-2 rounded-full ${
                    preset.preset_id === 'case_high_pd' ? 'bg-rose-500' :
                    preset.preset_id === 'case_moderate_pd' ? 'bg-amber-500' :
                    preset.preset_id === 'case_therapy_response' ? 'bg-blue-500' : 'bg-emerald-500'
                  }`} />
                </div>
                <p className="text-[11px] text-slate-500 line-clamp-1">{preset.label}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Demographic & Cognitive Variables */}
      <div className="grid grid-cols-2 gap-2.5 pt-3 border-t border-slate-100 text-xs">
        
        {/* MoCA Score */}
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
          <div className="flex items-center justify-between text-slate-600 mb-1">
            <span className="flex items-center space-x-1">
              <Brain className="w-3.5 h-3.5 text-teal-600" />
              <span>MoCA Score</span>
            </span>
            <span className="font-bold text-slate-900">{moca}/30</span>
          </div>
          <input
            type="range"
            min="10"
            max="30"
            value={moca}
            onChange={(e) => onMetadataChange && onMetadataChange({ ...clinicalMetadata, moca: parseInt(e.target.value) })}
            className="w-full accent-teal-600 h-1 bg-slate-200 rounded-lg cursor-pointer"
          />
          <span className="text-[10px] text-slate-400 block mt-0.5">
            {moca >= 26 ? 'Normative cognition' : 'Mild cognitive flagging'}
          </span>
        </div>

        {/* Symptom Duration */}
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
          <div className="flex items-center justify-between text-slate-600 mb-1">
            <span className="flex items-center space-x-1">
              <Clock className="w-3.5 h-3.5 text-teal-600" />
              <span>Duration</span>
            </span>
            <span className="font-bold text-slate-900">{symptomMonths} mo</span>
          </div>
          <input
            type="range"
            min="0"
            max="72"
            value={symptomMonths}
            onChange={(e) => onMetadataChange && onMetadataChange({ ...clinicalMetadata, symptom_months: parseInt(e.target.value) })}
            className="w-full accent-teal-600 h-1 bg-slate-200 rounded-lg cursor-pointer"
          />
          <span className="text-[10px] text-slate-400 block mt-0.5">Time since onset</span>
        </div>

        {/* Age Slider */}
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
          <div className="flex items-center justify-between text-slate-600 mb-1">
            <span className="flex items-center space-x-1">
              <Calendar className="w-3.5 h-3.5 text-teal-600" />
              <span>Age</span>
            </span>
            <span className="font-bold text-slate-900">{age} yrs</span>
          </div>
          <input
            type="range"
            min="35"
            max="90"
            value={age}
            onChange={(e) => onMetadataChange && onMetadataChange({ ...clinicalMetadata, age: parseInt(e.target.value) })}
            className="w-full accent-teal-600 h-1 bg-slate-200 rounded-lg cursor-pointer"
          />
          <span className="text-[10px] text-slate-400 block mt-0.5">Demographic risk factor</span>
        </div>

        {/* Biological Sex Toggle */}
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5 flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-600 mb-1">
            <span className="flex items-center space-x-1">
              <User className="w-3.5 h-3.5 text-teal-600" />
              <span>Biological Sex</span>
            </span>
            <span className="font-bold text-slate-900">{sex}</span>
          </div>
          <div className="grid grid-cols-2 gap-1 bg-slate-200/80 p-0.5 rounded-lg text-xs mt-0.5">
            <button
              type="button"
              onClick={() => onMetadataChange && onMetadataChange({ ...clinicalMetadata, sex: 'Male' })}
              className={`py-0.5 rounded-md font-semibold text-center transition-all ${
                sex === 'Male'
                  ? 'bg-white text-teal-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Male
            </button>
            <button
              type="button"
              onClick={() => onMetadataChange && onMetadataChange({ ...clinicalMetadata, sex: 'Female' })}
              className={`py-0.5 rounded-md font-semibold text-center transition-all ${
                sex === 'Female'
                  ? 'bg-white text-teal-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Female
            </button>
          </div>
          <span className="text-[10px] text-slate-400 block mt-0.5">GP2 Phenotype</span>
        </div>

      </div>

    </div>
  );
}
