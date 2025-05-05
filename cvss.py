import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------------------------
# 📥 Extract for Dashboard
# -------------------------
def extract_vulnerability_data(file):
    raw_data = json.load(file)
    output = []

    for result in raw_data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            entry = {
                "id": vuln.get("VulnerabilityID", ""),
                "cvss": vuln.get("CVSS", {}).get("ghsa", {}).get("V3Score", ""),
                "publishedDate": vuln.get("PublishedDate", "")[:10],
                "cwe": vuln.get("CweIDs", [""])[0] if vuln.get("CweIDs") else ""
            }
            output.append(entry)
    return output

# -------------------------
# 📥 Extract for Email
# -------------------------
def extract_email_data(file):
    file.seek(0)
    raw_data = json.load(file)
    output = []

    for result in raw_data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            entry = {
                "id": vuln.get("VulnerabilityID", ""),
                "description": vuln.get("Description", "No description provided."),
                "installed_version": vuln.get("InstalledVersion", "N/A"),
                "fixed_version": vuln.get("FixedVersion", "N/A"),
                "cvss": vuln.get("CVSS", {}).get("nvd", {}).get("V3Score", 0),
                "suggestion": vuln.get("PrimaryURL", "Please check the advisory for more details.")
            }
            output.append(entry)
    return output

def preprocess_data(df):
    df['publishedDate'] = pd.to_datetime(df['publishedDate'], errors='coerce')
    df['cvss'] = pd.to_numeric(df['cvss'], errors='coerce')  # Convert CVSS to float
    df['Year'] = df['publishedDate'].dt.year
    df['Month'] = df['publishedDate'].dt.to_period('M')
    return df

# -------------------------
# 📧 Email Report
# -------------------------
def send_email(receiver_email, top_vulns):
    EMAIL_ADDRESS = "aibomgenerator@gmail.com"
    EMAIL_PASSWORD = "yawj eczy bcje aovh"

    subject = "🚨 Detailed Vulnerability Report (Top 5 by CVSS)"

    body = "Hi there,\n\nHere are the top 5 critical vulnerabilities:\n\n"
    for idx, row in top_vulns.iterrows():
        body += f"""🔐 Vulnerability ID: {row['id']}
📄 Description: {row['description']}
📦 Installed Version: {row['installed_version']}
🛠️ Fixed Version: {row['fixed_version']}
📊 CVSS Score: {row['cvss']}
💡 Suggestion: {row['suggestion']}

"""

    body += "Stay Secure,\nYour AIBOM Framework 💻"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

# -------------------------
# 🚀 Streamlit App
# -------------------------
def main():
    st.title("🛡️ CVE Dashboard + Vulnerability Email Report")
    st.write("Upload your `vulnerabilities.json` to view filtered CVEs and receive an email summary.")

    uploaded_file = st.file_uploader("📂 Upload JSON File", type="json")

    if uploaded_file:
        # Dashboard display
        filtered_data = extract_vulnerability_data(uploaded_file)

        with open("filtered_vulnerabilities.json", "w") as outfile:
            json.dump(filtered_data, outfile, indent=2)

        st.success("✅ Filtered vulnerabilities saved as filtered_vulnerabilities.json")

        # Email preparation

        email_data = extract_email_data(uploaded_file)
        df_email = pd.DataFrame(email_data)
        df_email['cvss'] = pd.to_numeric(df_email['cvss'], errors='coerce')
        top5 = df_email.sort_values(by="cvss", ascending=False).head(5)

        st.subheader("📧 Enter your email to receive full vulnerability report")
        user_email = st.text_input("Email Address")

        if user_email and st.button("Send Email Report"):
            if send_email(user_email, top5):
                st.success("💌 Email sent successfully!")
            else:
                st.error("❌ Email failed to send. Please check credentials or network.")

        # Step 2: Load into DataFrame
        df = pd.DataFrame(filtered_data)
        df = preprocess_data(df)

        st.subheader("📊 Sample of Filtered CVE Data")
        st.dataframe(df.head())

        # CVSS Score Trend Over Time
        st.subheader("📈 CVSS Score Trend Over Time")
        trend_df = df.groupby("Month")["cvss"].mean().reset_index()
        trend_df["Month"] = trend_df["Month"].astype(str)

        plt.figure(figsize=(10, 4))
        sns.lineplot(data=trend_df, x="Month", y="cvss", marker="o")
        plt.xticks(rotation=45)
        plt.ylabel("Average CVSS Score")
        plt.title("Average CVSS Score by Month")
        st.pyplot(plt.gcf())

        # Monthly Vulnerability Counts
        st.subheader("🗓️ Number of Vulnerabilities per Month")
        count_df = df.groupby("Month")["id"].count().reset_index(name="count")
        count_df["Month"] = count_df["Month"].astype(str)

        plt.figure(figsize=(10, 4))
        sns.barplot(data=count_df, x="Month", y="count")
        plt.xticks(rotation=45)
        plt.ylabel("Number of Vulnerabilities")
        plt.title("Monthly Vulnerability Counts")
        st.pyplot(plt.gcf())

        # Critical Vulnerabilities (CVSS > 7)
        st.subheader("🔥 Critical Vulnerabilities per Month (CVSS > 7)")
        critical_df = df[df["cvss"] > 7]
        crit_count_df = critical_df.groupby("Month")["id"].count().reset_index(name="critical_count")
        crit_count_df["Month"] = crit_count_df["Month"].astype(str)

        plt.figure(figsize=(10, 4))
        sns.lineplot(data=crit_count_df, x="Month", y="critical_count", marker="o", color='red')
        plt.xticks(rotation=45)
        plt.ylabel("Critical Vulnerabilities")
        plt.title("Monthly Critical Vulnerabilities")
        st.pyplot(plt.gcf())

        # CWE Analysis
        st.subheader("🛠️ Most Common CWEs (Software Weaknesses)")
        cwe_counts = df["cwe"].value_counts().head(10).reset_index()
        cwe_counts.columns = ["CWE", "Count"]

        plt.figure(figsize=(8, 4))
        sns.barplot(data=cwe_counts, x="Count", y="CWE", palette="mako")
        plt.xlabel("Count")
        plt.ylabel("CWE")
        plt.title("Top 10 Common Software Weaknesses (CWEs)")
        st.pyplot(plt.gcf())


        

if __name__ == "__main__":
    main()
