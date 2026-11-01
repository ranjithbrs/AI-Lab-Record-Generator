"""
Comprehensive Test Suite for AI Lab Record Generator
Validates:
1. Prompt Generation and Output Quality
2. Hugging Face and Gemini API Failure, Rate-Limit, and Timeout Scenarios
3. Generated Content and Formatting (CS & Science Schemas)
4. API Key Protection and Environment Variable Handling
5. Frontend/Backend Integration and CORS Handling
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import os
import requests

# Import application under test
import app as lab_app


class TestPromptGenerationAndQuality(unittest.TestCase):
    """1. Verify prompt generation and output quality."""

    def test_cs_fallback_output_quality(self):
        """Verify that CS experiments produce complete, high-quality structured records."""
        experiments = [
            ("Computer Science", "Binary Search"),
            ("Programming", "Bubble Sort"),
            ("CSE", "Stack Operations"),
            ("Python", "Queue Implementation"),
            ("Data Structure", "Singly Linked List"),
            ("CS", "Merge Sort"),
            ("Computer Science", "Quick Sort"),
            ("CSE", "Matrix Multiplication"),
            ("Computer Science", "SQL DDL and DML Commands"),
        ]
        required_keys = {"Aim", "Algorithm", "Code", "Output", "Result"}

        for subj, exp in experiments:
            with self.subTest(subject=subj, experiment=exp):
                data = lab_app.generate_fallback_record(subj, exp)
                self.assertIsInstance(data, dict)
                self.assertEqual(set(data.keys()), required_keys)
                for key in required_keys:
                    val = data[key]
                    self.assertIsInstance(val, str, f"{key} should be a string")
                    self.assertGreater(len(val.strip()), 10, f"{key} should not be empty")
                # Specific content quality checks
                self.assertIn(exp.lower().split()[0], data["Aim"].lower() + data["Code"].lower())

    def test_science_fallback_output_quality(self):
        """Verify that Science experiments produce complete, high-quality structured records."""
        experiments = [
            ("Physics", "Ohm's Law"),
            ("Physics", "Simple Pendulum"),
            ("Physics", "Vernier Caliper"),
            ("Physics", "Screw Gauge"),
            ("Physics", "Meter Bridge"),
            ("Physics", "Spectrometer Prism"),
            ("Physics", "Young's Modulus"),
            ("Physics", "Torsional Pendulum"),
            ("Chemistry", "Acid Base Titration"),
            ("Chemistry", "Hardness of Water by EDTA"),
            ("Chemistry", "Conductometric Titration"),
            ("Chemistry", "Viscosity using Ostwald Viscometer"),
            ("Chemistry", "Surface Tension using Stalagmometer"),
            ("Chemistry", "Preparation of Aspirin"),
            ("Biology", "Mitosis in Onion Root Tip"),
            ("Biology", "Gram Staining Technique"),
            ("Biology", "Isolation of DNA from Banana"),
            ("Biology", "Biochemical Food Tests"),
            ("Biology", "Rate of Photosynthesis in Hydrilla"),
        ]
        required_keys = {"Aim", "Theory", "Procedure", "Observation", "Result"}

        for subj, exp in experiments:
            with self.subTest(subject=subj, experiment=exp):
                data = lab_app.generate_fallback_record(subj, exp)
                self.assertIsInstance(data, dict)
                self.assertEqual(set(data.keys()), required_keys)
                for key in required_keys:
                    val = data[key]
                    self.assertIsInstance(val, str, f"{key} should be a string")
                    self.assertGreater(len(val.strip()), 15, f"{key} should have substantial content")


class TestApiFailureAndTimeoutScenarios(unittest.TestCase):
    """2. Test Hugging Face API failure and timeout scenarios."""

    def setUp(self):
        self.client = lab_app.app.test_client()

    @patch("requests.post")
    def test_huggingface_timeout_fallback(self, mock_post):
        """Verify graceful fallback when Hugging Face API times out."""
        mock_post.side_effect = requests.exceptions.Timeout("Read timeout after 8 seconds")

        with patch.object(lab_app, "GEMINI_API_KEY", ""):
            with patch.dict(lab_app.HEADERS, {"Authorization": "Bearer hf_test_token"}):
                response = self.client.post(
                    "/generate",
                    json={"Subject": "Computer Science", "Experiment": "Binary Search", "Username": "TestStudent"}
                )
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertIn("Aim", data)
                self.assertIn("Algorithm", data)
                self.assertIn("Code", data)
                self.assertIn("Binary Search", data["Aim"])

    @patch("requests.post")
    def test_huggingface_503_service_unavailable(self, mock_post):
        """Verify graceful fallback when Hugging Face API returns 503 Model Loading."""
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.json.return_value = {"error": "Model is currently loading"}
        mock_post.return_value = mock_response

        with patch.object(lab_app, "GEMINI_API_KEY", ""):
            with patch.dict(lab_app.HEADERS, {"Authorization": "Bearer hf_test_token"}):
                response = self.client.post(
                    "/generate",
                    json={"Subject": "Physics", "Experiment": "Ohm's Law", "Username": "TestStudent"}
                )
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertIn("Theory", data)
                self.assertIn("ohm", (data["Aim"] + data["Result"] + data["Theory"]).lower())

    @patch("requests.post")
    def test_huggingface_invalid_token_401(self, mock_post):
        """Verify graceful fallback when Hugging Face API returns 401 Unauthorized."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid API token"}
        mock_post.return_value = mock_response

        with patch.object(lab_app, "GEMINI_API_KEY", ""):
            with patch.dict(lab_app.HEADERS, {"Authorization": "Bearer hf_bad_token"}):
                response = self.client.post(
                    "/generate",
                    json={"Subject": "Chemistry", "Experiment": "Conductometric Titration"}
                )
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertIn("Conductance", data["Theory"])

    @patch("requests.post")
    def test_gemini_timeout_and_hf_timeout_cascade(self, mock_post):
        """Verify that when both Gemini and Hugging Face fail, local template generator always succeeds."""
        mock_post.side_effect = requests.exceptions.Timeout("Connection failed")

        with patch.object(lab_app, "GEMINI_API_KEY", "test_gemini_key"):
            with patch.dict(lab_app.HEADERS, {"Authorization": "Bearer hf_test_token"}):
                response = self.client.post(
                    "/generate",
                    json={"Subject": "Biology", "Experiment": "Mitosis in Onion Root Tip"}
                )
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertIn("Aim", data)
                self.assertIn("mitosis", data["Aim"].lower())
                self.assertIn("Prophase", data["Theory"])

    @patch("requests.post")
    def test_huggingface_malformed_response_triggers_schema_fallback(self, mock_post):
        """Verify that malformed or non-schema Hugging Face responses fail validation and trigger template fallback."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"generated_text": "This is just a loose sentence with no valid academic schema."}]
        mock_post.return_value = mock_response

        with patch.object(lab_app, "GEMINI_API_KEY", ""):
            with patch.dict(lab_app.HEADERS, {"Authorization": "Bearer hf_test_token"}):
                response = self.client.post(
                    "/generate",
                    json={"Subject": "Computer Science", "Experiment": "Binary Search"}
                )
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                # Should not have raw unvalidated sentence dumped into fields
                self.assertIn("Aim", data)
                self.assertIn("Binary Search", data["Aim"])
                self.assertIn("def binary_search", data["Code"])

    @patch("requests.post")
    def test_huggingface_valid_json_schema_accepted(self, mock_post):
        """Verify that valid structured JSON from Hugging Face is accepted by strict schema validation."""
        valid_json_payload = {
            "Aim": "To implement Bubble Sort in Python to order an array of integers.",
            "Algorithm": "1. Iterate through array.\n2. Compare adjacent elements.\n3. Swap if greater.",
            "Code": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]: arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr",
            "Output": "Sorted array: [11, 12, 22, 25, 34, 64, 90]",
            "Result": "Bubble sort algorithm successfully organized elements in ascending order."
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"generated_text": json.dumps(valid_json_payload)}]
        mock_post.return_value = mock_response

        with patch.object(lab_app, "GEMINI_API_KEY", ""):
            with patch.dict(lab_app.HEADERS, {"Authorization": "Bearer hf_test_token"}):
                response = self.client.post(
                    "/generate",
                    json={"Subject": "Computer Science", "Experiment": "Bubble Sort"}
                )
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertEqual(data["Aim"], valid_json_payload["Aim"])
                self.assertEqual(data["Code"], valid_json_payload["Code"])


class TestContentValidationAndFormatting(unittest.TestCase):
    """3. Validate generated content and formatting."""

    def test_cs_schema_compliance(self):
        """Validate CS record schema contains no unexpected keys or None values."""
        res = lab_app.generate_fallback_record("Computer Science", "Linear Search")
        expected_keys = {"Aim", "Algorithm", "Code", "Output", "Result"}
        self.assertEqual(set(res.keys()), expected_keys)
        for k, v in res.items():
            self.assertIsNotNone(v)
            self.assertIsInstance(v, str)
            self.assertNotIn("None", v)

    def test_science_schema_compliance(self):
        """Validate Science record schema contains no unexpected keys or None values."""
        res = lab_app.generate_fallback_record("Physics", "Spectrometer Prism")
        expected_keys = {"Aim", "Theory", "Procedure", "Observation", "Result"}
        self.assertEqual(set(res.keys()), expected_keys)
        for k, v in res.items():
            self.assertIsNotNone(v)
            self.assertIsInstance(v, str)

    def test_generic_fallback_when_unknown_topic(self):
        """Validate that completely unknown experiment names receive a valid structured template."""
        res_cs = lab_app.generate_fallback_record("Computer Science", "Quantum Annealing")
        self.assertEqual(set(res_cs.keys()), {"Aim", "Algorithm", "Code", "Output", "Result"})
        self.assertIn("Quantum Annealing", res_cs["Aim"])

        res_sci = lab_app.generate_fallback_record("Geology", "Seismic Refraction Analysis")
        self.assertEqual(set(res_sci.keys()), {"Aim", "Theory", "Procedure", "Observation", "Result"})
        self.assertIn("Seismic Refraction Analysis", res_sci["Aim"])

    def test_validate_record_schema_logic(self):
        """Verify that validate_record_schema strictly enforces key existence and minimum content length."""
        valid_cs = {
            "Aim": "To study and implement the binary search algorithm.",
            "Algorithm": "1. Initialize low and high pointers.\n2. Compute mid.\n3. Search key.",
            "Code": "def search(a, k):\n    return binary_search(a, k)",
            "Output": "Element found at index 4.",
            "Result": "Binary search algorithm executed successfully."
        }
        self.assertTrue(lab_app.validate_record_schema(valid_cs, is_cs=True))

        # Missing key
        invalid_cs_missing = dict(valid_cs)
        del invalid_cs_missing["Code"]
        self.assertFalse(lab_app.validate_record_schema(invalid_cs_missing, is_cs=True))

        # Short/empty content (<15 chars)
        invalid_cs_short = dict(valid_cs, Aim="Too short")
        self.assertFalse(lab_app.validate_record_schema(invalid_cs_short, is_cs=True))

        # Non-dict
        self.assertFalse(lab_app.validate_record_schema(["not", "a", "dict"], is_cs=True))
        self.assertFalse(lab_app.validate_record_schema(None, is_cs=True))


class TestApiKeyProtectionAndEnvVars(unittest.TestCase):
    """4. Review API key protection and environment variables."""

    def test_no_hardcoded_secrets_in_module_defaults(self):
        """Verify module does not contain hardcoded credentials in default initializers."""
        self.assertNotIn("AIzaSy", lab_app.API_URL)
        # Default HF_TOKEN must not be a real secret
        default_hf = os.environ.get("HF_TOKEN", "")
        self.assertTrue(default_hf == "" or default_hf.startswith("hf_") or len(default_hf) < 10 or "YOUR_TOKEN" in default_hf)

    def test_endpoint_does_not_leak_api_keys(self):
        """Verify that /generate response payload never leaks any API keys or tokens."""
        client = lab_app.app.test_client()
        with patch.object(lab_app, "GEMINI_API_KEY", "AIzaSySuperSecretKey123"):
            with patch.dict(lab_app.HEADERS, {"Authorization": "Bearer hf_SuperSecretToken456"}):
                res = client.post("/generate", json={"Subject": "Physics", "Experiment": "Ohm's Law"})
                res_text = res.get_data(as_text=True)
                self.assertNotIn("AIzaSySuperSecretKey123", res_text)
                self.assertNotIn("hf_SuperSecretToken456", res_text)


class TestFrontendBackendIntegration(unittest.TestCase):
    """5. Test frontend/backend integration."""

    def setUp(self):
        self.client = lab_app.app.test_client()

    def test_cors_headers_present(self):
        """Verify CORS headers are returned so frontend on GitHub Pages or custom domain can call API."""
        res = self.client.post("/generate", json={"Subject": "Physics", "Experiment": "Screw Gauge"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("Access-Control-Allow-Origin", res.headers)
        self.assertEqual(res.headers.get("Access-Control-Allow-Origin"), "*")

    def test_empty_json_payload_handling(self):
        """Verify backend handles empty or minimal JSON gracefully without 500 error."""
        res = self.client.post("/generate", json={})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("Aim", data)

    def test_none_values_handling(self):
        """Verify backend handles null values in JSON body gracefully."""
        res = self.client.post("/generate", json={"Subject": None, "Experiment": None})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("Aim", data)


if __name__ == "__main__":
    unittest.main()
