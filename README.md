# ⚡️ Nexus Monitor: Serverless Website Health Tracker

![Status](https://img.shields.io/badge/status-active-success.svg)
![AWS](https://img.shields.io/badge/AWS-Lambda%20|%20DynamoDB%20|%20S3%20|%20API%20Gateway%20|%20SNS-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Nexus Monitor** is a fully serverless, event-driven application that tracks website uptime and latency in real-time. Built 100% on AWS Cloud services, it features a modern glassmorphism dashboard, automated alerts, and minute-by-minute data visualization.

---

## 🏗 Architecture

The system leverages a **Serverless Architecture** to ensure high availability, zero server management, and near-zero cost.

graph TD
    %% Define Styles
    classDef aws fill:#FF9900,stroke:#232F3E,color:white,stroke-width:2px;
    classDef external fill:#fff,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;
    
    %% Actors and External Systems
    User[User / Browser]
    TargetWeb[Target Website]:::external
    Email[Admin Email]:::external

    %% Frontend Stack
    subgraph Frontend_Hosting [Frontend Hosting]
        S3[S3 Bucket<br/>(Static Website)]:::aws
    end

    %% Backend Stack
    subgraph Serverless_Backend [Serverless Backend]
        Scheduler[EventBridge<br/>(1-min Trigger)]:::aws
        Checker[Lambda A<br/>(Checker)]:::aws
        Reader[Lambda B<br/>(Reader)]:::aws
        DB[(DynamoDB<br/>WebsiteHealth)]:::aws
        API[API Gateway<br/>(HTTP API)]:::aws
        SNS[SNS Topic<br/>(Alerts)]:::aws
    end

    %% Relationships - Monitoring Flow
    Scheduler -->|Triggers| Checker
    Checker -->|HTTP GET| TargetWeb
    Checker -->|Save Metrics| DB
    Checker -.->|If Error| SNS
    SNS -.->|Send Email| Email

    %% Relationships - Dashboard Flow
    User -->|Visits| S3
    User -->|Fetch Data via JS| API
    API -->|Invoke| Reader
    Reader -->|Query Last 24h| DB

---

## 🛠 Tech Stack

* **Cloud Provider:** Amazon Web Services (AWS)
* **Infrastructure:** Lambda, DynamoDB, API Gateway, EventBridge, SNS, S3
* **Backend Code:** Python 3.12 (Boto3, Urllib3)
* **Frontend:** HTML5, CSS3 (Glassmorphism UI), Chart.js
* **Version Control:** Git & GitHub

---

## 🚀 Features

* ✅ **Real-Time Monitoring:** Checks website health every 60 seconds.
* ✅ **Interactive Dashboard:** Visualizes latency trends over the last 10 minutes, 1 hour, or 24 hours.
* ✅ **Instant Alerts:** Sends an email notification immediately if the site goes down.
* ✅ **Data Persistence:** Stores historical performance data for analysis.
* ✅ **Cost Efficient:** Optimized to run within the AWS Free Tier.

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

## 📸 Screenshots

*(Add a screenshot of your dashboard here)*

---

## 🧠 What I Learned
* **Event-Driven Design:** How to decouple check logic (Lambda A) from data retrieval (Lambda B).
* **NoSQL Modeling:** Designing a DynamoDB schema for efficient time-series querying.
* **CORS & Security:** Configuring API Gateway to securely serve data to a static frontend.
* **Cost Optimization:** Leveraging AWS Free Tier limits for 24/7 monitoring without incurring costs.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

