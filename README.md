# 🍔 FastBite
![Python](https://img.shields.io/badge/Python-3.7%2B-blue) 
![Flask](https://img.shields.io/badge/Flask-1.1.2-orange) 
![License](https://img.shields.io/badge/License-MIT-green)
![Frontend - Siddarth](https://img.shields.io/badge/Frontend-Siddarth-blueviolet?style=for-the-badge&logo=github)
![Backend - Rishi](https://img.shields.io/badge/Backend-Rishi-green?style=for-the-badge&logo=github)
![Data - Koushik](https://img.shields.io/badge/Data-Koushik-orange?style=for-the-badge&logo=github)
![ML - Siddarth & Rishi](https://img.shields.io/badge/ML-Siddarth%20%26%20Rishi-red?style=for-the-badge&logo=python)



FastBite is a full-stack web application designed to solve the problem of long queues and inefficient service at the VIT Bhopal canteens.  
This prototype demonstrates a complete user flow — from **secure user authentication** to a **dynamic ordering system**, all powered by a **Python backend** and a **predictive machine learning model** for wait-time estimation.

---

## 📋 Table of Contents
- [🎯 The Problem](#-the-problem)
- [✨ Key Features](#-key-features)
- [🚀 Getting Started: Running The Project Locally](#-getting-started-running-the-project-locally)
- [🛠️ Built With](#️-built-with)
- [👨‍💻 The Team](#-the-team)

---

## 🎯 The Problem
Students at our college often waste **40–50 minutes per meal** due to:
- Long ordering queues  
- Inefficient processing  
- Uncertain wait times  

This leads to severe overcrowding and frustration, especially during peak hours.  
**FastBite tackles this problem head-on by digitizing the canteen ordering experience.**

---

## ✨ Key Features
- 🔐 **Secure User Authentication**: Login & registration system with **Flask-Bcrypt** (hashed passwords) and **JWT-based session management**.  
- 🛒 **Dynamic Food Menu & Interactive Cart**: Single-page, responsive UI where users can browse, add items to cart, and place orders.  
- ⏱️ **AI-Powered Wait-Time Prediction**: Machine learning model (**Scikit-learn RandomForestRegressor**) predicts ETA based on order size and traffic.  
- 🔗 **Full-Stack Integration**: Frontend (**HTML + Tailwind CSS + JS**) connected with **Flask backend**.  
- 💾 **Persistent Database**: User accounts & order history stored in **SQLite**.  

---

## 🚀 Getting Started: Running The Project Locally

### 1️⃣ Prerequisites
- Install **Python 3.7+**  
Check version:
```bash
python3 --version
```
[Download Python](https://www.python.org/downloads/) (check "Add Python to PATH" on Windows).  

---

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/monkeyDluffy06/FastBite-.git
cd FastBite-
```

---

### 3️⃣ Set Up Virtual Environment
```bash
python3 -m venv venv
```

Activate it:  
- macOS/Linux:
```bash
source venv/bin/activate
```
- Windows:
```bash
.\venv\Scripts\activate
```

---

### 4️⃣ Install Dependencies
```bash
pip install Flask Flask-SQLAlchemy Flask-Bcrypt Flask-Cors PyJWT pandas joblib scikit-learn
```

---

### 5️⃣ Run the Application
```bash
python3 app.py
```
Server will run at: **http://127.0.0.1:5000**

---

### 6️⃣ Access the App
Open your browser and go to:  
👉 **http://localhost:5000**  
You’ll see the FastBite **login page**.

---

## 🛠️ Built With

### 🔹 Frontend
- **HTML5** – Page structure  
- **Tailwind CSS** – Responsive styling  
- **JavaScript** – Client-side interactivity, API calls, dynamic cart  

### 🔹 Backend & Machine Learning
- **Python + Flask** – Core server & API endpoints  
- **SQLite + SQLAlchemy** – Persistent storage  
- **Flask-Bcrypt + JWT** – Authentication & password security  
- **Pandas + Scikit-learn + Joblib** – Data preprocessing, ML training & wait-time prediction  

---

## 👨‍💻 The Team
Team 07 – VIT Bhopal

- **T. Siddarth Bharadwaj** – [GitHub Profile](https://github.com/monkeyDluffy06)  
- **Godala Koushik Reddy** – [GitHub Profile](https://github.com/koushikreddy8635)  
- **Rishi Kumar Singh** – [GitHub Profile](https://github.com/rishi-zen)  
- **Anushka Kamariya**    
- **Kushi Gupta**   

---

🚀 *FastBite – Making campus dining faster, smarter, and stress-free.*  
