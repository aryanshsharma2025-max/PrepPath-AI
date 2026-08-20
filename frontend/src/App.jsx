import React, { useState, useEffect } from 'react';
import { checkHealth } from './services/api';
import OpportunityAnalyzer from './pages/OpportunityAnalyzer';
import StudentProfile from './pages/StudentProfile';
import { 
  CheckCircle2, 
  AlertTriangle, 
  ArrowRight, 
  ShieldCheck, 
  GraduationCap, 
  FileText, 
  Sparkles,
  Activity,
  Server,
  User
} from 'lucide-react';

export default function App() {
  const [currentView, setCurrentView] = useState('landing'); // 'landing' | 'analyzer' | 'profile'
  const [apiStatus, setApiStatus] = useState({ status: 'checking', service: '' });
  const [loading, setLoading] = useState(false);

  const fetchHealth = async () => {
    setLoading(true);
    const res = await checkHealth();
    setApiStatus(res);
    setLoading(false);
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  if (currentView === 'analyzer') {
    return <OpportunityAnalyzer onBack={() => setCurrentView('landing')} />;
  }

  if (currentView === 'profile') {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100">
        <StudentProfile onBack={() => setCurrentView('landing')} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-blue-600 selection:text-white">
      {/* Background Glow Accents */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-600/15 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 -right-40 w-96 h-96 bg-indigo-600/15 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 left-1/3 w-96 h-96 bg-emerald-600/10 rounded-full blur-3xl"></div>
      </div>

      {/* Navigation Header */}
      <header className="relative z-10 border-b border-slate-800/80 bg-slate-900/50 backdrop-blur-md px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setCurrentView('landing')}>
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <GraduationCap className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                PrepPath AI
              </span>
              <span className="ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-950 text-blue-400 border border-blue-800/50">
                Scholarships MVP
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={() => setCurrentView('profile')}
              className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 font-semibold text-xs transition flex items-center gap-1.5 border border-slate-800"
            >
              <User className="w-3.5 h-3.5" /> My Profile
            </button>
            <button
              onClick={() => setCurrentView('analyzer')}
              className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition flex items-center gap-1.5 shadow-lg shadow-blue-600/20"
            >
              <Sparkles className="w-3.5 h-3.5" /> Analyze Scholarship PDF
            </button>

            <div className="hidden sm:flex items-center gap-2 text-xs font-medium px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800">
              <span className={`h-2 w-2 rounded-full ${apiStatus.status === 'healthy' ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
              <span className="text-slate-300">
                Backend: {apiStatus.status === 'healthy' ? 'Connected' : apiStatus.status === 'checking' ? 'Checking...' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 max-w-6xl mx-auto px-6 py-16 flex-1 flex flex-col justify-center">
        <div className="text-center space-y-6 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold tracking-wide uppercase">
            <Sparkles className="w-3.5 h-3.5" /> Opportunity-to-Application Readiness
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight">
            PrepPath AI
          </h1>

          <p className="text-xl sm:text-2xl font-medium bg-gradient-to-r from-blue-400 via-indigo-300 to-slate-200 bg-clip-text text-transparent">
            From Opportunity to Application-Ready
          </p>

          <p className="text-slate-400 text-base sm:text-lg leading-relaxed pt-2 max-w-2xl mx-auto">
            Bridge the gap between being <strong className="text-slate-200">eligible</strong> for a scholarship and being <strong className="text-slate-200">application-ready</strong>. Powered by deterministic eligibility rules and intelligent document analysis.
          </p>

          <div className="pt-4 flex justify-center">
            <button
              onClick={() => setCurrentView('analyzer')}
              className="px-8 py-4 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-base transition flex items-center gap-2 shadow-xl shadow-blue-600/25 transform hover:-translate-y-0.5"
            >
              <Sparkles className="w-5 h-5" /> Analyze Scholarship PDF <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Backend Connectivity Status Box */}
        <div className="mt-12 max-w-xl mx-auto w-full">
          <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 backdrop-blur-xl shadow-2xl space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Server className="w-5 h-5 text-blue-400" />
                <h3 className="text-sm font-semibold text-slate-200">API Gateway Status</h3>
              </div>
              <button
                onClick={fetchHealth}
                disabled={loading}
                className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1.5 disabled:opacity-50"
              >
                <Activity className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
                Ping API
              </button>
            </div>

            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 font-mono text-xs text-slate-300">
              <div className="flex justify-between items-center py-1">
                <span className="text-slate-500">Endpoint:</span>
                <span className="text-blue-400">GET /health</span>
              </div>
              <div className="flex justify-between items-center py-1 border-t border-slate-900">
                <span className="text-slate-500">Service:</span>
                <span>{apiStatus.service || 'PrepPath AI API'}</span>
              </div>
              <div className="flex justify-between items-center py-1 border-t border-slate-900">
                <span className="text-slate-500">Status:</span>
                <span className={apiStatus.status === 'healthy' ? 'text-emerald-400 font-bold' : 'text-amber-400'}>
                  {apiStatus.status}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Product Architecture Pillars */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800/80 space-y-2">
            <div className="h-8 w-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-slate-200">1. Eligibility</h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              Deterministic rule engine verifies hard age, academic, and demographic criteria.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800/80 space-y-2">
            <div className="h-8 w-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <FileText className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-slate-200">2. Application Readiness</h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              Calculates readiness score based on available vs required documents.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800/80 space-y-2">
            <div className="h-8 w-8 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
              <AlertTriangle className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-slate-200">3. Application Risk</h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              Detects profile inconsistencies and impending opportunity deadlines.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800/80 space-y-2">
            <div className="h-8 w-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <ArrowRight className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-slate-200">4. Next Best Action</h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              Actionable recommendations to bridge gaps and complete applications.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        <p>PrepPath AI &copy; 2026 &bull; Architecture Extensible for Scholarships, Internships, Fellowships & Competitions</p>
      </footer>
    </div>
  );
}
