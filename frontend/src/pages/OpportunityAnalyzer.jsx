import React, { useState } from 'react';
import { analyzeOpportunity, checkEligibility, getProfile } from '../services/api';
import { 
  Upload, 
  FileText, 
  Sparkles, 
  AlertCircle, 
  CheckCircle, 
  Calendar, 
  Building2, 
  ExternalLink, 
  Award, 
  ShieldCheck, 
  ArrowLeft,
  RefreshCw,
  Info
} from 'lucide-react';

export default function OpportunityAnalyzer({ onBack }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [eligibilityResult, setEligibilityResult] = useState(null);
  const [eligibilityLoading, setEligibilityLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setError(null);
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Please select a valid PDF document (.pdf).');
      setSelectedFile(null);
      return;
    }

    if (file.size > 15 * 1024 * 1024) {
      setError('Selected PDF file size exceeds maximum limit of 15 MB.');
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select a scholarship PDF file first.');
      return;
    }

    setLoading(true);
    setError(null);

    const response = await analyzeOpportunity(selectedFile);
    setLoading(false);

    if (response.success && response.opportunity) {
      setResult(response.opportunity);
    } else {
      setError(response.error || 'Failed to analyze the document. Please try again.');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setEligibilityResult(null);
  };

  const handleCheckEligibility = async () => {
    if (!result?.id) {
      setError('No opportunity ID available. Please re-analyze the document.');
      return;
    }
    setEligibilityLoading(true);
    setError(null);
    setEligibilityResult(null);

    // Verify profile is not empty
    const currentProfile = await getProfile();
    const hasProfileData = currentProfile && (
      currentProfile.state || 
      currentProfile.family_income !== null || 
      currentProfile.academic_percentage !== null || 
      currentProfile.academic_percentile !== null ||
      currentProfile.attendance_percentage !== null ||
      currentProfile.course_level ||
      currentProfile.category ||
      currentProfile.bpl_status !== null ||
      currentProfile.passed_first_attempt !== null ||
      currentProfile.receiving_other_scholarship !== null
    );

    if (!hasProfileData) {
      setEligibilityLoading(false);
      setError('Your Student Profile is currently empty. Please complete and save your Student Profile first to evaluate eligibility.');
      return;
    }

    const res = await checkEligibility(result.id);
    setEligibilityLoading(false);
    if (res) {
      setEligibilityResult(res);
    } else {
      setError('Failed to evaluate eligibility. Make sure your profile is saved.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-8 selection:bg-blue-600 selection:text-white">
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Navigation & Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-6">
          <div className="flex items-center gap-4">
            {onBack && (
              <button
                onClick={onBack}
                className="p-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-800 transition"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
            )}
            <div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
                <Sparkles className="w-7 h-7 text-blue-500" /> Opportunity Analyzer
              </h1>
              <p className="text-slate-400 text-sm mt-1">
                Upload a scholarship document (PDF) to extract structured requirements, deadlines, benefits & required documents.
              </p>
            </div>
          </div>
          {result && (
            <button
              onClick={handleReset}
              className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 text-xs font-semibold flex items-center gap-2 transition"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Analyze Another
            </button>
          )}
        </div>

        {/* Error Notification */}
        {error && (
          <div className="p-4 rounded-xl bg-red-950/50 border border-red-800/80 text-red-300 text-sm flex items-start gap-3 animate-fadeIn">
            <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="font-semibold text-red-200">Analysis Error</p>
              <p className="text-xs text-red-300/90 mt-0.5">{error}</p>
            </div>
          </div>
        )}

        {/* PDF Upload Section (visible when no result yet) */}
        {!result && (
          <div className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl shadow-2xl space-y-6">
            <div className="text-center space-y-2">
              <h2 className="text-lg font-bold text-slate-200">Upload Scholarship PDF</h2>
              <p className="text-xs text-slate-400">Supported format: PDF up to 15 MB</p>
            </div>

            {/* Dropzone */}
            <label className="block cursor-pointer">
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleFileChange}
                disabled={loading}
                className="hidden"
              />
              <div className={`p-10 rounded-2xl border-2 border-dashed transition text-center flex flex-col items-center justify-center gap-3 ${
                selectedFile 
                  ? 'border-blue-500/60 bg-blue-950/20' 
                  : 'border-slate-800 hover:border-slate-700 bg-slate-950/40 hover:bg-slate-950/60'
              }`}>
                <div className="h-14 w-14 rounded-2xl bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                  <FileText className="w-7 h-7" />
                </div>

                {selectedFile ? (
                  <div>
                    <p className="font-semibold text-blue-300 text-sm">{selectedFile.name}</p>
                    <p className="text-xs text-slate-400 mt-1">
                      {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB &bull; Ready for analysis
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm font-medium text-slate-300">
                      Click to choose or drag & drop scholarship PDF
                    </p>
                    <p className="text-xs text-slate-500 mt-1">Extracts criteria deterministically without OCR</p>
                  </div>
                )}
              </div>
            </label>

            {/* Submit Button */}
            <div className="flex justify-end pt-2">
              <button
                onClick={handleAnalyze}
                disabled={!selectedFile || loading}
                className="w-full sm:w-auto px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white font-semibold text-sm transition flex items-center justify-center gap-2 shadow-lg shadow-blue-600/20 disabled:shadow-none disabled:text-slate-500"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" /> Analyzing Document with AI...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" /> Analyze Scholarship
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Structured Results Display */}
        {result && (
          <div className="space-y-8 animate-fadeIn">
            
            {/* Header & General Info Card */}
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800/80 backdrop-blur-xl shadow-xl space-y-6">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div className="space-y-2 max-w-2xl">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold">
                      {result.category || 'Scholarship'}
                    </span>
                    {result.provider && (
                      <span className="px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700 text-xs font-semibold flex items-center gap-1">
                        <Building2 className="w-3 h-3 text-slate-400" /> {result.provider}
                      </span>
                    )}
                  </div>

                  <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
                    {result.title}
                  </h2>

                  {result.description ? (
                    <p className="text-slate-300 text-sm leading-relaxed pt-1">
                      {result.description}
                    </p>
                  ) : (
                    <p className="text-slate-500 text-sm italic pt-1">
                      Description not specified in document.
                    </p>
                  )}
                </div>

                {result.official_url ? (
                  <a
                    href={result.official_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-4 py-2 rounded-xl bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/30 text-xs font-semibold flex items-center gap-1.5 transition shrink-0"
                  >
                    Official Application Site <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                ) : (
                  <span className="px-4 py-2 rounded-xl bg-slate-900 text-slate-500 border border-slate-800 text-xs font-semibold flex items-center gap-1.5 shrink-0">
                    URL Not Provided <ExternalLink className="w-3.5 h-3.5 opacity-50" />
                  </span>
                )}
              </div>

              {/* Quick Info Grid (Benefits & Deadline) */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-slate-800/80">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-start gap-3">
                  <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                    <Award className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Award / Benefit</p>
                    <p className="text-sm font-semibold text-slate-200 mt-0.5">
                      {result.benefit || 'Not specified in document'}
                    </p>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-start gap-3">
                  <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400">
                    <Calendar className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Application Deadline</p>
                    <p className="text-sm font-semibold text-slate-200 mt-0.5">
                      {result.deadline || 'Not specified in document'}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Eligibility Requirements Section */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-blue-400" /> Eligibility Requirements
                </h3>
                <span className="text-xs text-slate-400 bg-slate-900 px-2.5 py-1 rounded-full border border-slate-800">
                  {result.eligibility?.length || 0} Criteria
                </span>
              </div>

              {result.eligibility && result.eligibility.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {result.eligibility.map((req, idx) => (
                    <div key={idx} className="p-5 rounded-xl bg-slate-900/50 border border-slate-800/80 space-y-3">
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-950 text-blue-400 border border-blue-800/50 uppercase tracking-wider">
                          {req.requirement_type}
                        </span>
                        {req.mandatory ? (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-red-950/60 text-red-400 border border-red-900/50">
                            Mandatory
                          </span>
                        ) : (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                            Optional
                          </span>
                        )}
                      </div>

                      <div className="text-sm font-medium text-slate-200 leading-relaxed">
                        {req.description ? (
                          <p>{req.description}</p>
                        ) : (
                          <p>
                            Student must satisfy: <span className="font-semibold text-blue-300">{req.field.replace(/_/g, ' ')}</span>{' '}
                            {req.operator && <span className="text-slate-400">{req.operator}</span>}{' '}
                            {req.value && <span className="font-semibold text-emerald-300">{req.value}</span>}{' '}
                            {req.unit && <span className="text-slate-400">{req.unit}</span>}
                          </p>
                        )}
                      </div>

                      <details className="group">
                        <summary className="text-[11px] text-slate-500 hover:text-slate-400 cursor-pointer select-none flex items-center gap-1 transition-colors">
                          <Info className="w-3 h-3" /> View raw criteria & source
                        </summary>
                        <div className="mt-3 space-y-2 pl-4 border-l-2 border-slate-800">
                          <div className="font-mono text-[11px] text-slate-400 flex items-center gap-1.5 flex-wrap">
                            Raw: <span className="text-slate-300">{req.field}</span>
                            {req.operator && <span className="text-blue-400/80">{req.operator}</span>}
                            {req.value && <span className="text-emerald-400/80">{req.value}</span>}
                            {req.unit && <span>{req.unit}</span>}
                          </div>
                          {req.source_text && (
                            <div className="text-[11px] text-slate-500 italic">
                              Source: "{req.source_text}"
                            </div>
                          )}
                        </div>
                      </details>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800 text-center text-xs text-slate-500">
                  No explicit eligibility requirements extracted.
                </div>
              )}
            </div>

            {/* Required Documents Section */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <FileText className="w-5 h-5 text-indigo-400" /> Required Documents
                </h3>
                <span className="text-xs text-slate-400 bg-slate-900 px-2.5 py-1 rounded-full border border-slate-800">
                  {result.documents?.length || 0} Documents
                </span>
              </div>

              {result.documents && result.documents.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  {result.documents.map((doc, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/80 space-y-3 flex flex-col justify-between">
                      <div className="space-y-3">
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex items-start gap-2">
                            <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                            <span className="text-sm font-semibold text-slate-100">
                              {doc.name}
                            </span>
                          </div>
                          {doc.mandatory ? (
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-red-950/60 text-red-400 border border-red-900/50 shrink-0">
                              Mandatory
                            </span>
                          ) : (
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700 shrink-0">
                              Optional
                            </span>
                          )}
                        </div>

                        {doc.description && (
                          <p className="text-xs text-slate-300 pl-6">
                            {doc.description}
                          </p>
                        )}
                      </div>

                      <details className="group pl-6">
                        <summary className="text-[11px] text-slate-500 hover:text-slate-400 cursor-pointer select-none flex items-center gap-1 transition-colors">
                          <Info className="w-3 h-3" /> View source
                        </summary>
                        <div className="mt-2 pl-3 border-l-2 border-slate-800">
                          {doc.source_text ? (
                            <div className="text-[11px] text-slate-400 italic">
                              "{doc.source_text}"
                            </div>
                          ) : (
                            <div className="text-[11px] text-slate-500 italic">
                              Source text not provided.
                            </div>
                          )}
                        </div>
                      </details>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800 text-center text-xs text-slate-500">
                  No required documents explicitly listed.
                </div>
              )}
            </div>

            {/* Check My Eligibility Button */}
            <div className="flex justify-center pt-2">
              <button
                onClick={handleCheckEligibility}
                disabled={eligibilityLoading || !result?.id}
                className="px-8 py-3 rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 disabled:from-slate-800 disabled:to-slate-800 text-white font-bold text-sm transition flex items-center gap-2 shadow-lg shadow-emerald-600/20 disabled:shadow-none disabled:text-slate-500"
              >
                {eligibilityLoading ? (
                  <><RefreshCw className="w-4 h-4 animate-spin" /> Evaluating...</>
                ) : (
                  <><ShieldCheck className="w-5 h-5" /> Check My Eligibility</>
                )}
              </button>
            </div>

            {/* Eligibility Results */}
            {eligibilityResult && (
              <div className="space-y-6 animate-fadeIn">
                {/* Overall Status Banner */}
                <div className={`p-6 rounded-2xl border backdrop-blur-xl shadow-xl flex items-center gap-4 ${
                  eligibilityResult.status === 'ELIGIBLE' ? 'bg-emerald-950/50 border-emerald-800/80' :
                  eligibilityResult.status === 'INELIGIBLE' ? 'bg-red-950/50 border-red-800/80' :
                  'bg-amber-950/50 border-amber-800/80'
                }`}>
                  <div className={`text-4xl ${
                    eligibilityResult.status === 'ELIGIBLE' ? 'text-emerald-400' :
                    eligibilityResult.status === 'INELIGIBLE' ? 'text-red-400' :
                    'text-amber-400'
                  }`}>
                    {eligibilityResult.status === 'ELIGIBLE' ? '🟢' :
                     eligibilityResult.status === 'INELIGIBLE' ? '🔴' : '🟡'}
                  </div>
                  <div>
                    <h3 className={`text-xl font-bold ${
                      eligibilityResult.status === 'ELIGIBLE' ? 'text-emerald-300' :
                      eligibilityResult.status === 'INELIGIBLE' ? 'text-red-300' :
                      'text-amber-300'
                    }`}>
                      {eligibilityResult.status === 'ELIGIBLE' ? 'Eligible' :
                       eligibilityResult.status === 'INELIGIBLE' ? 'Not Eligible' :
                       'More Information Required'}
                    </h3>
                    <p className="text-sm text-slate-400 mt-1">
                      {eligibilityResult.passed.length} passed, {eligibilityResult.failed.length} failed, {eligibilityResult.unknown.length} unknown
                    </p>
                  </div>
                </div>

                {/* Passed Requirements */}
                {eligibilityResult.passed.length > 0 && (
                  <div className="space-y-3">
                    <h4 className="text-sm font-bold text-emerald-400 flex items-center gap-2">
                      <CheckCircle className="w-4 h-4" /> Passed ({eligibilityResult.passed.length})
                    </h4>
                    <div className="space-y-2">
                      {eligibilityResult.passed.map((e, i) => (
                        <div key={i} className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-900/40 space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-emerald-200">{e.requirement.description || e.requirement.field}</span>
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-900/50 text-emerald-400">PASS</span>
                          </div>
                          <p className="text-xs text-slate-400">{e.explanation}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Failed Requirements */}
                {eligibilityResult.failed.length > 0 && (
                  <div className="space-y-3">
                    <h4 className="text-sm font-bold text-red-400 flex items-center gap-2">
                      <AlertCircle className="w-4 h-4" /> Failed ({eligibilityResult.failed.length})
                    </h4>
                    <div className="space-y-2">
                      {eligibilityResult.failed.map((e, i) => (
                        <div key={i} className="p-4 rounded-xl bg-red-950/20 border border-red-900/40 space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-red-200">{e.requirement.description || e.requirement.field}</span>
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-red-900/50 text-red-400">FAIL</span>
                          </div>
                          <p className="text-xs text-slate-400">{e.explanation}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Unknown Requirements */}
                {eligibilityResult.unknown.length > 0 && (
                  <div className="space-y-3">
                    <h4 className="text-sm font-bold text-amber-400 flex items-center gap-2">
                      <Info className="w-4 h-4" /> Unknown ({eligibilityResult.unknown.length})
                    </h4>
                    <div className="space-y-2">
                      {eligibilityResult.unknown.map((e, i) => (
                        <div key={i} className="p-4 rounded-xl bg-amber-950/20 border border-amber-900/40 space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-amber-200">{e.requirement.description || e.requirement.field}</span>
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-900/50 text-amber-400">UNKNOWN</span>
                          </div>
                          <p className="text-xs text-slate-400">{e.explanation}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Document Readiness Checklist */}
                {eligibilityResult.documents.length > 0 && (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h4 className="text-sm font-bold text-indigo-400 flex items-center gap-2">
                        <FileText className="w-4 h-4" /> Required Application Documents Checklist
                      </h4>
                      <span className="text-xs text-slate-400 bg-slate-900 px-2.5 py-0.5 rounded-full border border-slate-800">
                        {eligibilityResult.documents.length} Items
                      </span>
                    </div>

                    <p className="text-xs text-slate-400 bg-slate-900/60 border border-slate-800/80 rounded-xl p-3 flex items-start gap-2">
                      <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
                      <span>Document checklist based on the opportunity requirements. PrepPath AI has not verified which documents you currently possess.</span>
                    </p>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {eligibilityResult.documents.map((d, i) => {
                        const isOptional = d.status === 'OPTIONAL';
                        const isAvailable = d.status === 'AVAILABLE';
                        const displayBadge = isOptional ? 'OPTIONAL' : isAvailable ? 'AVAILABLE' : 'REQUIRED';
                        
                        return (
                          <div key={i} className={`p-3.5 rounded-xl border flex items-center justify-between gap-3 ${
                            isAvailable ? 'bg-emerald-950/20 border-emerald-900/40' :
                            isOptional ? 'bg-slate-900/40 border-slate-800' :
                            'bg-slate-900/60 border-slate-800/80'
                          }`}>
                            <span className="text-sm font-medium text-slate-200">{d.document.name}</span>
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider shrink-0 ${
                              isAvailable ? 'bg-emerald-900/50 text-emerald-400 border border-emerald-800' :
                              isOptional ? 'bg-slate-800 text-slate-400 border border-slate-700' :
                              'bg-indigo-950/80 text-indigo-300 border border-indigo-800/60'
                            }`}>{displayBadge}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            )}

          </div>
        )}

      </div>
    </div>
  );
}
