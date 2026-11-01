"""
Automated Integration and Smoke Test Suite for AI Lab Record Generator
Supports testing:
- Running local Flask instance (http://127.0.0.1:5000)
- In-memory Flask Test Client (standalone without separate server process)
- Remote live Vercel endpoint (pass URL as argument or env var)
"""

import sys
import os
import requests
import json

# Target server URL or in-memory fallback
TARGET_URL = os.environ.get("TEST_SERVER_URL", "http://127.0.0.1:5000")

def run_tests_via_http(base_url):
    print(f"[*] Running integration tests against HTTP server: {base_url}\n")
    test_cases = [
        ("CS - Binary Search", {"Subject": "Computer Science", "Experiment": "Binary Search", "Username": "Ranjith"}, {"Aim", "Algorithm", "Code", "Output", "Result"}),
        ("Physics - Ohm's Law", {"Subject": "Physics", "Experiment": "Ohm's Law", "Username": "Ranjith"}, {"Aim", "Theory", "Procedure", "Observation", "Result"}),
        ("Chemistry - Titration", {"Subject": "Chemistry", "Experiment": "Acid Base Titration", "Username": "Ranjith"}, {"Aim", "Theory", "Procedure", "Observation", "Result"}),
        ("Biology - Mitosis", {"Subject": "Biology", "Experiment": "Mitosis in Onion Root Tip", "Username": "Ranjith"}, {"Aim", "Theory", "Procedure", "Observation", "Result"}),
    ]

    passed = 0
    for name, payload, expected_keys in test_cases:
        print(f"=== {name} ===")
        try:
            r = requests.post(f"{base_url}/generate", json=payload, timeout=8)
            print(f"STATUS: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                keys_present = set(data.keys())
                missing = expected_keys - keys_present
                if not missing:
                    print(f"  [PASS] All expected keys present: {expected_keys}")
                    for k in sorted(data.keys()):
                        print(f"    - {k}: {str(data[k])[:70]}...")
                    passed += 1
                else:
                    print(f"  [FAIL] Missing keys: {missing}")
            else:
                print(f"  [FAIL] HTTP status {r.status_code}: {r.text[:120]}")
        except Exception as e:
            print(f"  [ERROR] {e}")
        print()

    print(f"[*] HTTP Test Results: {passed}/{len(test_cases)} passed.")
    return passed == len(test_cases)

def run_tests_via_client():
    print("[*] Local server not active. Testing directly via Flask Test Client...\n")
    import app as lab_app
    client = lab_app.app.test_client()

    test_cases = [
        ("CS - Stack Operations", {"Subject": "Computer Science", "Experiment": "Stack Operations"}, {"Aim", "Algorithm", "Code", "Output", "Result"}),
        ("Physics - Vernier Calipers", {"Subject": "Physics", "Experiment": "Vernier Calipers"}, {"Aim", "Theory", "Procedure", "Observation", "Result"}),
        ("Chemistry - EDTA Hardness", {"Subject": "Chemistry", "Experiment": "Hardness of Water by EDTA"}, {"Aim", "Theory", "Procedure", "Observation", "Result"}),
        ("Biology - DNA Extraction", {"Subject": "Biology", "Experiment": "Isolation of DNA from Banana"}, {"Aim", "Theory", "Procedure", "Observation", "Result"}),
    ]

    passed = 0
    for name, payload, expected_keys in test_cases:
        print(f"=== {name} ===")
        res = client.post("/generate", json=payload)
        print(f"STATUS: {res.status_code}")
        if res.status_code == 200:
            data = res.get_json()
            keys_present = set(data.keys())
            missing = expected_keys - keys_present
            if not missing:
                print(f"  [PASS] All expected keys present: {expected_keys}")
                for k in sorted(data.keys()):
                    print(f"    - {k}: {str(data[k])[:70]}...")
                passed += 1
            else:
                print(f"  [FAIL] Missing keys: {missing}")
        else:
            print(f"  [FAIL] HTTP {res.status_code}")
        print()

    print(f"[*] Flask Test Client Results: {passed}/{len(test_cases)} passed.")
    return passed == len(test_cases)

if __name__ == "__main__":
    # Check if HTTP server is reachable
    is_server_up = False
    try:
        r = requests.get(TARGET_URL, timeout=1.5)
        is_server_up = True
    except Exception:
        is_server_up = False

    if is_server_up:
        success = run_tests_via_http(TARGET_URL)
    else:
        success = run_tests_via_client()

    sys.exit(0 if success else 1)
