# AIBOM_Generator

AIBOM Generation Tool

Overview

The AIBOM (AI Bill of Materials) Generation Tool automates the process of generating:

AIBOM (AI Bill of Materials)

SBOM (Software Bill of Materials)

Vulnerability Report


This tool is designed to work with various AI models by allowing users to provide their own model directory. It ensures flexibility by keeping model dependencies separate from the tool itself. Additionally, the tool integrates security scanning using Syft and Trivy to detect vulnerabilities.


---

Installation

1. Install General Dependencies

Before running the script, install the required dependencies:

pip install numpy pandas json5

2. Install Security Tools

The script requires Syft and Trivy for SBOM and vulnerability analysis. Install them using:

pip install syft

Download and install Trivy from the official source:
Trivy Installation Guide

3. Install Model-Specific Dependencies

Since different AI models have unique requirements, install dependencies based on your model type:

For PyTorch-based models (e.g., GPT-2, BERT, LLaMA):

pip install torch transformers

For TensorFlow-based models:

pip install tensorflow

For other models: Refer to the official documentation and install the necessary libraries.



---

Usage

Command to Run the Script

Execute the script by providing the model directory path:

python generate_aibom.py --model-path /path/to/your/model

Example

If the AI model is stored in /home/user/models/gpt-2, use:

python generate_aibom.py --model-path /home/user/models/gpt-2

The script will analyze the model directory, extract dependencies, and generate corresponding reports.


---

Output

Upon successful execution, the script will generate three reports inside the reports/ directory:

aibom.json – AI Bill of Materials

sbom.json – Software Bill of Materials

vulnerability_report.json – Security vulnerabilities detected


If vulnerabilities are found in vulnerability_report.json, the script will display:

⚠️ WARNING: Model has vulnerabilities! Not ready for production. ⚠️

If no vulnerabilities are found, it will display:

✅ Model passes security checks.


---

Handling Environment Variables

The script requires environment variables for correct execution:

LOCAL_PATH – Must be set before running the script.


Ensure it is defined in your shell session:

export LOCAL_PATH=/path/to/your/local/directory

For Windows (PowerShell):

$env:LOCAL_PATH="C:\path\to\your\local\directory"


---

Directory Structure

After running the script, the expected directory structure is:

/path/to/your/model/
│── reports/
│ ├── aibom.json
│ ├── sbom.json
│ ├── vulnerability_report.json
│── other_model_files/


---

License

This project is open-source. Feel free to use, modify, and contribute!


---

Notes:

This script does not include model-specific dependencies; users must install them separately.

Ensure that the provided model directory contains valid model files before running the script.

The LOCAL_PATH environment variable must be set for successful execution
