<div align="center">

# ⚡️ Nexus Monitor: Serverless Website Health Tracker

![Status](https://img.shields.io/badge/status-active-success.svg)
![AWS](https://img.shields.io/badge/AWS-Lambda%20|%20DynamoDB%20|%20S3%20|%20API%20Gateway%20|%20SNS-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A fully **serverless, event-driven website monitoring solution** that tracks uptime and latency in real-time. Built entirely on AWS Cloud services, Nexus Monitor features a modern glassmorphism dashboard, automated alerts, and minute-by-minute data visualization.

[🌐 Live Demo](http://my-health-dashboard-123.s3-website-us-east-1.amazonaws.com/)

</div>

---

## 🏗 Architecture Overview

Nexus Monitor leverages a **serverless architecture** to achieve high availability, minimal cost, and zero server maintenance.

![Architecture Diagram](https://my-health-dashboard-123.s3.us-east-1.amazonaws.com/screenshots/nexus-architecture.jpg)

**Workflow:**
1. **EventBridge Scheduler** triggers the health check Lambda every minute.  
2. **Lambda (Checker):** Pings target URLs, measures latency, and checks HTTP status codes.  
3. **DynamoDB:** Stores time-series data (Timestamp, Latency, Status) with TTL for auto-cleanup.  
4. **SNS:** Sends instant email alerts if a website returns a non-200 status.  
5. **Lambda (Reader):** Retrieves historical data from DynamoDB and formats it for the frontend.  
6. **API Gateway:** Exposes the Reader Lambda via a secure REST API.  
7. **S3 + CloudFront:** Hosts the responsive static dashboard globally.  

---

## 📊 Dashboard & Features

### 1. Real-Time Monitoring
* Responsive **glassmorphism UI** with vanilla HTML/CSS and Chart.js.  
* Toggle between **10-minute, 1-hour, and 24-hour latency views**.  

![Operational Dashboard](https://my-health-dashboard-123.s3.us-east-1.amazonaws.com/screenshots/Screenshot+2025-12-03+at+15.41.15.png)

### 2. Incident Response
* Event-driven architecture updates the UI instantly if a site is down.  
* **SNS notifications** trigger automated email alerts.  

**Critical State Dashboard:**  
![Critical Dashboard](https://my-health-dashboard-123.s3.us-east-1.amazonaws.com/screenshots/Screenshot+2025-12-03+at+15.28.15.png)

**Example Email Alert:**  
![Email Alert](https://my-health-dashboard-123.s3.us-east-1.amazonaws.com/screenshots/Screenshot+2025-12-03+at+16.02.08.png)

---

## 🛠 Tech Stack

* **Cloud:** AWS (Lambda, DynamoDB, S3, API Gateway, EventBridge, SNS)  
* **Backend:** Python 3.12 (Boto3, Urllib3)  
* **Frontend:** HTML5, CSS3 (Glassmorphism), Chart.js  
* **Version Control:** Git & GitHub  

---

## 💻 Deployment Guide

### Backend Setup
1. **DynamoDB Table:** `WebsiteHealth`  
   * Partition Key: `UrlID` (String)  
   * Sort Key: `Timestamp` (String)  
2. **SNS Topic:** `WebsiteDownAlerts` – subscribe your email.  
3. **IAM Role:** Permissions for `DynamoDBFullAccess` & `AmazonSNSFullAccess`.  

### Lambda Functions
* **Checker (`backend/checker.py`):**  
  - Set target URL and SNS ARN via environment variables.  
  - Trigger every **1 minute** using EventBridge Scheduler.  

* **Reader (`backend/reader.py`):**  
  - Fetches data from DynamoDB and exposes via **API Gateway (GET route)**.  
  - Enable **CORS** for frontend access.  

### Frontend Deployment
1. Replace placeholder API URL in `index.html`:
```javascript
const API_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com";
