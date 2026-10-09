# 🧪 AI Lab Record Generator

<div align="center">

### Create complete, ready-to-submit college lab records in seconds with AI!

[![Try Live Demo on Vercel](https://img.shields.io/badge/🚀%20Open%20Live%20App-Vercel-black?style=for-the-badge&logo=vercel&logoColor=white)](https://ai-lab-record-generator-two.vercel.app)
[![Try on GitHub Pages](https://img.shields.io/badge/🌐%20Alternative%20Link-GitHub%20Pages-10B981?style=for-the-badge&logo=github&logoColor=white)](https://ranjithbrs.github.io/AI-Lab-Record-Generator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

</div>

---

## 💡 What is this project?

Writing college lab records takes hours of searching textbooks, writing algorithms, formatting code, and drawing tables. 

**AI Lab Record Generator** solves this problem! It is a free, smart website that automatically writes a **complete, properly formatted lab record** for any experiment in **Computer Science, Physics, Chemistry, or Biology** — ready to copy or print as a PDF for college submission.

---

## 🎯 How to Use It (No Coding Required!)

You do **not** need to install anything on your computer. Just use it directly in your browser:

1. **Open the Website**: Click 👉 **[ai-lab-record-generator-two.vercel.app](https://ai-lab-record-generator-two.vercel.app)**.
2. **Sign In**: Enter your name to start.
3. **Pick Your Subject**: Choose from *Computer Science*, *Physics*, *Chemistry*, or *Biology*.
4. **Select or Type an Experiment**: 
   - Click one of the quick suggestion buttons (like *Binary Search*, *Ohm's Law*, or *Mitosis*), or type any custom experiment name.
5. **Click "Generate Lab Record"**:
   - In 2 seconds, you get a full lab record!
6. **Save or Print**:
   - 📄 **Download PDF / Print**: Generates a clean, college-style printable document with your name, date, and a teacher signature box.
   - 📋 **Copy to Clipboard**: Copy everything with one click to paste into Word or Google Docs.
   - ⬇️ **Download .txt**: Save as a plain text file.

---

## 📋 What Does Each Lab Record Include?

Depending on your subject, the app creates the exact academic format your professors expect:

### 💻 For Computer Science & IT:
* **🎯 Aim** — What the program does.
* **⚙️ Algorithm** — Step-by-step logic (Step 1, Step 2...).
* **💻 Program / Code** — Clean, tested code (Python, C, or Java) with comments.
* **📊 Expected Output** — What shows on the screen when the code runs.
* **✅ Result** — Final verification statement.

### 🔬 For Science Labs (Physics, Chemistry, Biology):
* **🎯 Aim** — Goal of the experiment.
* **📖 Theory & Formulas** — Scientific laws, equations, and principles.
* **🔬 Procedure** — Numbered instructions on how the experiment is performed.
* **📝 Observations & Readings** — Realistic sample measurement tables and values.
* **✅ Result** — Final calculated conclusions with units.

---

## 📚 Supported Experiments (Out of the Box)

Even without an internet connection or AI key, the generator has **24+ built-in, verified templates**:

| Subject | Popular Pre-Built Experiments |
|---|---|
| **💻 Computer Science** | Binary Search, Bubble Sort, Linear Search, Stack Operations, Queue Operations, Singly Linked List, Merge Sort, Quick Sort, Matrix Multiplication, SQL Queries (DDL & DML) |
| **⚡ Physics** | Ohm's Law, Simple Pendulum, Vernier Calipers, Screw Gauge, Meter Bridge, Spectrometer Prism, Young's Modulus (Uniform Bending), Torsional Pendulum |
| **🧪 Chemistry** | Water Hardness by EDTA, Conductometric Titration, Acid-Base Titration, Viscosity (Ostwald Viscometer), Surface Tension (Stalagmometer), Synthesis of Aspirin |
| **🧬 Biology & Biotech** | Mitosis in Onion Root Tip, Gram Staining of Bacteria, DNA Extraction from Plants, Food Tests (Carbohydrates & Proteins), Photosynthesis in Hydrilla |

> 🌟 **Have a custom experiment?** The system connects to **Google Gemini AI** to automatically write reports for **any other topic** in the world!

---

## ✨ Top Features

* 📱 **Works on Any Device** — Works smoothly on phones, tablets, and laptops.
* 🎨 **Clean, Modern Look** — Beautiful dark mode interface with smooth animations.
* 📄 **Print-Ready College Format** — Automatically switches to a clean black-and-white theme when printing to save printer ink and match official submission formats.
* 💡 **Clickable Suggestion Chips** — No need to guess what to type; click suggestions based on your subject.
* 🔒 **Private & Secure** — Your work stays in your browser; no personal passwords required.

---

## 🛠️ How It Works (For Tech Enthusiasts & Developers)

For developers curious about the underlying technology:

* **Frontend**: Pure HTML5, modern CSS3 (Glassmorphism design system), and Vanilla JavaScript (ES6+).
* **Backend**: Python 3.11+ using the **Flask** microframework.
* **AI Intelligence**: 
  1. **Primary**: Google Gemini 1.5/3.6 Flash API for real-time generative responses.
  2. **Secondary**: Hugging Face Inference API (`google/flan-t5-base`).
  3. **Zero-Downtime Fallback**: 24+ offline rule-based templates if APIs are busy or offline.
* **Cloud Hosting**: Deployed serverless on **Vercel** with static hosting mirrored on **GitHub Pages**.

---

## 💻 Running It Locally on Your Computer

If you want to run this project on your own machine:

### 1. Download the code
```bash
git clone https://github.com/ranjithbrs/AI-Lab-Record-Generator.git
cd AI-Lab-Record-Generator
```

### 2. Set up Python environment
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Start the application
```bash
python app.py
```

### 4. Open in your browser
Go to **`http://127.0.0.1:5000`** in Google Chrome or your favorite browser!

---

## 👨‍💻 Created By

**Ranjith B**  
🎓 *B.Tech Computer Science & Business Systems (CSBS)*  
🏛️ *Nehru Institute of Engineering and Technology, Coimbatore*  

* 🌐 **Live Website**: [ai-lab-record-generator-two.vercel.app](https://ai-lab-record-generator-two.vercel.app)
* 💼 **LinkedIn**: [linkedin.com/in/ranjith-b-csbs23](https://linkedin.com/in/ranjith-b-csbs23)
* 🐙 **GitHub**: [github.com/ranjithbrs](https://github.com/ranjithbrs)
* 🌐 **Portfolio**: [ranjithbrs.github.io/portfolio](https://ranjithbrs.github.io/portfolio/)
* 📧 **Email**: ranjithb2k06@gmail.com

---

## 📄 License

This project is open-source and free to use under the [MIT License](LICENSE). Feel free to share it with your classmates and teachers!
