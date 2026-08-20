import React, { useState, useEffect } from 'react';
import { getProfile, updateProfile } from '../services/api';
import { User, Save, RefreshCw, ArrowLeft, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function StudentProfile({ onBack }) {
  const [profile, setProfile] = useState({
    age: '',
    state: '',
    category: '',
    family_income: '',
    academic_percentage: '',
    academic_percentile: '',
    course_level: '',
    institution_type: '',
    institution_state: '',
    bpl_status: '',
    receiving_other_scholarship: '',
    passed_first_attempt: '',
    attendance_status: '',
    attendance_percentage: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    async function load() {
      const data = await getProfile();
      if (data) {
        setProfile({
          age: data.age !== null && data.age !== undefined ? String(data.age) : '',
          state: data.state || '',
          category: data.category || '',
          family_income: data.family_income !== null && data.family_income !== undefined ? String(data.family_income) : '',
          academic_percentage: data.academic_percentage !== null && data.academic_percentage !== undefined ? String(data.academic_percentage) : '',
          academic_percentile: data.academic_percentile !== null && data.academic_percentile !== undefined ? String(data.academic_percentile) : '',
          course_level: data.course_level || '',
          institution_type: data.institution_type || '',
          institution_state: data.institution_state || '',
          bpl_status: data.bpl_status !== null && data.bpl_status !== undefined ? String(data.bpl_status) : '',
          receiving_other_scholarship: data.receiving_other_scholarship !== null && data.receiving_other_scholarship !== undefined ? String(data.receiving_other_scholarship) : '',
          passed_first_attempt: data.passed_first_attempt !== null && data.passed_first_attempt !== undefined ? String(data.passed_first_attempt) : '',
          attendance_status: data.attendance_status || '',
          attendance_percentage: data.attendance_percentage !== null && data.attendance_percentage !== undefined ? String(data.attendance_percentage) : ''
        });
      }
      setLoading(false);
    }
    load();
  }, []);

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
    setMessage('');
    setErrorMsg('');
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setMessage('');
    setErrorMsg('');

    // Age validation: integer, 1 to 120
    let parsedAge = null;
    if (profile.age !== '' && profile.age !== null && profile.age !== undefined) {
      const numAge = Number(profile.age);
      if (!Number.isInteger(numAge) || numAge < 1 || numAge > 120) {
        setErrorMsg('Age must be a whole number between 1 and 120.');
        return;
      }
      parsedAge = numAge;
    }

    // Attendance percentage validation: numeric, 0 to 100
    let parsedAttendance = null;
    if (profile.attendance_percentage !== '' && profile.attendance_percentage !== null && profile.attendance_percentage !== undefined) {
      const numAtt = Number(profile.attendance_percentage);
      if (isNaN(numAtt) || numAtt < 0 || numAtt > 100) {
        setErrorMsg('Attendance percentage must be a number between 0 and 100.');
        return;
      }
      parsedAttendance = numAtt;
    }

    // Academic percentage validation: numeric, 0 to 100
    let parsedAcademicPct = null;
    if (profile.academic_percentage !== '' && profile.academic_percentage !== null && profile.academic_percentage !== undefined) {
      const numAcad = Number(profile.academic_percentage);
      if (isNaN(numAcad) || numAcad < 0 || numAcad > 100) {
        setErrorMsg('Academic percentage must be a number between 0 and 100.');
        return;
      }
      parsedAcademicPct = numAcad;
    }

    // Academic percentile validation: numeric, 0 to 100
    let parsedPercentile = null;
    if (profile.academic_percentile !== '' && profile.academic_percentile !== null && profile.academic_percentile !== undefined) {
      const numPct = Number(profile.academic_percentile);
      if (isNaN(numPct) || numPct < 0 || numPct > 100) {
        setErrorMsg('Academic percentile must be a number between 0 and 100.');
        return;
      }
      parsedPercentile = numPct;
    }

    // Family income validation
    let parsedIncome = null;
    if (profile.family_income !== '' && profile.family_income !== null && profile.family_income !== undefined) {
      const numInc = Number(profile.family_income);
      if (isNaN(numInc) || numInc < 0) {
        setErrorMsg('Annual family income must be a positive number.');
        return;
      }
      parsedIncome = Math.round(numInc);
    }

    setSaving(true);
    
    // Convert to proper types
    const payload = {
      age: parsedAge,
      state: profile.state.trim() || null,
      category: profile.category || null,
      family_income: parsedIncome,
      academic_percentage: parsedAcademicPct,
      academic_percentile: parsedPercentile,
      course_level: profile.course_level || null,
      institution_type: profile.institution_type || null,
      institution_state: profile.institution_state.trim() || null,
      bpl_status: profile.bpl_status === 'true' ? true : profile.bpl_status === 'false' ? false : null,
      receiving_other_scholarship: profile.receiving_other_scholarship === 'true' ? true : profile.receiving_other_scholarship === 'false' ? false : null,
      passed_first_attempt: profile.passed_first_attempt === 'true' ? true : profile.passed_first_attempt === 'false' ? false : null,
      attendance_status: profile.attendance_status.trim() || null,
      attendance_percentage: parsedAttendance
    };

    const res = await updateProfile(payload);
    if (res) {
      setMessage('Profile saved successfully!');
    } else {
      setErrorMsg('Failed to save profile. Please check your backend connection.');
    }
    setSaving(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-8">
      <div className="flex items-center gap-4 mb-8">
        <button
          onClick={onBack}
          className="p-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-800 transition"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
            <User className="w-7 h-7 text-indigo-500" /> Student Profile
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Complete your profile to enable deterministic eligibility evaluation.
          </p>
        </div>
      </div>

      <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 sm:p-8 shadow-xl">
        {message && (
          <div className="p-4 rounded-xl mb-6 text-sm font-medium border bg-emerald-900/30 text-emerald-400 border-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            {message}
          </div>
        )}

        {errorMsg && (
          <div className="p-4 rounded-xl mb-6 text-sm font-medium border bg-red-900/30 text-red-400 border-red-800 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Age */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Age</label>
              <input 
                type="number" 
                name="age" 
                value={profile.age} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition" 
                placeholder="e.g., 19 (1-120)" 
              />
            </div>

            {/* State / Domicile */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">State / Domicile</label>
              <input 
                type="text" 
                name="state" 
                value={profile.state} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition" 
                placeholder="e.g., Chhattisgarh" 
              />
            </div>

            {/* Category */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Category</label>
              <select 
                name="category" 
                value={profile.category} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition"
              >
                <option value="">Not provided</option>
                <option value="General">General</option>
                <option value="OBC">OBC</option>
                <option value="SC">SC</option>
                <option value="ST">ST</option>
                <option value="EWS">EWS</option>
              </select>
            </div>

            {/* Annual Family Income */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Annual Family Income (₹)</label>
              <input 
                type="number" 
                name="family_income" 
                value={profile.family_income} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition" 
                placeholder="e.g., 300000" 
              />
            </div>

            {/* Academic Percentage */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Academic Percentage (%)</label>
              <input 
                type="number" 
                step="0.01" 
                name="academic_percentage" 
                value={profile.academic_percentage} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition" 
                placeholder="e.g., 82.0 (0-100)" 
              />
            </div>

            {/* Academic Percentile */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Academic Percentile</label>
              <input 
                type="number" 
                step="0.01" 
                name="academic_percentile" 
                value={profile.academic_percentile} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition" 
                placeholder="e.g., 85.0 (0-100)" 
              />
            </div>

            {/* Attendance Percentage */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Attendance Percentage (%)</label>
              <input 
                type="number" 
                step="0.01" 
                name="attendance_percentage" 
                value={profile.attendance_percentage} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition" 
                placeholder="e.g., 82.0 (0-100)" 
              />
            </div>

            {/* Course Level */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Course / Degree Level</label>
              <select 
                name="course_level" 
                value={profile.course_level} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition"
              >
                <option value="">Not provided</option>
                <option value="Undergraduate">Undergraduate</option>
                <option value="Postgraduate">Postgraduate</option>
                <option value="Diploma">Diploma</option>
                <option value="PhD">PhD</option>
              </select>
            </div>

            {/* Institution Type */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Institution Type</label>
              <select 
                name="institution_type" 
                value={profile.institution_type} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition"
              >
                <option value="">Not provided</option>
                <option value="Government">Government / Public</option>
                <option value="Private">Private</option>
                <option value="Aided">Aided</option>
              </select>
            </div>

            {/* Institution State */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Institution State</label>
              <input 
                type="text" 
                name="institution_state" 
                value={profile.institution_state} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition" 
                placeholder="e.g., Chhattisgarh" 
              />
            </div>

            {/* BPL Status */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">BPL (Below Poverty Line) Status</label>
              <select 
                name="bpl_status" 
                value={profile.bpl_status} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition"
              >
                <option value="">Not provided</option>
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </div>

            {/* Passed in First Attempt */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Passed in First Attempt?</label>
              <select 
                name="passed_first_attempt" 
                value={profile.passed_first_attempt} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition"
              >
                <option value="">Not provided</option>
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </div>

            {/* Receiving Another Scholarship */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Receiving Another Scholarship?</label>
              <select 
                name="receiving_other_scholarship" 
                value={profile.receiving_other_scholarship} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition"
              >
                <option value="">Not provided</option>
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </div>

            {/* Attendance Status (Qualitative) */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Qualitative Attendance Status</label>
              <input 
                type="text" 
                name="attendance_status" 
                value={profile.attendance_status} 
                onChange={handleChange} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition" 
                placeholder="e.g., adequate / regular / satisfactory" 
              />
            </div>

          </div>

          <div className="pt-6 border-t border-slate-800 flex justify-end">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white font-semibold text-sm transition flex items-center gap-2 shadow-lg shadow-indigo-600/20"
            >
              {saving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              Save Profile
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

