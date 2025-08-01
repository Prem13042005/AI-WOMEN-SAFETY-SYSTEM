# 🔐 AI-Based Women Safety & Emergency Response System 🚨

A smart, AI-powered emergency response system designed to protect and empower women through real-time location tracking, SOS triggers, WhatsApp alerts, and predictive risk detection using machine learning.

> 🛡️ Developed as a third-year CSE mini-project with real-world scalability, patentability focus, and societal impact goals.

---

## 📌 Key Features

- 🔴 **SOS Trigger** (Button + Voice Activated)
- 📍 **Live Location Tracking** (HTML5 Geolocation API)
- 📊 **AI-Based Danger Prediction** (with ML model `danger_predictor.pkl`)
- 🧠 **ML Model** trained on location, time, urban type, and crime data
- 📤 **WhatsApp Alerts via Twilio** to emergency contacts
- 👩‍💻 **User Authentication & Profile Management**
- 📁 **Contact Registration** for emergency alerting
- 📡 **Modular Flask Backend** + Vanilla JS Frontend + Lottie UI

---

## ⚙️ Tech Stack

| Layer         | Tech Used                              |
|---------------|-----------------------------------------|
| **Frontend**  | HTML, CSS, JavaScript, Lottie           |
| **Backend**   | Flask (Python), Blueprints              |
| **Database**  | MySQL                                   |
| **ML Model**  | Scikit-learn, joblib                    |
| **Location APIs** | HTML5 Geolocation, Custom Location Context |
| **Notifications** | Twilio WhatsApp API                 |
| **Voice Input** | Web Speech API                        |
| **Hosting (optional)** | Render / Railway (Flask Support) |

---

## 📁 Folder Structure

```bash
ai_women_safety_project/
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── templates/ (optional if using frontend/)
│   └── static/ (optional if using frontend/)
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── contact.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── models/
│   ├── danger_predictor.pkl
│   └── scaler.pkl
│
├── database/
│   ├── schema.sql
│   └── seed_data.sql
│
├── iot_prototype/
│   ├── code.ino
│   └── wiring_diagram.png
│
├── docs/
│   ├── pitch_deck.pptx
│   ├── architecture.png
│   └── user_manual.pdf
│
├── requirements.txt
└── README.md
