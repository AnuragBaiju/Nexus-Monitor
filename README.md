# ⚡️ Nexus Monitor: Serverless Website Health Tracker

![Status](https://img.shields.io/badge/status-active-success.svg)
![AWS](https://img.shields.io/badge/AWS-Lambda%20|%20DynamoDB%20|%20S3%20|%20API%20Gateway%20|%20SNS-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Nexus Monitor** is a fully serverless, event-driven application that tracks website uptime and latency in real-time. Built 100% on AWS Cloud services, it features a modern glassmorphism dashboard, automated alerts, and minute-by-minute data visualization.

---

## 🏗 Architecture

The system leverages a **Serverless Architecture** to ensure high availability, zero server management, and near-zero cost.

![Architecture Diagram](https://my-health-dashboard-123.s3.us-east-1.amazonaws.com/screenshots/nexus-architecture.jpg)

1.  **EventBridge Scheduler:** Triggers the health check Lambda every 1 minute.
2.  **AWS Lambda (Checker):** Python script that pings the target URL, calculates latency, and verifies HTTP status codes.
3.  **Amazon DynamoDB:** NoSQL database storing time-series data (Timestamp, Latency, Status) with TTL (Time-To-Live) enabled for auto-cleanup.
4.  **Amazon SNS:** Publishes instant email alerts if the website returns a non-200 status code.
5.  **AWS Lambda (Reader):** Fetches historical data from DynamoDB and formats it for the frontend.
6.  **Amazon API Gateway:** Exposes the Reader Lambda via a secure REST API endpoint.
7.  **Amazon S3 & CloudFront:** Hosts the static HTML/JS dashboard with global content delivery.

---

## 📸 Dashboard & Features

### 1. Real-Time Monitoring (Operational)
A responsive, glassmorphism UI built with vanilla HTML/CSS and Chart.js. It visualizes latency trends and allows toggling between 10-minute, 1-hour, and 24-hour views.

![Operational Dashboard](https://my-health-dashboard-123.s3.us-east-1.amazonaws.com/screenshots/Screenshot+2025-12-03+at+15.41.15.png)

### 2. Incident Response System
The system is "Event-Driven." If the target website goes down or returns an error (e.g., 404, 500), the UI updates instantly to a **Critical State**, and the backend triggers an **SNS Alert**.

**Critical Dashboard View:**
![Critical Dashboard](https://my-health-dashboard-123.s3.us-east-1.amazonaws.com/screenshots/Screenshot+2025-12-03+at+15.28.15.png)

**Automated Email Notification:**
![Email Alert](https://my-health-dashboard-123.s3.us-east-1.amazonaws.com/screenshots/Screenshot+2025-12-03+at+16.02.08.png)

---

## 🛠 Tech Stack

* **Cloud Provider:** Amazon Web Services (AWS)
* **Infrastructure:** Lambda, DynamoDB, API Gateway, EventBridge, SNS, S3
* **Backend Code:** Python 3.12 (Boto3, Urllib3)
* **Frontend:** HTML5, CSS3 (Glassmorphism UI), Chart.js
* **Version Control:** Git & GitHub

---

## 💻 How to Deploy

### 1. Backend Setup (AWS)
1.  **DynamoDB:** Create a table named `WebsiteHealth` with Partition Key: `UrlID` (String) and Sort Key: `Timestamp` (String).
2.  **SNS Topic:** Create a Standard Topic named `WebsiteDownAlerts` and subscribe your email.
3.  **IAM Role:** Create a role with permissions for `DynamoDBFullAccess` and `AmazonSNSFullAccess`.

### 2. Lambda Functions
* **Checker Function (`backend/checker.py`):**
    * Set environment variables or hardcode your target URL and SNS ARN.
    * Set EventBridge Scheduler to trigger this function every `rate(1 minute)`.
* **Reader Function (`backend/reader.py`):**
    * Deploy this function to read from DynamoDB.
    * Connect it to **API Gateway** (HTTP API) with a `GET` route.
    * Enable **CORS** (Access-Control-Allow-Origin: `*`).

### 3. Frontend Deployment
1.  Open `index.html`.
2.  Replace the placeholder API URL with your actual **API Gateway Invoke URL**:
    ```javascript
    const API_URL = "[https://your-api-id.execute-api.us-east-1.amazonaws.com](https://your-api-id.execute-api.us-east-1.amazonaws.com)";
    ```
3.  Create an **S3 Bucket** and enable **Static Website Hosting**.
4.  Upload `index.html`.
5.  Update the **Bucket Policy** to allow public read access (`s3:GetObject`).

---

## 🧠 What I Learned
* **Event-Driven Design:** How to decouple check logic (Lambda A) from data retrieval (Lambda B).
* **NoSQL Modeling:** Designing a DynamoDB schema for efficient time-series querying.
* **CORS & Security:** Configuring API Gateway to securely serve data to a static frontend.
* **Cost Optimization:** Leveraging AWS Free Tier limits for 24/7 monitoring without incurring costs.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.


