# CI/CD Pipeline for AI BOM Generator

This Jenkins pipeline automates the process of fetching, building, testing, and promoting an AI-based Bill of Materials (AIBOM) model. The pipeline ensures that the model is properly validated, tested, and checked for security vulnerabilities before deployment.

## 📌 Pipeline Stages

### 1️⃣ **Build**

- Cleans the existing model directory.
- Fetches the model from either a GitHub repository or a local path.
- Ensures essential files (`dataset.json` and `model_info.json`) exist.

### 2️⃣ **Deploy**

- Fetches the AIBOM script from the predefined repository.
- Copies the necessary script (`generate_aibom.py`) into the model directory.

### 3️⃣ **Test**

- Installs security tools (**Syft** and **Trivy**) for Software Bill of Materials (SBOM) and vulnerability scanning.
- Runs the AIBOM script to generate reports.
- Ensures that the reports directory is created.

### 4️⃣ **Promote**

- Validates the generated reports (`aibom.json`, `sbom.json`, `vulnerability.json`).
- Checks for security vulnerabilities in the `vulnerability.json` file.
- Displays the generated reports.

## 🔧 **Setup & Configuration**

### **Pipeline Parameters**

| Parameter          | Default Value | Description                                   |
| ------------------ | ------------- | --------------------------------------------- |
| `MODEL_GIT_URL`    | `""` (empty)  | GitHub repository URL for fetching the model. |
| `MODEL_LOCAL_PATH` | `""` (empty)  | Local path to fetch the model.                |

### **Environment Variables**

| Variable             | Description                                             |
| -------------------- | ------------------------------------------------------- |
| `GIT_CREDENTIALS_ID` | Jenkins credential ID for accessing private GitHub repositories. |
| `MODEL_DIR`          | Directory where the model files will be stored.        |
| `SCRIPT_REPO`        | GitHub repository URL for fetching AIBOM script (change as per requirement). |
| `REPORT_DIR`         | Directory where reports will be stored.                |
| `TOOLS_DIR`          | Directory for storing installed security tools.        |

## 📂 **Model Directory Structure**

The model directory must contain the following essential files:

```
MODEL_DIR/
├── dataset.json       # Dataset file required for the model
├── model_info.json    # Model metadata and configurations
```

## 🚀 **Running the Pipeline**

### **Prerequisites**
Before running the pipeline, ensure that **Python or Python3** is installed on the system.

### **Execution Steps**
1. Configure the `MODEL_GIT_URL` or `MODEL_LOCAL_PATH` as parameters.
2. Run the pipeline from Jenkins.
3. Monitor the console output for errors or warnings.

## ✅ **Success Criteria**

- Model is successfully fetched.
- Required files exist in the model directory.
- Security tools are installed and executed without errors.
- Vulnerability scan shows no critical issues.
- Reports are successfully generated in the `reports/` directory.

## ⚠️ **Failure Scenarios**

- Missing model files (`dataset.json` or `model_info.json`).
- Pipeline fails due to security vulnerabilities in the model.
- Reports not generated properly.

## 📝 **Post-Pipeline Execution**

- If the pipeline fails, check the logs for errors.
- If the pipeline succeeds, review the generated reports.
- Take necessary actions based on security scan results before promoting the model.

### Notes:

Ensure that the provided model directory contains valid model files before running the script.
The LOCAL_PATH environment variable must be set for successful execution
----
