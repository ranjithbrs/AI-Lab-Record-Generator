// Show a transient notification toast
function showToast(message) {
    let toast = document.getElementById("toast");
    if (!toast) {
        toast = document.createElement("div");
        toast.id = "toast";
        toast.className = "toast";
        document.body.appendChild(toast);
    }
    toast.innerHTML = `✨ ${message}`;
    toast.classList.add("show");
    setTimeout(() => {
        toast.classList.remove("show");
    }, 2500);
}

// 1. User Authentication (Login / Register)
function login() {
    const usernameInput = document.getElementById("Username");
    if (usernameInput && usernameInput.value.trim() !== "") {
        localStorage.setItem("username", usernameInput.value.trim());
        window.location.href = "form.html";
    }
}

function registerUser() {
    const nameInput = document.getElementById("Name");
    if (nameInput && nameInput.value.trim() !== "") {
        localStorage.setItem("username", nameInput.value.trim());
        showToast("Registration successful! Redirecting to login...");
        setTimeout(() => {
            window.location.href = "login.html";
        }, 1200);
    }
}

// Helper to check authentication and load username on Form Page
function checkAuth() {
    const username = localStorage.getItem("username");
    if (!username) {
        // If not logged in, redirect to login page
        window.location.href = "login.html";
        return;
    }
    const welcomeHeader = document.getElementById("welcome-user");
    if (welcomeHeader) {
        welcomeHeader.innerText = username;
    }
}

// Logout user
function logout() {
    localStorage.removeItem("username");
    window.location.href = "login.html";
}

// 2. Submit Experiment details from Form Page
function submitExperimentForm() {
    const subject = document.getElementById("Subject").value;
    const experiment = document.getElementById("Experiment").value;
    
    if (subject && experiment) {
        window.location.href = `result.html?subject=${encodeURIComponent(subject)}&experiment=${encodeURIComponent(experiment)}`;
    }
}

// Helper to format record text for copying/downloading
function formatRecordText(data, subject, experiment) {
    let text = `AI LAB RECORD GENERATOR\n`;
    text += `=========================================\n`;
    text += `Subject   : ${subject}\n`;
    text += `Experiment: ${experiment}\n`;
    text += `=========================================\n\n`;
    
    text += `AIM:\n${data.Aim || 'To study the experiment.'}\n\n`;
    
    if (data.Algorithm) {
        text += `ALGORITHM:\n${data.Algorithm}\n\n`;
        text += `PROGRAM / CODE:\n${data.Code}\n\n`;
        text += `EXPECTED OUTPUT:\n${data.Output}\n\n`;
    } else {
        text += `THEORY:\n${data.Theory}\n\n`;
        text += `PROCEDURE:\n${data.Procedure}\n\n`;
        text += `OBSERVATION / DISCUSSION:\n${data.Observation}\n\n`;
    }
    
    text += `RESULT / CONCLUSION:\n${data.Result}\n`;
    text += `=========================================\n`;
    return text;
}

// Store generated data globally on the page for copy/download scripts
let currentRecordData = null;
let currentSubject = "";
let currentExperiment = "";

// 3. Load Result Page details and call backend API
async function loadResultPage() {
    const params = new URLSearchParams(window.location.search);
    const subject = params.get("subject");
    const experiment = params.get("experiment");
    const username = localStorage.getItem("username") || "Student";
    
    if (!subject || !experiment) {
        document.getElementById("error-container").style.display = "block";
        document.getElementById("loading-container").style.display = "none";
        return;
    }

    currentSubject = subject;
    currentExperiment = experiment;
    
    document.getElementById("display-subject").innerText = subject;
    document.getElementById("display-experiment").innerText = experiment;
    
    try {
        const response = await fetch("http://127.0.0.1:5000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                Subject: subject,
                Experiment: experiment,
                Username: username
            })
        });
        
        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }
        
        const data = await response.json();
        currentRecordData = data;
        
        // Hide loading indicator
        document.getElementById("loading-container").style.display = "none";
        
        const recordContent = document.getElementById("record-content");
        recordContent.style.display = "block";
        
        // Populate Aim and Result (common to both layout variants)
        document.getElementById("val-aim").innerText = data.Aim || "...";
        document.getElementById("val-result").innerText = data.Result || "...";
        
        // Check layout structure from backend response
        if (data.Algorithm) {
            // CS/Programming Layout
            document.getElementById("cs-layout").style.display = "block";
            document.getElementById("val-algorithm").innerText = data.Algorithm || "...";
            document.getElementById("val-code").innerText = data.Code || "...";
            document.getElementById("val-output").innerText = data.Output || "...";
        } else {
            // General Science Layout
            document.getElementById("science-layout").style.display = "block";
            document.getElementById("val-theory").innerText = data.Theory || "...";
            document.getElementById("val-procedure").innerText = data.Procedure || "...";
            document.getElementById("val-observation").innerText = data.Observation || "...";
        }
        
    } catch (error) {
        console.error("❌ Error generating lab record:", error);
        document.getElementById("loading-container").style.display = "none";
        document.getElementById("error-container").style.display = "block";
        document.getElementById("error-message").innerText = `Could not connect to generator: ${error.message}`;
    }
}

// 4. Action functions on Result Page
function copyToClipboard() {
    if (!currentRecordData) return;
    
    const formattedText = formatRecordText(currentRecordData, currentSubject, currentExperiment);
    navigator.clipboard.writeText(formattedText)
        .then(() => {
            showToast("Copied record to clipboard!");
        })
        .catch(err => {
            console.error("Failed to copy text: ", err);
            showToast("Failed to copy. Please select and copy manually.");
        });
}

function downloadRecord() {
    if (!currentRecordData) return;
    
    const formattedText = formatRecordText(currentRecordData, currentSubject, currentExperiment);
    const blob = new Blob([formattedText], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement("a");
    const sanitizedTitle = currentExperiment.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    a.href = url;
    a.download = `${sanitizedTitle}_lab_record.txt`;
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast("Downloaded record successfully!");
}

// Initialize scripts based on which page is active
window.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;
    
    if (path.includes("form.html")) {
        checkAuth();
    } else if (path.includes("result.html")) {
        loadResultPage();
    }
});
