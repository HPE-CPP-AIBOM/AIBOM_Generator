# Automated framework for generation and maintainence of generation and maintainence of AI Bill of meterials

This Jenkins CI/CD pipeline automates the complete lifecycle of an **AI-based Bill of Materials (AIBOM)** generation framework. It ensures that AI models are securely fetched, validated, scanned for vulnerabilities, and documented using AIBOM and SBOM reports.

It enhances security, traceability, and transparency throughout the AI model lifecycle.



### Pipeline Overview

**Pipeline Stages**


# 1. Build Stage

- Cleans the working model directory (MODEL_DIR) to avoid leftover data.

- Fetches the AI model from either:

    - A GitHub repository (MODEL_GIT_URL), or

    - A specified local path (MODEL_LOCAL_PATH).

    - Verifies the presence of required files:

    - dataset.json — dataset metadata.

    - model_info.json — AI model details, training specs, and configurations.



# 2. Deploy Stage

- Clones the AIBOM generation script from the specified script repository (SCRIPT_REPO).

- Copy the script generate_aibom.py into the model directory for execution.

# 3. Test Stage

- Installs Syft to generate SBOM (Software Bill of Materials).

- Installs Trivy for scanning vulnerabilities.

- Executes the AIBOM generation script, which performs:

- AIBOM report generation (aibom.json)

- SBOM report creation (sbom.json)

- Vulnerability analysis (vulnerability_requirements.json and vulnerability_sbom.json)

- Merging of vulnerabilities into merged_vulnerabilities.json

- Ensures the reports/ folder is created and populated.



# 4. Promote Stage

- Validates the presence and format of reports.

- Parses vulnerability data to ensure no critical issues are present.

- Displays generated reports in the Jenkins console for review.

# 5. 
- Launch the CVSS dashboard to visualize vulnerabilities.
- The dashboard is accessible at http://localhost:8501.

# Setup & Configuration

# Pipeline Parameters

| Parameter           | Default Value | Description                                                  |
|---------------------|----------------|--------------------------------------------------------------|
| `MODEL_GIT_URL`     | `""`           | GitHub URL to fetch the model repository.                   |
| `MODEL_LOCAL_PATH`  | `""`           | Local directory path containing model files.                |

> **Note:** Provide either `MODEL_GIT_URL` or `MODEL_LOCAL_PATH`—not both.



# Environment Variables

| Variable            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `GIT_CREDENTIALS_ID`| Jenkins credentials for accessing private GitHub repositories.              |
| `MODEL_DIR`         | Working directory for downloaded or copied model files.                     |
| `SCRIPT_REPO`       | Repository URL containing `generate_aibom.py`.                              |
| `REPORT_DIR`        | Output directory for all reports.                                           |
| `TOOLS_DIR`         | Directory for Syft and Trivy installations.                                 |
| `USER_EMAIL`        | Email ID to receive vulnerability alerts via the Streamlit dashboard.       |


# Required Directory Structure

The MODEL_DIR must contain:

MODEL_DIR/

├── dataset.json                # Dataset metadata

├── model_info.json             # AI model specifications

├── generate_aibom.py           # (Automatically copied during Deploy stage)



# How to Run the Pipeline


**Prerequisites**

- Jenkins and Python 3.x are installed on the agent machine.

- Internet access is required to install tools and clone repositories.

- Environment variables and parameters are properly configured.


**Execution Steps**

- Navigate to Jenkins > New Pipeline.

- Enter MODEL_GIT_URL or MODEL_LOCAL_PATH.

- Set USER_EMAIL for dashboard notification (if enabled).

- Run the pipeline and monitor output in the Jenkins console.



**Streamlit Dashboard – Vulnerability Visualisation**

- After report generation, a Streamlit-based dashboard is automatically launched that visualises vulnerabilities using four detailed graphs:

    - Vulnerabilities by CVSS Severity

    - Vulnerabilities by CWE (Common Weakness Enumeration)

    - Time-based Vulnerability Trends (if data available)

    - Vulnerability Source Comparison: requirements.txt vs. SBOM


**Email Alert Feature**

- The dashboard includes a text field where users can enter their email address.

- On submission, the system sends a detailed report with:

    - Top 5 Critical Vulnerabilities

    - A direct suggestion link to AquaSec Vulnerability Advisory

    - This ensures real-time awareness and actionable insight for developers and security teams.


# Success Criteria

- The model is fetched successfully from Git or local.

- Required files (dataset.json, model_info.json) are validated.

- Reports (aibom.json, sbom.json, vulnerability.json) are generated.

- Streamlit dashboard runs successfully with the email alert feature.

