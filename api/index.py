from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import sys

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Hugging Face setup — token read from environment variable for security
HF_TOKEN = os.environ.get("HF_TOKEN", "")
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_fallback_record(subject, experiment):
    subj_lower = subject.lower() if subject else ""
    exp_lower = experiment.lower() if experiment else ""
    
    # Check if CS/programming subject - use exact word matching to avoid 'cs' matching inside 'physics'
    cs_subjects = {"computer science", "cs", "cse", "programming", "python", "java", "c++", "data structure"}
    subj_words = set(subj_lower.replace(',', ' ').split())
    is_cs = bool(cs_subjects & subj_words) or any(kw in subj_lower for kw in ["computer science", "data structure", "c++"])
    
    # 1. Computer Science templates
    if is_cs:
        # Check standard experiments
        if "binary search" in exp_lower:
            aim = "To implement a Binary Search algorithm in Python to find an element in a sorted list."
            algo = (
                "1. Read the list of elements and the target value to search.\n"
                "2. Sort the list if it is not already sorted.\n"
                "3. Set low pointer to 0 and high pointer to len(list) - 1.\n"
                "4. Loop while low <= high:\n"
                "   a. Calculate mid = (low + high) // 2.\n"
                "   b. If list[mid] equals target, return mid.\n"
                "   c. If list[mid] < target, set low = mid + 1.\n"
                "   d. If list[mid] > target, set high = mid - 1.\n"
                "5. If loop ends and target is not found, return -1."
            )
            code = (
                "def binary_search(arr, x):\n"
                "    low = 0\n"
                "    high = len(arr) - 1\n"
                "    while low <= high:\n"
                "        mid = (low + high) // 2\n"
                "        if arr[mid] < x:\n"
                "            low = mid + 1\n"
                "        elif arr[mid] > x:\n"
                "            high = mid - 1\n"
                "        else:\n"
                "            return mid\n"
                "    return -1\n\n"
                "# Test array\n"
                "arr = [2, 3, 4, 10, 40]\n"
                "x = 10\n"
                "result = binary_search(arr, x)\n"
                "if result != -1:\n"
                "    print(f'Element is present at index {result}')\n"
                "else:\n"
                "    print('Element is not present in array')"
            )
            output = "Element is present at index 3"
            result = "The Binary Search program was successfully written, compiled, and executed."
        elif "bubble sort" in exp_lower:
            aim = "To implement the Bubble Sort algorithm to sort an array of integers in ascending order."
            algo = (
                "1. Start with the first element (index 0) and compare it with the next element.\n"
                "2. If the current element is greater than the next element, swap them.\n"
                "3. Repeat this comparison and swapping for all adjacent elements in the array.\n"
                "4. This process pushes the largest unsorted element to its correct position at the end of the array.\n"
                "5. Repeat the entire pass n-1 times (where n is the number of elements) to sort the complete array."
            )
            code = (
                "def bubble_sort(arr):\n"
                "    n = len(arr)\n"
                "    for i in range(n):\n"
                "        # Last i elements are already in place\n"
                "        for j in range(0, n-i-1):\n"
                "            if arr[j] > arr[j+1]:\n"
                "                arr[j], arr[j+1] = arr[j+1], arr[j]\n\n"
                "arr = [64, 34, 25, 12, 22, 11, 90]\n"
                "bubble_sort(arr)\n"
                "print('Sorted array:', arr)"
            )
            output = "Sorted array: [11, 12, 22, 25, 34, 64, 90]"
            result = "The Bubble Sort program was successfully implemented and the array was sorted in ascending order."
        elif "linear search" in exp_lower:
            aim = "To implement Linear Search algorithm in Python to search for a target element in an array."
            algo = (
                "1. Traverse the array sequentially starting from index 0.\n"
                "2. In each iteration, compare the current element with the target element.\n"
                "3. If a match is found, return the current index.\n"
                "4. If the array is fully traversed and target is not found, return -1."
            )
            code = (
                "def linear_search(arr, x):\n"
                "    for i in range(len(arr)):\n"
                "        if arr[i] == x:\n"
                "            return i\n"
                "    return -1\n\n"
                "arr = [10, 20, 80, 30, 60, 50, 110, 100, 130, 170]\n"
                "x = 110\n"
                "res = linear_search(arr, x)\n"
                "print(f'Element found at index: {res}' if res != -1 else 'Element not found')"
            )
            output = "Element found at index: 6"
            result = "The Linear Search program was successfully verified and executed."
        else:
            aim = f"To write a program to implement the {experiment} experiment."
            algo = (
                f"1. Start the program execution.\n"
                f"2. Initialize variables and inputs required for {experiment}.\n"
                f"3. Perform core logic processing according to {experiment} specifications.\n"
                f"4. Format and print the computed results.\n"
                f"5. End the program execution."
            )
            code = (
                f"# Python program for {experiment}\n"
                f"def solve_problem(*args):\n"
                f"    print('Executing logic for {experiment}...')\n"
                f"    result = True\n"
                f"    return result\n\n"
                f"if __name__ == '__main__':\n"
                f"    solve_problem()"
            )
            output = f"Executing logic for {experiment}...\nSuccess"
            result = f"The program for {experiment} was successfully implemented and verified."
            
        return {
            "Aim": aim,
            "Algorithm": algo,
            "Code": code,
            "Output": output,
            "Result": result
        }
        
    # 2. Science templates
    else:
        if "ohm" in exp_lower:
            aim = "To study the relationship between potential difference and current across a conductor and determine its resistance."
            theory = (
                "Ohm's Law states that at a constant physical state (temperature, pressure, etc.), "
                "the electric current (I) flowing through a metallic conductor is directly proportional "
                "to the potential difference (V) across its ends. Mathematically: V = IR, where R is a "
                "constant called the electrical resistance of the conductor."
            )
            procedure = (
                "1. Assemble the circuit elements including voltmeter, ammeter, rheostat, key, battery, and the resistance wire.\n"
                "2. Connect the voltmeter in parallel and the ammeter in series with the resistance wire.\n"
                "3. Close the plug-in key and adjust the sliding contact of the rheostat to get the minimum current.\n"
                "4. Note the readings of the ammeter and voltmeter.\n"
                "5. Shift the rheostat sliding contact slightly to increase current, and record new ammeter and voltmeter values.\n"
                "6. Take at least 5 different readings and plot a graph of V vs I."
            )
            observation = (
                "A linear graph passing through the origin is obtained by plotting Voltage (V) on the Y-axis and "
                "Current (I) on the X-axis. The slope of this line represents the Resistance (R = V/I) of the wire."
            )
            result = "The potential difference (V) is found to vary linearly with current (I), verifying Ohm's Law. The resistance of the wire is determined from the slope."
        elif "titration" in exp_lower or "acid" in exp_lower or "base" in exp_lower:
            aim = "To determine the strength of a given hydrochloric acid solution by titrating it against a standard sodium hydroxide solution."
            theory = (
                "The reaction between an acid and a base is a neutralization reaction. Hydrochloric acid (HCl) reacts "
                "with Sodium Hydroxide (NaOH) to produce Sodium Chloride (NaCl) and water:\n"
                "HCl + NaOH -> NaCl + H2O\n"
                "At the equivalence point, the moles of acid equal the moles of base. Phenolphthalein is used as an indicator, "
                "which changes color from colorless in acidic medium to pale pink at the neutral/basic endpoint."
            )
            procedure = (
                "1. Clean the burette and fill it with the standard NaOH solution. Remove any air bubbles.\n"
                "2. Pipette out 10 mL of the given HCl solution into a clean conical flask.\n"
                "3. Add 1-2 drops of phenolphthalein indicator to the conical flask. The solution remains colorless.\n"
                "4. Titrate the acid against NaOH solution by adding NaOH dropwise with constant swirling.\n"
                "5. Stop titration as soon as a persistent faint pink color appears.\n"
                "6. Note the burette reading and repeat to obtain concordant values."
            )
            observation = (
                "Concordant Volume of NaOH used = 9.8 mL\n"
                "Calculated Normality of HCl = (Normality of NaOH * Vol of NaOH) / Vol of HCl\n"
                "Using N1V1 = N2V2, strength of HCl is determined."
            )
            result = "The strength of the given HCl solution was successfully determined to be 0.1 N through titration."
        elif "pendulum" in exp_lower:
            aim = "To determine the acceleration due to gravity (g) using a simple pendulum by plotting L-T^2 graph."
            theory = (
                "A simple pendulum consists of a heavy point mass (bob) suspended from a rigid support by a light, inextensible string. "
                "For small angular displacements, the time period of oscillation is given by T = 2 * pi * sqrt(L/g), where L is the length "
                "of the pendulum and g is the acceleration due to gravity. Thus, g = 4 * pi^2 * (L / T^2)."
            )
            procedure = (
                "1. Measure the diameter of the pendulum bob using Vernier calipers to find its radius.\n"
                "2. Tie a thread to the bob hook and clamp it between two split cork pieces in a stand.\n"
                "3. Set the length of the pendulum (suspension point to center of bob) to 80 cm.\n"
                "4. Displace the bob slightly to one side and release it gently to initiate oscillations.\n"
                "5. Using a stopwatch, record the time taken for 20 complete oscillations.\n"
                "6. Repeat for pendulum lengths of 90 cm, 100 cm, 110 cm, and 120 cm, computing T and T^2 for each."
            )
            observation = (
                "Table of Pendulum Length (L) vs Time Period (T) and T^2.\n"
                "The ratio L / T^2 is found to be constant.\n"
                "Graph of L vs T^2 is a straight line passing through the origin."
            )
            result = "The acceleration due to gravity (g) was successfully calculated to be approximately 9.8 m/s^2 using the simple pendulum."
        else:
            aim = f"To study the principles and perform the experiment of {experiment}."
            theory = (
                f"The experiment {experiment} is based on the fundamental principles of {subject}. "
                f"It explores the key variables and their behaviors under controlled experimental conditions."
            )
            procedure = (
                f"1. Gather all necessary apparatus and equipment for the {experiment} experiment.\n"
                f"2. Set up the experimental apparatus securely according to safe laboratory protocols.\n"
                f"3. Perform system calibration and record initial baseline measurements.\n"
                f"4. Introduce variables systematically and record observations at each interval.\n"
                f"5. Turn off all equipment and clean the experimental workspace."
            )
            observation = (
                f"During the {experiment} experiment, data was systematically gathered and recorded in tabular format. "
                f"The observations demonstrate direct correlation and follow established theoretical models."
            )
            result = f"The experiment {experiment} in {subject} was successfully conducted, and observations were verified."
            
        return {
            "Aim": aim,
            "Theory": theory,
            "Procedure": procedure,
            "Observation": observation,
            "Result": result
        }

@app.route('/')
def home():
    return "Flask API server is running. Use /generate with POST requests."

@app.route('/generate', methods=['POST'])
def generate_record():
    data = request.json or {}
    subject = data.get("Subject")
    experiment = data.get("Experiment")
    user = data.get("Username", "Student")

    # If Hugging Face is set up with a real token, try it
    use_huggingface = False
    if "YOUR_TOKEN" not in HEADERS.get("Authorization", "") and HEADERS.get("Authorization", "") != "Bearer ":
        use_huggingface = True

    result_data = None
    
    if use_huggingface:
        prompt = f"Generate a {subject} lab record for {experiment}. Include Aim, Algorithm/Theory, Procedure/Code, Output, Result."
        payload = {"inputs": prompt}
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=8)
            if response.status_code == 200:
                result = response.json()
                print("[DEBUG] Hugging Face raw response:", result)
                generated_text = ""
                if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                    generated_text = result[0]["generated_text"]
                elif isinstance(result, dict) and "generated_text" in result:
                    generated_text = result["generated_text"]
                
                if generated_text:
                    subj_lower = subject.lower() if subject else ""
                    is_cs = any(kw in subj_lower for kw in ["computer science", "cs", "programming", "cse", "python", "java", "c++", "data structure"])
                    if is_cs:
                        result_data = {
                            "Aim": f"To study {experiment}",
                            "Algorithm": f"Algorithm steps for {experiment}: {generated_text}",
                            "Code": f"Sample code or procedure for {experiment}: {generated_text}",
                            "Output": f"Expected output for {experiment}: {generated_text}",
                            "Result": f"Successfully executed {experiment} in {subject} lab."
                        }
                    else:
                        result_data = {
                            "Aim": f"To study {experiment}",
                            "Theory": f"Theory explanation for {experiment}: {generated_text}",
                            "Procedure": f"Step-by-step procedure for {experiment}: {generated_text}",
                            "Observation": f"Observations for {experiment}: {generated_text}",
                            "Result": f"Successfully performed {experiment} in {subject} lab."
                        }
        except Exception as e:
            print(f"[WARN] Hugging Face API error: {e}. Falling back to templates.")
            
    # Fallback to local template generator if HF is not configured, or if the API call failed/timed out
    if not result_data:
        print("[INFO] Using high-quality local template generation...")
        result_data = generate_fallback_record(subject, experiment)
        
    return jsonify(result_data)

if __name__ == '__main__':
    app.run(debug=True)
