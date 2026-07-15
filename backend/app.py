from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Example model
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

@app.route('/generate', methods=['POST'])
def generate_record():
    data = request.json
    subject = data.get("Subject")
    experiment = data.get("Experiment")

    # Build prompt for Hugging Face
    prompt = f"Generate a {subject} lab record for {experiment}. Include Aim, Theory/Algorithm, Procedure/Code, Output, Result."

    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()

    # Extract generated text safely
    generated_text = ""
    if isinstance(result, list) and "generated_text" in result[0]:
        generated_text = result[0]["generated_text"]
    elif "generated_text" in result:
        generated_text = result["generated_text"]

    # Different structures based on subject
    if subject.lower() in ["computer science", "cs", "programming", "cse"]:
        return jsonify({
            "Aim": f"To study {experiment}",
            "Algorithm": "Algorithm steps generated or described here...",
            "Code": "Program code generated or described here...",
            "Output": "Expected output generated or described here...",
            "Result": f"Successfully executed {experiment} in {subject} lab."
        })
    else:
        return jsonify({
            "Aim": f"To study {experiment}",
            "Theory": generated_text or f"Theory explanation for {experiment} goes here...",
            "Procedure": f"Step-by-step procedure for {experiment} in {subject} lab...",
            "Observation": "Observations/calculations go here...",
            "Result": f"Successfully performed {experiment} in {subject} lab."
        })

if __name__ == '__main__':
    app.run(debug=True)
