# 🩺 DermaLens AI

An AI-powered skin analysis application that detects common skin conditions from facial images and generates personalized skincare recommendations with a professional clinical-style report.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 📷 Upload a facial skin image
- 🤖 AI-based skin condition detection
- 📊 Skin health assessment
- 🧴 Personalized skincare routine
- 🌞 Morning & 🌙 Night skincare regimen
- 💊 Ingredient recommendations
- 🚫 Ingredients to avoid
- 📄 Downloadable PDF skin report
- 📜 Scan history tracking
- 👤 User authentication
- 🎨 Clean and responsive Streamlit interface

---

## 🧠 Supported Skin Conditions

- ✅ Healthy Skin
- 🔴 Acne
- 🌑 Pigmentation
- 👵 Wrinkles

---

## 🏗️ Tech Stack

**Frontend**
- Streamlit
- HTML/CSS

**Backend**
- Python

**Machine Learning**
- TensorFlow / Keras
- OpenCV
- NumPy
- Pillow

**Utilities**
- ReportLab (PDF Generation)

---

## 📂 Project Structure

```text
DermaLens-AI
│
├── app.py
├── assets/
├── ml/
│   ├── model_loader.py
│   ├── predict.py
│   ├── preprocess.py
│   └── __init__.py
├── pages/
├── utils/
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/xravanii/DermaLens-AI.git
cd DermaLens-AI
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 📋 Workflow

```text
Upload Image
      │
      ▼
Image Preprocessing
      │
      ▼
Deep Learning Model
      │
      ▼
Skin Condition Detection
      │
      ▼
Questionnaire Personalization
      │
      ▼
Clinical AI Report
      │
      ▼
PDF Generation + History
```

---

## 📸 Screenshots

> Add screenshots here

- Welcome Screen
- Upload Screen
- Questionnaire
- AI Analysis
- Clinical Report
- History Page

---

## 🔮 Future Improvements

- More skin conditions
- Explainable AI (Grad-CAM)
- Severity estimation
- Progress tracking
- Cloud deployment
- Mobile application

---

## ⚠️ Disclaimer

DermaLens AI is intended for educational and research purposes only. It is **not** a substitute for professional medical advice or diagnosis.

---

## 👩‍💻 Author

**Sravani**

Computer Science Engineering Student

GitHub: https://github.com/xravanii

---

⭐ If you found this project useful, consider starring the repository!
