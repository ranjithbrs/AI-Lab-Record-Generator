// ✅ LOGIN FUNCTION
function login() {
   let user = document.getElementById("Username").value;
   let pass = document.getElementById("Password").value;

   if(user && pass) {
      // Save username for later use
      localStorage.setItem("Username", user);

      // Redirect to form page
      window.location.href = "form.html";
   } else {
      alert("Please enter username and password");
   }
}

// ✅ REGISTER FUNCTION (optional, for register.html)
function registerUser() {
   let name = document.getElementById("Name").value;
   let mail = document.getElementById("MailId").value;
   let pass = document.getElementById("Password").value;

   if(name && mail && pass) {
      // Save registration details temporarily
      localStorage.setItem("Username", name);
      localStorage.setItem("MailId", mail);
      localStorage.setItem("Password", pass);

      alert("Account created successfully!");
      window.location.href = "form.html";
   } else {
      alert("Please fill all fields");
   }
}

// ✅ SUBMIT FUNCTION (form.html)
function submitForm() {
   let subject = document.getElementById("Subject").value;
   let experiment = document.getElementById("Experiment").value;

   // Save data in localStorage
   localStorage.setItem("Subject", subject);
   localStorage.setItem("Experiment", experiment);

   // Redirect to result page
   window.location.href = "result.html";
}

// ✅ GENERATE FUNCTION (result.html)
function generateRecord() {
   let user = localStorage.getItem("Username");
   let subject = localStorage.getItem("Subject");
   let experiment = localStorage.getItem("Experiment");

   document.getElementById("welcome").innerText = `Welcome, ${user}`;

   document.getElementById("LabRecord").innerHTML = `
      <h3>Aim</h3>
      <p>To study ${experiment}</p>

      <h3>Theory</h3>
      <p>${experiment} theory explanation goes here...</p>

      <h3>Procedure</h3>
      <p>Step-by-step procedure for ${experiment} will be listed here...</p>

      <h3>Result</h3>
      <p>Successfully performed ${experiment} in ${subject} lab.</p>
   `;
}

// ✅ COPY FUNCTION
function copyRecord() {
   let content = document.getElementById("LabRecord").innerText;
   navigator.clipboard.writeText(content);
   alert("Lab record copied to clipboard!");
}

// ✅ DOWNLOAD FUNCTION
function downloadRecord() {
   let content = document.getElementById("LabRecord").innerText;
   let blob = new Blob([content], { type: "text/plain" });
   let link = document.createElement("a");
   link.href = URL.createObjectURL(blob);
   link.download = "LabRecord.txt";
   link.click();
}
