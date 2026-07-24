import requests
import json

# Test 1: CS Subject - Binary Search
print("=== TEST 1: CS - Binary Search ===")
r = requests.post('http://127.0.0.1:5000/generate',
    json={'Subject': 'Computer Science', 'Experiment': 'Binary Search', 'Username': 'Ranjith'}, timeout=5)
print('STATUS:', r.status_code)
data = r.json()
for k, v in data.items():
    print(f"  {k}: {str(v)[:80]}")

print()

# Test 2: Physics Subject - Ohm's Law
print("=== TEST 2: Physics - Ohm's Law ===")
r2 = requests.post('http://127.0.0.1:5000/generate',
    json={'Subject': 'Physics', 'Experiment': "Ohm's Law", 'Username': 'Ranjith'}, timeout=5)
print('STATUS:', r2.status_code)
data2 = r2.json()
for k, v in data2.items():
    print(f"  {k}: {str(v)[:80]}")

print()

# Test 3: Generic Science Subject
print("=== TEST 3: Chemistry - Titration ===")
r3 = requests.post('http://127.0.0.1:5000/generate',
    json={'Subject': 'Chemistry', 'Experiment': 'Acid Base Titration', 'Username': 'Ranjith'}, timeout=5)
print('STATUS:', r3.status_code)
data3 = r3.json()
for k, v in data3.items():
    print(f"  {k}: {str(v)[:80]}")
