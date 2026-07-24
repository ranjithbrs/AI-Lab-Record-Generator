# AI Lab Record Generator

An intelligent web application to automate lab record creation for students in **Computer Science** and **Science subjects (Physics, Chemistry, Biology)**.

## 🌐 Live Demo
Experience the project live on Vercel: **[AI Lab Record Generator](https://ai-lab-record-generator-two.vercel.app)**

---

## 🚀 Features
- **Modern Glassmorphism UI** with dark mode aesthetics and smooth micro-animations
- **User Access & Auth Flow** (Login & Register pages with persistent local session)
- **Smart Experiment Generator**:
  - **CS / Programming Labs** → Aim, Algorithm, Code / Program, Output, Result
  - **General Science Labs** → Aim, Theory, Procedure, Observation, Result
- **Instant Save Tools**: One-click **Copy to Clipboard** and **Download .txt Record**
- **Robust Fallback Engine**: Works seamlessly online and offline via rule-based AI template fallback

---

## 🛠️ Tech Stack
- **Frontend**: HTML5, Modern CSS3 (Glassmorphism), JavaScript (ES6+)
- **Backend**: Python 3.14, Flask, Flask-CORS, Requests
- **Deployment**: Vercel Serverless Functions

---

## 📂 Project Structure
```text
AI-Lab-Record-Generator/
├── api/
│   └── index.py         # Vercel Serverless Function entry point
├── backend/
│   └── app.py           # Local Flask server
├── public/              # Static Frontend Assets
│   ├── index.html       # Login Page (Root)
│   ├── login.html       # Login Page
│   ├── register.html    # Register Page
│   ├── form.html        # Experiment Details Form
│   ├── result.html      # Dynamic Record Display Page
│   ├── script.js        # Frontend Logic & API Integration
│   └── style.css        # Glassmorphic Stylesheet
├── requirements.txt     # Python Dependencies
├── vercel.json          # Vercel Serverless & Static Rewrite Config
└── README.md            # Documentation
```

---

## ⚡ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ranjithbrs/AI-Lab-Record-Generator.git
   cd AI-Lab-Record-Generator
   ```

2. **Set up virtual environment & install dependencies:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # On Windows
   # source .venv/bin/activate # On Linux/macOS
   pip install -r requirements.txt
   ```

3. **Start the Flask Backend:**
   ```bash
   python backend/app.py
   ```

4. **Open Frontend:**
   Open `public/login.html` or `public/index.html` in any web browser!

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
