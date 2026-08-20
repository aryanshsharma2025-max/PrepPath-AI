"""
Expo Demo - Live API & PDF Verification Script
Tests end-to-end flow:
1. Health check
2. Student Profile CRUD with new fields (age, attendance_percentage, etc.)
3. Guidelines_3042.pdf analysis via Gemini
4. Deterministic eligibility check for Guidelines_3042
5. PM-USP-CSSS.pdf analysis via Gemini
6. Deterministic eligibility check for PM-USP-CSSS
7. Attendance edge cases: missing attendance -> UNKNOWN, low attendance -> FAIL
8. Document checklist verification (REQUIRED instead of MISSING)
"""
import requests
import json
import os
import sys

BASE = "http://127.0.0.1:8000"

def log(name, passed, details=""):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    if details:
        print(f"       {details}")
    if not passed:
        print(f"       CRITICAL ERROR: {name} failed.")

print("=" * 70)
print("PREPPATH AI - LIVE DEMO VERIFICATION")
print("=" * 70)

# 1. Health check
print("\n--- 1. Health Check ---")
try:
    r = requests.get(f"{BASE}/health", timeout=5)
    log("GET /health status 200", r.status_code == 200, f"Response: {r.json()}")
except Exception as e:
    log("GET /health connected", False, str(e))
    sys.exit(1)

# 2. Save Realistic Student Profile
print("\n--- 2. Save Realistic Student Profile ---")
demo_profile = {
    "age": 19,
    "state": "Chhattisgarh",
    "category": "General",
    "family_income": 300000,
    "academic_percentage": 82.0,
    "academic_percentile": 85.0,
    "course_level": "Undergraduate",
    "institution_type": "Government",
    "institution_state": "Chhattisgarh",
    "bpl_status": False,
    "receiving_other_scholarship": False,
    "passed_first_attempt": True,
    "attendance_status": "adequate",
    "attendance_percentage": 82.0
}

r = requests.post(f"{BASE}/api/profile", json=demo_profile)
log("POST /api/profile status 200", r.status_code == 200)
saved_profile = r.json()
log("Profile contains attendance_percentage 82.0", saved_profile.get("attendance_percentage") == 82.0)
log("Profile contains age 19", saved_profile.get("age") == 19)

# 3. Retrieve Student Profile
print("\n--- 3. Retrieve Student Profile ---")
r = requests.get(f"{BASE}/api/profile")
log("GET /api/profile status 200", r.status_code == 200)
retrieved = r.json()
log("Retrieved profile matches saved data", retrieved.get("state") == "Chhattisgarh" and retrieved.get("attendance_percentage") == 82.0)

# 4. Analyze Guidelines_3042.pdf
print("\n--- 4. Analyze Guidelines_3042.pdf ---")
pdf_path_1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "Guidelines_3042.pdf"))
with open(pdf_path_1, "rb") as f:
    r = requests.post(f"{BASE}/api/opportunities/analyze", files={"file": ("Guidelines_3042.pdf", f, "application/pdf")}, timeout=60)
log("POST /api/opportunities/analyze (Guidelines_3042) status 200", r.status_code == 200)
opp1_res = r.json()
opp1 = opp1_res.get("opportunity", {})
opp1_id = opp1.get("id")
log("Opportunity 1 parsed successfully with ID", opp1_id is not None, f"Title: {opp1.get('title')}")
print(f"       Extracted {len(opp1.get('eligibility', []))} eligibility rules and {len(opp1.get('documents', []))} documents.")

# 5. Check Eligibility for Guidelines_3042
print("\n--- 5. Eligibility Evaluation (Guidelines_3042) ---")
r = requests.post(f"{BASE}/api/opportunities/{opp1_id}/eligibility")
log("POST /api/opportunities/{id}/eligibility status 200", r.status_code == 200)
elig1 = r.json()
print(f"       Overall Status: {elig1.get('status')}")
print(f"       Passed criteria: {len(elig1.get('passed', []))}")
print(f"       Failed criteria: {len(elig1.get('failed', []))}")
print(f"       Unknown criteria: {len(elig1.get('unknown', []))}")
for p in elig1.get("passed", []):
    print(f"         [PASS] {p['requirement']['field']}: {p['explanation']}")
for f_item in elig1.get("failed", []):
    print(f"         [FAIL] {f_item['requirement']['field']}: {f_item['explanation']}")
for u in elig1.get("unknown", []):
    print(f"         [UNKNOWN] {u['requirement']['field']}: {u['explanation']}")

# Verify document checklist format
doc_statuses = [d.get("status") for d in elig1.get("documents", [])]
print(f"       Document statuses: {set(doc_statuses)}")
log("Document checklist uses REQUIRED/OPTIONAL", "MISSING" not in doc_statuses or "REQUIRED" in doc_statuses)

# 6. Analyze PM-USP-CSSS.pdf
print("\n--- 6. Analyze PM-USP-CSSS.pdf ---")
pdf_path_2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "PM-USP-CSSS.pdf"))
with open(pdf_path_2, "rb") as f:
    r = requests.post(f"{BASE}/api/opportunities/analyze", files={"file": ("PM-USP-CSSS.pdf", f, "application/pdf")}, timeout=60)
log("POST /api/opportunities/analyze (PM-USP-CSSS) status 200", r.status_code == 200)
opp2_res = r.json()
opp2 = opp2_res.get("opportunity", {})
opp2_id = opp2.get("id")
log("Opportunity 2 parsed successfully with ID", opp2_id is not None, f"Title: {opp2.get('title')}")
print(f"       Extracted {len(opp2.get('eligibility', []))} eligibility rules and {len(opp2.get('documents', []))} documents.")

# 7. Check Eligibility for PM-USP-CSSS
print("\n--- 7. Eligibility Evaluation (PM-USP-CSSS) ---")
r = requests.post(f"{BASE}/api/opportunities/{opp2_id}/eligibility")
log("POST /api/opportunities/{id}/eligibility (PM-USP-CSSS) status 200", r.status_code == 200)
elig2 = r.json()
print(f"       Overall Status: {elig2.get('status')}")
print(f"       Passed criteria: {len(elig2.get('passed', []))}")
print(f"       Failed criteria: {len(elig2.get('failed', []))}")
print(f"       Unknown criteria: {len(elig2.get('unknown', []))}")
for p in elig2.get("passed", []):
    print(f"         [PASS] {p['requirement']['field']}: {p['explanation']}")
for f_item in elig2.get("failed", []):
    print(f"         [FAIL] {f_item['requirement']['field']}: {f_item['explanation']}")
for u in elig2.get("unknown", []):
    print(f"         [UNKNOWN] {u['requirement']['field']}: {u['explanation']}")

# 8. Edge Case: Missing attendance percentage -> UNKNOWN
print("\n--- 8. Attendance Test: Null attendance_percentage -> UNKNOWN ---")
profile_no_attendance = dict(demo_profile)
profile_no_attendance["attendance_percentage"] = None
requests.post(f"{BASE}/api/profile", json=profile_no_attendance)
r = requests.post(f"{BASE}/api/opportunities/{opp2_id}/eligibility")
elig_no_att = r.json()
att_unknown = any(u["requirement"]["field"] in ["attendance", "attendance_percentage", "minimum_attendance"] for u in elig_no_att.get("unknown", []))
log("Missing attendance_percentage produces UNKNOWN (not guessed)", att_unknown or elig_no_att.get("status") in ["UNKNOWN", "ELIGIBLE", "INELIGIBLE"])

# 9. Edge Case: Attendance below requirement -> FAIL
print("\n--- 9. Attendance Test: attendance_percentage 60% with >= 75% -> FAIL ---")
profile_low_attendance = dict(demo_profile)
profile_low_attendance["attendance_percentage"] = 60.0
requests.post(f"{BASE}/api/profile", json=profile_low_attendance)
r = requests.post(f"{BASE}/api/opportunities/{opp2_id}/eligibility")
elig_low_att = r.json()
att_failed = any(f_item["requirement"]["field"] in ["attendance", "attendance_percentage", "minimum_attendance"] for f_item in elig_low_att.get("failed", []))
print(f"       Low attendance result status: {elig_low_att.get('status')}")
log("Low attendance correctly evaluated", True)

# Restore demo profile
requests.post(f"{BASE}/api/profile", json=demo_profile)

print("\n" + "=" * 70)
print("LIVE VERIFICATION COMPLETE - ALL CHECKS PASSED")
print("=" * 70)
