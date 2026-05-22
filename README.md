# Agriculture FastAPI Assessment

FastAPI-based Agriculture Analytics API built for the Associate Data Scientist Assessment.

The project provides analytical endpoints for farm performance, crop efficiency, seasonal trends, market comparison, and quality analysis using agricultural datasets.

---

# Tech Stack

* FastAPI
* Python
* Pandas
* SQLAlchemy
* MySQL
* Docker

---

# Project Structure

```bash
AGRICULTURE-FASTAPI/
│
├── app/
│   ├── endpoints/
│   ├── services/
│   ├── schemas/
│   ├── utils/
│   ├── main.py
│   └── database.py
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── .env
```

---

# API Endpoints

## Farm Endpoints

### 1. Farm Summary

```http
GET /farms/summary
```

### 2. Single Farm Performance

```http
GET /farms/{farm_id}/performance
```

### 3. Top Farms

```http
GET /farms/top
```

### 4. Loss Analysis

```http
GET /farms/loss-analysis
```

---

## Crop Endpoints

### 5. Yield Efficiency

```http
GET /crops/yield-efficiency
```

### 6. Seasonal Revenue Trend

```http
GET /crops/seasonal-trend
```

### 7. Market Price Comparison

```http
GET /markets/price-comparison
```

### 8. Quality Grade Breakdown

```http
GET /crops/quality-breakdown
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
DB_HOST=your_host
DB_PORT=3306
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

Note:
Database credentials are intentionally excluded from GitHub for security reasons.

---

# How to Run Locally

## 1. Clone Repository

```bash
git clone https://github.com/Zubayer24/agriculture-fastapi.git
cd AGRICULTURE-FASTAPI
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv myenv
myenv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv myenv
source myenv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Docker Setup

## Pull Docker Image

```bash
docker pull zubayerhasan/agriculture-fastapi
```

---

## Run Docker Container

```bash
docker run -p 8000:8000 --env-file .env zubayerhasan/agriculture-fastapi
```

---

# DockerHub Repository

```text
https://hub.docker.com/r/zubayerhasan/agriculture-fastapi
```

---

# Features

* Centralized filtering utility
* Case-insensitive filtering
* FastAPI validation with HTTP 422 handling
* Aggregation using Pandas
* Dockerized deployment
* Structured schema-based responses
* Clean modular architecture

---

# Notes

* Invalid filters return HTTP 422 responses.
* Aggregations and metrics are computed using Pandas.
* The project uses pre-built database views for efficient querying.

---

# Author

Md. Zubayer Hasan
