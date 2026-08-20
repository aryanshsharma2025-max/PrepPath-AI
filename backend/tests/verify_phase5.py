"""Live API verification script for Phase 5"""
import requests
import json
import sys

BASE = "http://127.0.0.1:8000"

def test(name, result):
    status = "PASS" if result else "FAIL"
    print(f"  [{status}] {name}")
    return result

print("=" * 60)
print("Phase 5 - Live API Verification")
print("=" * 60)

# 1. Health check
print("\n1. Health Check")
r = requests.get(f"{BASE}/health")
test("GET /health returns 200", r.status_code == 200)
print(f"  Response: {r.json()}")

# 2. Create/Update student profile
print("\n2. Create/Update Student Profile")
profile_data = {
    "state": "Maharashtra",
    "category": "General",
    "family_income": 300000,
    "academic_percentage": 85.5,
    "academic_percentile": 90.0,
    "course_level": "Undergraduate",
    "institution_type": "Government",
    "bpl_status": True,
    "receiving_other_scholarship": False,
    "passed_first_attempt": True,
    "attendance_status": "adequate"
}
r = requests.post(f"{BASE}/api/profile", json=profile_data)
test("POST /api/profile returns 200", r.status_code == 200)
profile_result = r.json()
print(f"  Profile saved: family_income={profile_result.get('family_income')}, bpl={profile_result.get('bpl_status')}")

# 3. Retrieve profile
print("\n3. Retrieve Student Profile")
r = requests.get(f"{BASE}/api/profile")
test("GET /api/profile returns 200", r.status_code == 200)
retrieved = r.json()
test("Profile family_income matches", retrieved.get("family_income") == 300000)
test("Profile bpl_status matches", retrieved.get("bpl_status") == True)
test("Profile academic_percentage matches", retrieved.get("academic_percentage") == 85.5)

# 4. Analyze Guidelines_3042.pdf
print("\n4. Analyze Guidelines_3042.pdf")
with open(r"..\data\Guidelines_3042.pdf", "rb") as f:
    r = requests.post(f"{BASE}/api/opportunities/analyze", files={"file": ("Guidelines_3042.pdf", f, "application/pdf")})
test("POST /api/opportunities/analyze returns 200", r.status_code == 200)
opp1 = r.json()
opp1_data = opp1.get("opportunity", {})
opp1_id = opp1_data.get("id")
test("Guidelines_3042 has opportunity ID", opp1_id is not None)
print(f"  Opportunity ID: {opp1_id}")
print(f"  Title: {opp1_data.get('title')}")
print(f"  Requirements: {len(opp1_data.get('eligibility', []))}")
print(f"  Documents: {len(opp1_data.get('documents', []))}")

# 5. Eligibility check for Guidelines_3042
print("\n5. Eligibility Check: Guidelines_3042 (Profile with all fields)")
r = requests.post(f"{BASE}/api/opportunities/{opp1_id}/eligibility")
test("POST eligibility returns 200", r.status_code == 200)
elig1 = r.json()
print(f"  Status: {elig1.get('status')}")
print(f"  Passed: {len(elig1.get('passed', []))}")
print(f"  Failed: {len(elig1.get('failed', []))}")
print(f"  Unknown: {len(elig1.get('unknown', []))}")
print(f"  Documents: {len(elig1.get('documents', []))}")
for p in elig1.get("passed", []):
    print(f"    PASS: {p['requirement']['field']} - {p['explanation']}")
for f_item in elig1.get("failed", []):
    print(f"    FAIL: {f_item['requirement']['field']} - {f_item['explanation']}")
for u in elig1.get("unknown", []):
    print(f"    UNKNOWN: {u['requirement']['field']} - {u['explanation']}")

# 6. Analyze PM-USP-CSSS.pdf
print("\n6. Analyze PM-USP-CSSS.pdf")
with open(r"..\data\PM-USP-CSSS.pdf", "rb") as f:
    r = requests.post(f"{BASE}/api/opportunities/analyze", files={"file": ("PM-USP-CSSS.pdf", f, "application/pdf")})
test("POST /api/opportunities/analyze returns 200", r.status_code == 200)
opp2 = r.json()
opp2_data = opp2.get("opportunity", {})
opp2_id = opp2_data.get("id")
test("PM-USP-CSSS has opportunity ID", opp2_id is not None)
print(f"  Opportunity ID: {opp2_id}")
print(f"  Title: {opp2_data.get('title')}")
print(f"  Requirements: {len(opp2_data.get('eligibility', []))}")
print(f"  Documents: {len(opp2_data.get('documents', []))}")

# 7. Eligibility check for PM-USP-CSSS
print("\n7. Eligibility Check: PM-USP-CSSS (Profile with all fields)")
r = requests.post(f"{BASE}/api/opportunities/{opp2_id}/eligibility")
test("POST eligibility returns 200", r.status_code == 200)
elig2 = r.json()
print(f"  Status: {elig2.get('status')}")
print(f"  Passed: {len(elig2.get('passed', []))}")
print(f"  Failed: {len(elig2.get('failed', []))}")
print(f"  Unknown: {len(elig2.get('unknown', []))}")
for p in elig2.get("passed", []):
    print(f"    PASS: {p['requirement']['field']} - {p['explanation']}")
for f_item in elig2.get("failed", []):
    print(f"    FAIL: {f_item['requirement']['field']} - {f_item['explanation']}")
for u in elig2.get("unknown", []):
    print(f"    UNKNOWN: {u['requirement']['field']} - {u['explanation']}")

# 8. Test UNKNOWN behavior with missing income
print("\n8. Test UNKNOWN: Update profile with missing income")
missing_income_profile = {
    "state": "Maharashtra",
    "category": "General",
    "family_income": None,
    "academic_percentage": 85.5,
    "bpl_status": True,
    "receiving_other_scholarship": False,
    "passed_first_attempt": True
}
r = requests.post(f"{BASE}/api/profile", json=missing_income_profile)
test("Profile update with null income returns 200", r.status_code == 200)

r = requests.post(f"{BASE}/api/opportunities/{opp2_id}/eligibility")
elig_unknown = r.json()
print(f"  Status: {elig_unknown.get('status')}")
has_unknown_income = any(
    u["requirement"]["field"] == "family_income" for u in elig_unknown.get("unknown", [])
)
test("Missing income produces UNKNOWN (not PASS or FAIL)", has_unknown_income)

# 9. Test INELIGIBLE: income too high
print("\n9. Test INELIGIBLE: income exceeds limit")
high_income = {
    "state": "Maharashtra",
    "category": "General",
    "family_income": 800000,
    "academic_percentage": 85.5,
    "academic_percentile": 90.0,
    "bpl_status": True,
    "receiving_other_scholarship": False,
    "passed_first_attempt": True
}
r = requests.post(f"{BASE}/api/profile", json=high_income)
r = requests.post(f"{BASE}/api/opportunities/{opp2_id}/eligibility")
elig_fail = r.json()
print(f"  Status: {elig_fail.get('status')}")
has_failed_income = any(
    f_item["requirement"]["field"] == "family_income" for f_item in elig_fail.get("failed", [])
)
test("High income produces FAIL for family_income", has_failed_income)

# 10. Test optional requirement doesn't make INELIGIBLE  
print("\n10. Test optional requirement failure does not make INELIGIBLE")
# Check if any optional-only failures exist in elig1 but status is still ELIGIBLE
optional_failures = [f_item for f_item in elig1.get("failed", []) if not f_item["requirement"]["mandatory"]]
mandatory_failures = [f_item for f_item in elig1.get("failed", []) if f_item["requirement"]["mandatory"]]
if optional_failures and not mandatory_failures:
    test("Optional failures alone do not produce INELIGIBLE", elig1.get("status") != "INELIGIBLE")
else:
    print("  (Skipped - no isolated optional-only failure scenario in this dataset)")

# 11. 404 for nonexistent opportunity
print("\n11. Test 404 for nonexistent opportunity")
r = requests.post(f"{BASE}/api/opportunities/nonexistent-id-999/eligibility")
test("Nonexistent opportunity returns 404", r.status_code == 404)

# Restore original profile
print("\n12. Restore original profile")
requests.post(f"{BASE}/api/profile", json=profile_data)
print("  Profile restored.")

print("\n" + "=" * 60)
print("Live API Verification Complete")
print("=" * 60)
