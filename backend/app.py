from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

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
        elif "stack" in exp_lower:
            aim = "To implement Stack data structure operations (Push, Pop, Peek, Display) using an array or list."
            algo = (
                "1. Initialize an empty stack and define the maximum capacity.\n"
                "2. Push Operation: Check if stack is full (Overflow). If not, append element to the top of stack.\n"
                "3. Pop Operation: Check if stack is empty (Underflow). If not, remove and return the topmost element.\n"
                "4. Peek Operation: Return the topmost element without removing it.\n"
                "5. Display Operation: Traverse and print all elements from top to bottom."
            )
            code = (
                "class Stack:\n"
                "    def __init__(self):\n"
                "        self.items = []\n\n"
                "    def push(self, item):\n"
                "        self.items.append(item)\n"
                "        print(f'Pushed: {item}')\n\n"
                "    def pop(self):\n"
                "        if not self.is_empty():\n"
                "            return self.items.pop()\n"
                "        return 'Stack Underflow'\n\n"
                "    def peek(self):\n"
                "        return self.items[-1] if not self.is_empty() else 'Empty'\n\n"
                "    def is_empty(self):\n"
                "        return len(self.items) == 0\n\n"
                "s = Stack()\n"
                "s.push(10)\n"
                "s.push(20)\n"
                "s.push(30)\n"
                "print('Popped element:', s.pop())\n"
                "print('Top element:', s.peek())"
            )
            output = "Pushed: 10\nPushed: 20\nPushed: 30\nPopped element: 30\nTop element: 20"
            result = "Stack operations were successfully implemented and verified."
        elif "queue" in exp_lower:
            aim = "To implement Queue data structure operations (Enqueue, Dequeue, Display) following FIFO principle."
            algo = (
                "1. Initialize front and rear pointers to track queue elements.\n"
                "2. Enqueue: Check for overflow. Add element at the rear and increment rear.\n"
                "3. Dequeue: Check for underflow. Remove element from the front and increment front.\n"
                "4. Display: Traverse the queue from front to rear and print elements."
            )
            code = (
                "class Queue:\n"
                "    def __init__(self):\n"
                "        self.queue = []\n\n"
                "    def enqueue(self, item):\n"
                "        self.queue.append(item)\n"
                "        print(f'Enqueued: {item}')\n\n"
                "    def dequeue(self):\n"
                "        if len(self.queue) > 0:\n"
                "            return self.queue.pop(0)\n"
                "        return 'Queue Underflow'\n\n"
                "q = Queue()\n"
                "q.enqueue(5)\n"
                "q.enqueue(15)\n"
                "q.enqueue(25)\n"
                "print('Dequeued:', q.dequeue())\n"
                "print('Remaining Queue:', q.queue)"
            )
            output = "Enqueued: 5\nEnqueued: 15\nEnqueued: 25\nDequeued: 5\nRemaining Queue: [15, 25]"
            result = "Queue implementation with FIFO operations was successfully executed."
        elif "linked list" in exp_lower:
            aim = "To implement Singly Linked List operations including insertion, deletion, and traversal."
            algo = (
                "1. Define a Node class with data and next pointer.\n"
                "2. Insertion: Create a new node. Link its next pointer and update the head.\n"
                "3. Deletion: Search for the key, adjust the next pointer of the previous node to skip the target node.\n"
                "4. Traversal: Start from head and traverse until the pointer is NULL, printing data."
            )
            code = (
                "class Node:\n"
                "    def __init__(self, data):\n"
                "        self.data = data\n"
                "        self.next = None\n\n"
                "class LinkedList:\n"
                "    def __init__(self):\n"
                "        self.head = None\n\n"
                "    def insert(self, data):\n"
                "        new_node = Node(data)\n"
                "        new_node.next = self.head\n"
                "        self.head = new_node\n\n"
                "    def display(self):\n"
                "        curr = self.head\n"
                "        elements = []\n"
                "        while curr:\n"
                "            elements.append(str(curr.data))\n"
                "            curr = curr.next\n"
                "        print(' -> '.join(elements) + ' -> None')\n\n"
                "ll = LinkedList()\n"
                "ll.insert(30)\n"
                "ll.insert(20)\n"
                "ll.insert(10)\n"
                "ll.display()"
            )
            output = "10 -> 20 -> 30 -> None"
            result = "Singly Linked List insertion and traversal operations were successfully executed."
        elif "merge sort" in exp_lower:
            aim = "To implement Merge Sort using Divide and Conquer strategy to sort an array."
            algo = (
                "1. Find the midpoint of the array: mid = len(arr) // 2.\n"
                "2. Recursively divide the array into left and right subarrays.\n"
                "3. Merge the two sorted subarrays back into the original array.\n"
                "4. Continue merging recursively until the entire array is sorted."
            )
            code = (
                "def merge_sort(arr):\n"
                "    if len(arr) > 1:\n"
                "        mid = len(arr) // 2\n"
                "        L = arr[:mid]\n"
                "        R = arr[mid:]\n"
                "        merge_sort(L)\n"
                "        merge_sort(R)\n"
                "        i = j = k = 0\n"
                "        while i < len(L) and j < len(R):\n"
                "            if L[i] < R[j]:\n"
                "                arr[k] = L[i]; i += 1\n"
                "            else:\n"
                "                arr[k] = R[j]; j += 1\n"
                "            k += 1\n"
                "        while i < len(L):\n"
                "            arr[k] = L[i]; i += 1; k += 1\n"
                "        while j < len(R):\n"
                "            arr[k] = R[j]; j += 1; k += 1\n\n"
                "arr = [38, 27, 43, 3, 9, 82, 10]\n"
                "merge_sort(arr)\n"
                "print('Sorted array:', arr)"
            )
            output = "Sorted array: [3, 9, 10, 27, 38, 43, 82]"
            result = "The array was successfully sorted in O(n log n) time using Merge Sort."
        elif "quick sort" in exp_lower:
            aim = "To implement Quick Sort algorithm using partition logic to sort an array."
            algo = (
                "1. Choose an element as pivot.\n"
                "2. Partition: rearrange array so elements smaller than pivot go left, larger go right.\n"
                "3. Recursively apply Quick Sort to the left and right subarrays.\n"
                "4. Combine subproblems until the whole array is sorted."
            )
            code = (
                "def quick_sort(arr):\n"
                "    if len(arr) <= 1:\n"
                "        return arr\n"
                "    pivot = arr[len(arr) // 2]\n"
                "    left = [x for x in arr if x < pivot]\n"
                "    middle = [x for x in arr if x == pivot]\n"
                "    right = [x for x in arr if x > pivot]\n"
                "    return quick_sort(left) + middle + quick_sort(right)\n\n"
                "arr = [10, 80, 30, 90, 40, 50, 70]\n"
                "sorted_arr = quick_sort(arr)\n"
                "print('Sorted array:', sorted_arr)"
            )
            output = "Sorted array: [10, 30, 40, 50, 70, 80, 90]"
            result = "Quick Sort algorithm was implemented and executed successfully."
        elif "matrix" in exp_lower:
            aim = "To implement Matrix Multiplication of two matrices using nested loops in Python."
            algo = (
                "1. Input dimensions of matrix A (r1 x c1) and matrix B (r2 x c2).\n"
                "2. Verify if multiplication is possible (c1 must equal r2).\n"
                "3. Initialize a result matrix with dimensions (r1 x c2) filled with zeros.\n"
                "4. Iterate through rows of A, columns of B, and accumulate dot product: C[i][j] += A[i][k] * B[k][j].\n"
                "5. Display resultant matrix."
            )
            code = (
                "A = [[1, 2], [3, 4]]\n"
                "B = [[5, 6], [7, 8]]\n"
                "result = [[0, 0], [0, 0]]\n\n"
                "for i in range(len(A)):\n"
                "    for j in range(len(B[0])):\n"
                "        for k in range(len(B)):\n"
                "            result[i][j] += A[i][k] * B[k][j]\n\n"
                "print('Resultant Matrix:')\n"
                "for r in result:\n"
                "    print(r)"
            )
            output = "Resultant Matrix:\n[19, 22]\n[43, 50]"
            result = "Matrix multiplication was successfully computed and verified."
        elif "sql" in exp_lower or "ddl" in exp_lower or "dml" in exp_lower or "database" in exp_lower:
            aim = "To execute fundamental SQL Data Definition (DDL) and Data Manipulation (DML) commands."
            algo = (
                "1. Use CREATE TABLE command to define student table structure with constraints.\n"
                "2. Use INSERT INTO command to populate records into the table.\n"
                "3. Use SELECT command to retrieve and filter data using WHERE clause.\n"
                "4. Use UPDATE command to modify existing table data.\n"
                "5. Use DELETE command to remove specific records."
            )
            code = (
                "-- 1. DDL: Create Table\n"
                "CREATE TABLE Student (\n"
                "    RegNo INT PRIMARY KEY,\n"
                "    Name VARCHAR(50),\n"
                "    Department VARCHAR(20),\n"
                "    Marks INT\n"
                ");\n\n"
                "-- 2. DML: Insert Data\n"
                "INSERT INTO Student VALUES (101, 'Ranjith', 'CSE', 95);\n"
                "INSERT INTO Student VALUES (102, 'Praveen', 'ECE', 88);\n\n"
                "-- 3. DQL: Query Data\n"
                "SELECT * FROM Student WHERE Marks > 90;\n\n"
                "-- 4. DML: Update Data\n"
                "UPDATE Student SET Marks = 98 WHERE RegNo = 101;"
            )
            output = "RegNo | Name    | Department | Marks\n------------------------------------\n101   | Ranjith | CSE        | 95\n(1 row affected)\nRecord updated successfully."
            result = "SQL DDL and DML operations were executed and table states verified."
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
        elif "conductometric" in exp_lower:
            aim = "To determine the strength of a given strong acid (HCl) by titrating against standard NaOH conductometrically."
            theory = (
                "Conductance of an electrolyte depends on the number and mobility of ions present.\n"
                "As NaOH is added to HCl, fast-moving H+ ions (mobility 350) are replaced by slower Na+ ions (mobility 50):\n"
                "H+ + Cl- + Na+ + OH- -> Na+ + Cl- + H2O\n"
                "Therefore, conductance decreases linearly until the equivalence point. Past the endpoint, excess fast-moving OH- ions "
                "cause conductance to increase sharply. The intersection of the two straight-line slopes gives the exact equivalence volume."
            )
            procedure = (
                "1. Calibrate the digital conductivity meter with 0.1 M standard KCl solution.\n"
                "2. Pipette 20 mL of the given HCl solution into a 100 mL beaker and add 40 mL of distilled water to fully immerse the cell.\n"
                "3. Dip the conductivity cell into the solution and note the initial conductance.\n"
                "4. Add 0.5 mL of 0.1 N NaOH from the burette, stir thoroughly with a glass rod, and record conductance.\n"
                "5. Continue titration well past the minimum point (at least 6-8 readings after rise).\n"
                "6. Plot Conductance (mS) on Y-axis against Volume of NaOH (mL) on X-axis to find the neutralization point."
            )
            observation = (
                "Equivalence Point Volume from graph (V_NaOH) = 19.8 mL\n"
                "Normality of NaOH = 0.1 N, Volume of HCl = 20 mL\n"
                "Calculated Normality of HCl (N1 = N2*V2/V1) = (0.1 * 19.8) / 20 = 0.099 N\n"
                "Strength of HCl = Normality * Equivalent Weight (36.5) = 3.61 g/L"
            )
            result = "The strength of the given HCl solution was conductometrically determined to be 0.099 N (3.61 g/L)."
        elif "hardness" in exp_lower or "edta" in exp_lower:
            aim = "To estimate the total, permanent, and temporary hardness of a given water sample using standard EDTA solution."
            theory = (
                "Hardness is primarily due to soluble bivalent salts of Calcium and Magnesium (Ca2+, Mg2+).\n"
                "EDTA (Disodium dihydrogen ethylenediaminetetraacetate) forms stable, 1:1 soluble chelate complexes with Ca2+ and Mg2+ at pH 9-10.\n"
                "Eriochrome Black-T (EBT) is used as indicator. Metal ions bind EBT forming a wine-red complex:\n"
                "[M-EBT] (wine-red) + EDTA -> [M-EDTA] (colorless) + Free EBT (steel blue)\n"
                "At endpoint, all metal ions are sequestered by EDTA, restoring the pure steel-blue color of free EBT."
            )
            procedure = (
                "1. Pipette 20 mL of the given hard water sample into a clean 250 mL conical flask.\n"
                "2. Add 5 mL of NH4Cl-NH4OH buffer solution to maintain pH at 10.\n"
                "3. Add 2-3 drops of Eriochrome Black-T indicator; solution turns wine-red.\n"
                "4. Titrate against standardized 0.01 M EDTA solution from burette with continuous swirling.\n"
                "5. Stop at the sharp change from wine-red to steel-blue and record volume V1.\n"
                "6. Boil 100 mL of water sample for 15 minutes, filter, and repeat titration on filtrate to determine permanent hardness (V2)."
            )
            observation = (
                "Total Hardness titre value (V1) = 18.4 mL\n"
                "Permanent Hardness titre value (V2) = 11.2 mL\n"
                "Temporary Hardness = V1 - V2 = 7.2 mL\n"
                "Total Hardness = (V1 * Molarity of EDTA * 100 * 1000) / Volume of Sample = 184 ppm (mg/L CaCO3 equivalent)"
            )
            result = "Total hardness = 184 ppm, Permanent hardness = 112 ppm, and Temporary hardness = 72 ppm as CaCO3 equivalents."
        elif "viscosity" in exp_lower or "ostwald" in exp_lower:
            aim = "To determine the coefficient of absolute and relative viscosity of a given liquid using an Ostwald Viscometer."
            theory = (
                "According to Poiseuille's law, the rate of flow of a liquid through a capillary tube depends on viscosity (eta), density (d), and time of flow (t).\n"
                "Relative Viscosity (eta_L / eta_W) = (d_L * t_L) / (d_W * t_W)\n"
                "where d_L, d_W are densities and t_L, t_W are flow times for test liquid and water respectively."
            )
            procedure = (
                "1. Thoroughly clean the Ostwald Viscometer with chromic acid solution and rinse with distilled water and dry.\n"
                "2. Clamp the viscometer vertically in a water bath to maintain constant temperature.\n"
                "3. Pipette 15 mL of distilled water into the wider limb and suck liquid above the upper index mark A.\n"
                "4. Release water and start stopwatch when meniscus passes mark A; stop when it passes lower mark B. Record time t_W.\n"
                "5. Repeat twice for concordant values. Rinse, dry, and repeat entire procedure with the test liquid to determine t_L.\n"
                "6. Determine densities using a specific gravity bottle."
            )
            observation = (
                "Flow time for water (t_W) = 48.2 s\n"
                "Flow time for test liquid (t_L) = 82.6 s\n"
                "Density of water (d_W) = 0.998 g/cm^3\n"
                "Density of liquid (d_L) = 0.865 g/cm^3\n"
                "Viscosity of water at 25 C = 0.891 cP\n"
                "Calculated Viscosity of Liquid = 1.32 cP"
            )
            result = "The relative viscosity of the test liquid with respect to water was 1.48, and absolute viscosity was 1.32 centipoise (cP)."
        elif "surface tension" in exp_lower or "stalagmometer" in exp_lower:
            aim = "To determine the surface tension of a given liquid using a Stalagmometer by the drop number method."
            theory = (
                "The weight of a falling liquid drop is proportional to its surface tension (gamma) and radius of capillary orifice:\n"
                "m * g = 2 * pi * r * gamma\n"
                "Comparing equal volumes of test liquid and water: gamma_L / gamma_W = (n_W * d_L) / (n_L * d_W)\n"
                "where n_W, n_L are drop counts, and d_W, d_L are densities."
            )
            procedure = (
                "1. Clean the stalagmometer with chromic acid, rinse with water and dry.\n"
                "2. Attach a clean rubber bulb and immerse capillary tip in distilled water.\n"
                "3. Suck water above upper mark A, clamp vertically, and regulate flow rate to 15-20 drops per minute.\n"
                "4. Count number of drops falling freely while liquid level drops from mark A to mark B (n_W).\n"
                "5. Rinse and dry stalagmometer, then repeat three times with test liquid to determine drop count (n_L).\n"
                "6. Measure liquid densities using a pycnometer / relative density bottle."
            )
            observation = (
                "Mean drop count for water (n_W) = 44 drops\n"
                "Mean drop count for test liquid (n_L) = 86 drops\n"
                "Density of water (d_W) = 0.997 g/mL, Density of liquid (d_L) = 0.789 g/mL\n"
                "Surface tension of water (gamma_W) = 72.8 dynes/cm\n"
                "Calculated Surface Tension of Liquid = 31.9 dynes/cm"
            )
            result = "The surface tension of the given test liquid at room temperature was determined to be 31.9 dynes/cm (mN/m)."
        elif "aspirin" in exp_lower or "soap" in exp_lower or "saponification" in exp_lower:
            aim = "To synthesize Aspirin (Acetylsalicylic acid) by acetylation of Salicylic acid."
            theory = (
                "Aspirin is synthesized via esterification/acetylation of the phenolic hydroxyl group of salicylic acid "
                "with acetic anhydride in the presence of concentrated sulfuric acid or phosphoric acid as catalyst:\n"
                "C7H6O3 (Salicylic Acid) + C4H6O3 (Acetic Anhydride) -> C9H8O4 (Aspirin) + CH3COOH (Acetic Acid)\n"
                "Pure aspirin precipitates as white needle-shaped crystals."
            )
            procedure = (
                "1. Weigh 2.0 g of dry salicylic acid and transfer into a clean, dry 100 mL conical flask.\n"
                "2. Add 5.0 mL of acetic anhydride followed by 4-5 drops of concentrated H2SO4.\n"
                "3. Warm the flask on a water bath at 50-60 C for 15 minutes with gentle swirling.\n"
                "4. Allow the reaction mixture to cool to room temperature, then add 20 mL of ice-cold water to decompose excess anhydride.\n"
                "5. Cool in an ice bath until crystallization is complete. Filter the crystals through a Buchner funnel under suction.\n"
                "6. Recrystallize the crude aspirin using an ethanol-water mixture and dry in a desiccator."
            )
            observation = (
                "Mass of Salicylic acid = 2.0 g\n"
                "Theoretical yield of Aspirin = 2.61 g\n"
                "Actual dry yield obtained = 2.18 g\n"
                "Percentage Yield = (2.18 / 2.61) * 100 = 83.5%\n"
                "Melting point of synthesized Aspirin = 135-136 C (Literature: 135 C)"
            )
            result = "Aspirin was successfully synthesized with a percentage yield of 83.5% and characterized by its melting point."
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
        elif "pendulum" in exp_lower and "torsional" not in exp_lower:
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
        elif "vernier" in exp_lower or "caliper" in exp_lower:
            aim = "To determine the volume of a cylinder and a sphere using Vernier Calipers."
            theory = (
                "Vernier Calipers are used to measure dimensions up to 0.1 mm precision.\n"
                "Least Count (LC) = 1 Main Scale Division (MSD) - 1 Vernier Scale Division (VSD) = 0.1 mm = 0.01 cm.\n"
                "Total Reading = MSR + (VSR * LC) +/- Zero Correction.\n"
                "Volume of Cylinder = pi * (D/2)^2 * h\n"
                "Volume of Sphere = (4/3) * pi * (D/2)^3"
            )
            procedure = (
                "1. Determine the least count and zero error of the Vernier Calipers.\n"
                "2. Place the cylinder longitudinally between lower jaws to measure height (h).\n"
                "3. Note down the Main Scale Reading (MSR) and Vernier Coincidence (VSR).\n"
                "4. Grip the cylinder and sphere across diameters to determine mean diameter (D).\n"
                "5. Calculate total reading and compute the volume using standard formulas."
            )
            observation = (
                "Least Count = 0.01 cm\n"
                "Zero Error = Nil\n"
                "Mean Diameter of Sphere = 2.42 cm\n"
                "Mean Height of Cylinder = 4.86 cm\n"
                "Calculated Volume of Cylinder = 22.38 cm^3\n"
                "Calculated Volume of Sphere = 7.42 cm^3"
            )
            result = "The dimensions and volume of the given cylinder and sphere were determined accurately using Vernier Calipers."
        elif "screw gauge" in exp_lower or "micrometer" in exp_lower:
            aim = "To determine the thickness of a glass plate and the diameter of a thin wire using a Screw Gauge."
            theory = (
                "A screw gauge works on the principle of a screw rotating in a fixed nut.\n"
                "Pitch of screw = (Distance moved by screw) / (No. of complete rotations) = 1 mm.\n"
                "Least Count (LC) = Pitch / (Total Head Scale Divisions) = 1 mm / 100 = 0.01 mm.\n"
                "Total Reading = PSR + (HSR * LC) +/- Zero Correction."
            )
            procedure = (
                "1. Determine the pitch, least count, and zero error of the screw gauge.\n"
                "2. Place the thin wire between the anvil and spindle and turn the ratchet until it clicks.\n"
                "3. Record the Pitch Scale Reading (PSR) and Head Scale Coincidence (HSR).\n"
                "4. Repeat measurements along different parts of the wire at right angles.\n"
                "5. Repeat the procedure to measure the thickness of the glass plate."
            )
            observation = (
                "Pitch = 1 mm\n"
                "Least Count = 0.01 mm\n"
                "Mean Diameter of Wire = 0.48 mm\n"
                "Mean Thickness of Glass Plate = 2.34 mm"
            )
            result = "The diameter of the wire (0.48 mm) and thickness of the glass plate (2.34 mm) were measured using the Screw Gauge."
        elif "meter bridge" in exp_lower or "metre bridge" in exp_lower:
            aim = "To determine the resistance and specific resistance (resistivity) of a given wire using a Meter Bridge."
            theory = (
                "The meter bridge operates on Wheatstone's bridge principle: P / Q = R / S.\n"
                "For a uniform wire of length 100 cm, unknown resistance X = R * (100 - l) / l, "
                "where l is balancing length and R is resistance from resistance box.\n"
                "Specific Resistance (rho) = (X * pi * r^2) / L, where r is radius and L is length of wire."
            )
            procedure = (
                "1. Assemble the circuit connecting battery, resistance box, unknown wire, and galvanometer.\n"
                "2. Introduce a suitable resistance R (e.g., 2 ohms) in the resistance box.\n"
                "3. Slide the jockey gently on the wire to locate the null deflection point (G = 0).\n"
                "4. Record the balancing length l and calculate (100 - l).\n"
                "5. Repeat for at least 4 different resistance values and calculate mean X and resistivity."
            )
            observation = (
                "Balancing lengths recorded for R = 2, 3, 4, 5 Ohms.\n"
                "Mean Unknown Resistance (X) = 3.42 Ohms\n"
                "Radius of wire (r) = 0.24 mm\n"
                "Length of wire (L) = 50 cm\n"
                "Calculated Specific Resistance (rho) = 1.24 x 10^-6 Ohm-m"
            )
            result = "The resistance of the given wire was found to be 3.42 Ohms and its specific resistance is 1.24 x 10^-6 Ohm-m."
        elif "spectrometer" in exp_lower or "prism" in exp_lower:
            aim = "To determine the angle of the prism (A) and angle of minimum deviation (D), and find the refractive index of the prism."
            theory = (
                "Refractive index (mu) of the material of a prism is given by:\n"
                "mu = sin((A + D) / 2) / sin(A / 2)\n"
                "where A is the angle of the prism and D is the angle of minimum deviation."
            )
            procedure = (
                "1. Perform initial adjustments of the spectrometer (leveling, focusing telescope and collimator for parallel rays).\n"
                "2. Place the prism with its refracting edge facing the collimator.\n"
                "3. Rotate the telescope to observe reflected light from both refracting surfaces and calculate prism angle A.\n"
                "4. Turn the prism to receive refracted rays and observe the spectrum.\n"
                "5. Rotate prism table until spectrum turns back; this turning position gives minimum deviation D."
            )
            observation = (
                "Vernier 1 and Vernier 2 readings recorded.\n"
                "Angle of the Prism (A) = 60 degrees\n"
                "Angle of Minimum Deviation (D) = 38 degrees 45 minutes\n"
                "Refractive Index (mu) = sin(49 deg 22 min) / sin(30 deg) = 1.518"
            )
            result = "The refractive index of the material of the prism was determined to be 1.52."
        elif "young" in exp_lower or "bending" in exp_lower:
            aim = "To determine the Young's Modulus of elasticity of the material of a wooden/metallic beam by uniform bending."
            theory = (
                "When a beam supported on two knife edges is loaded at center/symmetrically, bending occurs.\n"
                "Young's Modulus Y = (3 * g * l * m * p) / (2 * b * d^3 * y)\n"
                "where m is load, l is length between supports, b is breadth, d is thickness, and y is elevation/depression."
            )
            procedure = (
                "1. Place the beam symmetrically on two knife edges separated by distance l.\n"
                "2. Suspend equal weight hangers at equal distances from the supports.\n"
                "3. Focus the traveling microscope on a pin attached to the center of the beam.\n"
                "4. Record microscope readings for increasing and decreasing loads in steps of 50g.\n"
                "5. Measure breadth (b) with Vernier calipers and thickness (d) with screw gauge."
            )
            observation = (
                "Distance between knife edges (l) = 60 cm\n"
                "Breadth (b) = 2.45 cm, Thickness (d) = 0.42 cm\n"
                "Mean elevation per 50g load (y) = 0.082 cm\n"
                "Calculated Young's Modulus (Y) = 1.05 x 10^11 N/m^2"
            )
            result = "The Young's Modulus of elasticity of the given material was calculated to be 1.05 x 10^11 N/m^2."
        elif "torsional" in exp_lower:
            aim = "To determine the rigidity modulus of a wire and moment of inertia of a disc using a Torsional Pendulum."
            theory = (
                "A torsional pendulum performs simple harmonic torsional oscillations.\n"
                "Rigidity Modulus (n) = (8 * pi * I * L) / (T^2 * r^4)\n"
                "where I is moment of inertia, L is length of suspension wire, T is time period, and r is wire radius."
            )
            procedure = (
                "1. Suspend the circular metallic disc horizontally by the test wire clamped at both ends.\n"
                "2. Rotate disc slightly in horizontal plane and release to set into torsional oscillations.\n"
                "3. Record time for 20 oscillations using a stopwatch to compute period T0.\n"
                "4. Place two identical cylindrical masses at distances d1 and d2 symmetrically, measuring periods T1 and T2.\n"
                "5. Measure radius of wire with screw gauge and length with meter scale."
            )
            observation = (
                "Length of wire (L) = 65 cm, Radius of wire (r) = 0.45 mm\n"
                "Time period without masses (T0) = 2.12 s\n"
                "Time period with masses (T1) = 3.48 s\n"
                "Calculated Rigidity Modulus (n) = 2.82 x 10^10 N/m^2"
            )
            result = "The Rigidity Modulus of the wire was determined to be 2.82 x 10^10 N/m^2 using the Torsional Pendulum."
        elif "mitosis" in exp_lower or "onion" in exp_lower:
            aim = "To prepare a temporary squash mount of onion root tip cells and study the stages of mitosis under a microscope."
            theory = (
                "Mitosis is equational cell division occurring in somatic cells, preserving chromosome number.\n"
                "Active vegetative meristematic tissues in onion (Allium cepa) root tips show distinct mitotic phases:\n"
                "1. Prophase: Chromatin condenses into distinct chromosomes; nuclear envelope disappears.\n"
                "2. Metaphase: Chromosomes align along the equatorial metaphase plate attached to spindle fibers.\n"
                "3. Anaphase: Centromeres split; sister chromatids separate and migrate to opposite poles.\n"
                "4. Telophase: Chromosomes uncoil; nuclear envelopes reassemble around daughter nuclei followed by cytokinesis."
            )
            procedure = (
                "1. Grow fresh onion root tips over water for 3-4 days in a dark environment.\n"
                "2. Cut 2-3 mm of root tips and fix in Carnoy's fluid (Glacial acetic acid : Ethanol = 1:3) for 24 hours.\n"
                "3. Transfer root tips to 1 N HCl and warm at 60 C for 6-8 minutes for acid hydrolysis to dissolve pectin.\n"
                "4. Wash thoroughly with distilled water and place on a clean glass slide.\n"
                "5. Stain with 2% Acetocarmine for 10 minutes, add a drop of 45% acetic acid, cover with coverslip.\n"
                "6. Squash gently under blotting paper with thumb pressure and observe under 10x and 45x objectives."
            )
            observation = (
                "Microscopic field displays meristematic cells displaying distinct stages:\n"
                "- Interphase: Intact nucleus with prominent nucleolus and diffuse chromatin network.\n"
                "- Prophase: Thick, dark, coiled rod-like chromosomes visible.\n"
                "- Metaphase: Chromosomes aligned sharply along the center line (equatorial plane).\n"
                "- Anaphase: V- and L-shaped chromatids moving towards polar centrioles.\n"
                "- Telophase: Two distinct daughter nuclei formed with cell plate formation in center."
            )
            result = "The stages of mitosis (Prophase, Metaphase, Anaphase, Telophase) were successfully prepared, identified, and recorded."
        elif "gram" in exp_lower or "stain" in exp_lower:
            aim = "To identify and differentiate bacteria into Gram-positive and Gram-negative types using the Gram Staining technique."
            theory = (
                "Gram staining differentiates bacteria based on chemical and physical properties of their cell walls:\n"
                "- Gram-positive bacteria have a thick peptidoglycan layer containing teichoic acids that traps Crystal Violet-Iodine complex, resisting alcohol decolorization and appearing purple/violet.\n"
                "- Gram-negative bacteria have a thinner peptidoglycan layer enclosed by an outer lipopolysaccharide membrane. Alcohol dissolves the outer lipids, eluting the CV-I complex; counterstain Safranin stains them pink/red."
            )
            procedure = (
                "1. Prepare a thin bacterial smear from culture on a clean glass slide, air dry, and heat-fix by passing through flame 3 times.\n"
                "2. Flood smear with primary stain Crystal Violet for 1 minute, then gently wash with tap water.\n"
                "3. Flood with mordant Gram's Iodine for 1 minute; wash gently with water.\n"
                "4. Decolorize with 95% ethyl alcohol for 10-15 seconds until runoff is colorless; immediately wash with water to stop reaction.\n"
                "5. Counterstain with Safranin for 45 seconds, rinse with water, and blot dry with bibulous paper.\n"
                "6. Add a drop of immersion oil and observe under 100x oil immersion objective."
            )
            observation = (
                "Sample A: Cocci clustered in bunches retaining intense purple/violet color (Gram-positive, e.g., Staphylococcus aureus).\n"
                "Sample B: Short rod-shaped bacilli stained distinct pink/red color (Gram-negative, e.g., Escherichia coli)."
            )
            result = "The bacterial samples were successfully differentiated into Gram-positive (purple) and Gram-negative (pink) organisms."
        elif "dna" in exp_lower or "isolation" in exp_lower or "extraction" in exp_lower:
            aim = "To isolate and extract crude genomic DNA from plant material (Banana / Onion)."
            theory = (
                "Plant cell DNA is protected within cell walls, plasma membranes, and nuclear envelopes.\n"
                "- Mechanical grinding breaks rigid cellulose cell walls.\n"
                "- Detergent (SDS / liquid detergent) dissolves lipid bilayer cell and nuclear membranes by emulsification.\n"
                "- Sodium Chloride (NaCl) provides Na+ ions that shield negative charges of phosphate groups, allowing DNA strands to clump together.\n"
                "- Chilled Ethanol precipitates nucleic acids because DNA is polar and insoluble in cold alcohol, separating it from soluble proteins."
            )
            procedure = (
                "1. Mash 50 g of peeled banana or chopped onion thoroughly with a mortar and pestle.\n"
                "2. Prepare extraction buffer: 50 mL distilled water, 1 teaspoon table salt, and 2 tablespoons liquid detergent.\n"
                "3. Mix the plant paste with extraction buffer and incubate in a 60 C water bath for 15 minutes to denature DNases.\n"
                "4. Chill the mixture in an ice-water bath for 5 minutes and filter through a muslin cloth / filter funnel into a clean beaker.\n"
                "5. Tilt the beaker and slowly layer ice-cold 95% ethanol down the side wall without mixing.\n"
                "6. Observe white translucent cottony precipitate forming at the alcohol-water interface. Spool out with a glass rod."
            )
            observation = (
                "A dense, white fibrous precipitate of stringy DNA strands formed immediately at the alcohol-filtrate boundary layer.\n"
                "The DNA was easily spooled around a clean glass rod as viscous strands."
            )
            result = "Crude genomic DNA was successfully extracted and visualized from plant tissue using the alcohol precipitation method."
        elif "carbohydrate" in exp_lower or "protein" in exp_lower or "biochemical" in exp_lower or "food" in exp_lower:
            aim = "To detect the presence of carbohydrates, proteins, and fats in given food/biological samples through biochemical tests."
            theory = (
                "Biochemical tests rely on specific color reactions with functional groups:\n"
                "- Benedict's Test: Reducing sugars reduce blue Cu2+ to brick-red Cu2O precipitate upon heating.\n"
                "- Iodine Test: Amylose in starch traps iodine molecules in its helical structure, yielding a deep blue-black color.\n"
                "- Biuret Test: Peptide bonds react with cupric ions in alkaline medium forming a violet coordination complex.\n"
                "- Sudan III / Emulsion Test: Lipids dissolve non-polar dyes (Sudan III) producing red droplets or form milky white emulsions."
            )
            procedure = (
                "1. Test for Reducing Sugar: Add 2 mL Benedict's reagent to 2 mL sample; heat in boiling water bath for 5 minutes.\n"
                "2. Test for Starch: Add 2-3 drops of Lugol's iodine solution to 2 mL sample solution.\n"
                "3. Test for Protein: Add 1 mL 10% NaOH and 4 drops 1% CuSO4 solution to 2 mL sample solution; shake well.\n"
                "4. Test for Lipids: Shake 1 mL sample with 2 mL ethanol, decant liquid into a test tube containing 2 mL water."
            )
            observation = (
                "1. Benedict's Test: Brick-red precipitate formed -> Reducing sugars present.\n"
                "2. Iodine Test: Immediate blue-black coloration -> Starch present.\n"
                "3. Biuret Test: Distinct purple/violet color observed -> Proteins present.\n"
                "4. Emulsion Test: Turbid milky-white emulsion formed -> Lipids/Fats present."
            )
            result = "Qualitative biochemical analysis confirmed the presence of reducing sugars, starch, proteins, and lipids in the test sample."
        elif "photosynthesis" in exp_lower or "hydrilla" in exp_lower:
            aim = "To demonstrate the evolution of oxygen during photosynthesis using Hydrilla and examine factors affecting its rate."
            theory = (
                "Photosynthesis is the photochemical synthesis of carbohydrates from CO2 and H2O:\n"
                "6 CO2 + 6 H2O + Light -> C6H12O6 + 6 O2 (gas)\n"
                "Aquatic plants like Hydrilla release produced O2 as visible gas bubbles through intercellular spaces in cut stems.\n"
                "The rate of bubble release is a direct metric of photosynthetic activity, influenced by light intensity and CO2 availability."
            )
            procedure = (
                "1. Place several freshly cut healthy sprigs of Hydrilla verticillata into the bulb of a short-stem glass funnel.\n"
                "2. Invert the funnel in a large glass beaker filled with water containing 0.5 g sodium bicarbonate (NaHCO3) as CO2 source.\n"
                "3. Invert a water-filled test tube over the stem of the funnel, ensuring no initial air bubble is trapped.\n"
                "4. Place the apparatus under direct sunlight or at a distance of 20 cm from a 100 W incandescent lamp.\n"
                "5. Count bubbles released per minute from the cut stems. Vary lamp distance (30 cm, 40 cm, 50 cm) and recount.\n"
                "6. Test the collected gas in the test tube with a glowing wood splinter."
            )
            observation = (
                "Distance from light source vs Bubbles per minute:\n"
                "- 20 cm: 42 bubbles/min\n"
                "- 30 cm: 26 bubbles/min\n"
                "- 40 cm: 15 bubbles/min\n"
                "- 50 cm: 8 bubbles/min\n"
                "When the glowing splinter is inserted into the gas cavity, it reignites into a flame, confirming oxygen."
            )
            result = "Evolution of oxygen during photosynthesis was verified, and the photosynthetic rate was confirmed to be directly proportional to light intensity."
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

@app.route('/generate', methods=['POST'])
def generate_record():
    data = request.json or {}
    subject = data.get("Subject")
    experiment = data.get("Experiment")
    user = data.get("Username", "Student")

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
            
    if not result_data:
        print("[INFO] Using high-quality local template generation...")
        result_data = generate_fallback_record(subject, experiment)
        
    return jsonify(result_data)

if __name__ == '__main__':
    app.run(debug=True)
