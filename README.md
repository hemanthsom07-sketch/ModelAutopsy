<div align="center">

# 🧠 ModelAutopsy

![ModelAutopsy Home](frontend/src/assets/screenshots/home.png)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikitlearn)
![License](https://img.shields.io/badge/License-MIT-green)

An AI-powered machine learning platform for dataset analysis, model training, prediction, and explainable AI through an interactive React dashboard.

</div>

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

An end-to-end Machine Learning Analysis and Prediction Platform built with **FastAPI**, **React**, **TypeScript**, and **Scikit-learn**.

ModelAutopsy enables users to upload datasets, analyze data quality, train machine learning models, generate predictions, and understand model performance through interactive visualizations—all from a modern web interface.

---

## ✨ Features

- 📂 Upload CSV datasets
- 📊 Automatic dataset analysis
- 🧹 Missing value detection
- 📈 Statistical summaries
- 🔥 Correlation heatmap
- 📉 Distribution visualizations
- 🤖 Machine learning model training
- 🎯 Predictions on new data
- 📋 Model evaluation metrics
- 🌟 Feature importance visualization
- ⚡ FastAPI backend with React frontend

---

## 🛠️ Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- Recharts

### Backend
- FastAPI
- Uvicorn

### Machine Learning
- Scikit-learn
- Pandas
- NumPy

### Data Visualization
- Matplotlib
- Seaborn

### Development Tools
- Python
- Git & GitHub
- VS Code

---
## 🔄 Project Workflow

```text
Dataset (CSV)
      │
      ▼
Data Preprocessing
      │
      ▼
Exploratory Data Analysis
      │
      ▼
Feature Engineering
      │
      ▼
Model Training & Evaluation
      │
      ▼
Predictions & Explainability
      │
      ▼
Interactive React Dashboard
```

## 📂 Project Structure

```text
ModelAutopsy/
├── backend/              # FastAPI backend
├── frontend/             # React + TypeScript frontend
├── src/                  # Machine Learning engine
├── data/                 # Sample datasets
├── reports/              # Generated analysis reports
├── .gitignore
├── main.py
└── README.md
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/hemanthsom07-sketch/ModelAutopsy.git
cd ModelAutopsy
```

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The application will be available at:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

---

# 📸 Application Screenshots

## 🏠 Home Page

![Home Page](frontend/src/assets/screenshots/home.png)

---

## 📂 Upload Dataset

![Upload Dataset](frontend/src/assets/screenshots/upload.png)

---

## 📊 Dataset Analysis

![Dataset Analysis](frontend/src/assets/screenshots/analysis.png)

---

## 🔥 Correlation Heatmap

![Correlation Heatmap](frontend/src/assets/screenshots/correlation_heatmap.png)

---

## 📈 Distribution Analysis

![Distribution Analysis](frontend/src/assets/screenshots/distribution.png)

---

## 🎯 Prediction Results

![Prediction Results](frontend/src/assets/screenshots/prediction.png)

---

## 🧠 Model Autopsy

![Model Autopsy](frontend/src/assets/screenshots/model_autopsy.png)

## 🌐 Live Demo

- **Frontend:** https://model-autopsy.vercel.app
- **Backend API:** https://modelautopsy.onrender.com
- **API Documentation (Swagger):** https://modelautopsy.onrender.com/docs

## 🚀 Future Improvements

- Deploy the application for public access.
- Support additional machine learning algorithms.
- Add user authentication and project history.
- Enable dataset versioning and experiment tracking.
- Integrate advanced explainable AI techniques such as SHAP and LIME.
- Support deep learning models using TensorFlow and PyTorch.

## 👨‍💻 Author

**Hemanth R.S**

- GitHub: https://github.com/hemanthsom07-sketch
- LinkedIn: *(Add your LinkedIn profile URL here when you have one.)*

If you found this project helpful, consider giving it a ⭐ on GitHub!