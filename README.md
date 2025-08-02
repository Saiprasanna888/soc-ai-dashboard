# 🚨 SOC AI Agent Dashboard

This project is a real-time AI-powered **Security Operations Center (SOC) Dashboard**, built to help security analysts monitor, triage, and respond to incidents efficiently.
It combines **Machine Learning** for automated alert triage with an interactive **Streamlit dashboard** for visualization.

---

## 📌 Project Overview

🔐 In modern SOCs, analysts are flooded with alerts, and many turn out to be false positives.
To solve this, I built an **AI-driven SOC Analyst Assistant** that:

* 📥 **Ingests security incident logs**
* 🧠 **Predicts alert severity** using a trained ML model
* 📊 **Visualizes alerts** on a real-time dashboard
* 🔄 **Auto-refreshes** so analysts always see the latest data
* 📁 **Logs Incident Response notes** for documentation

This project showcases **defensive security skills** and demonstrates my ability to design SOC tools.

---

## ✨ Features

* 🧠 **ML-Powered Alert Triage**

  * Built with a `DecisionTreeClassifier`
  * Classifies alerts into *High Priority* vs *Normal*

* 📈 **Real-Time Dashboard**

  * Developed using **Streamlit**
  * Auto-refreshes every 60 seconds

* 📊 **Interactive Visualizations**

  * Plotly charts show trends in incident priority & urgency

* 📝 **Incident Response Notes**

  * Analysts can log their findings (see `docs/Incident_response.txt`)

* 🔍 **Future-Ready Design**

  * Can be extended with live SIEM feeds or APIs

---

## 📁 Project Structure

```plaintext
soc-ai-dashboard/
│
├── data/
│   └── incident_event_log.csv       # Security incident dataset
│
├── models/
│   └── triage_model.joblib          # Trained ML model
│
├── scripts/
│   ├── soc_dashboard.py             # Streamlit Dashboard
│   ├── ml_triage.py                 # ML model training & triage logic
│   └── real_time_agent.py           # Real-time alert simulation
│
├── docs/
│   ├── Incident_response.txt        # SOC Incident Response notes
│   └── screenshot.png               # Dashboard Screenshot
│
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## ⚙️ Installation & Setup

1️⃣ **Clone the Repository**

```bash
git clone https://github.com/Saiprasanna888/soc-ai-dashboard.git
cd soc-ai-dashboard
```

2️⃣ **Create a Virtual Environment (Recommended)**

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Linux/Mac
```

3️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

4️⃣ **Run the Dashboard**

```bash
streamlit run scripts/soc_dashboard.py
```

---

## 🧠 Machine Learning Model

* **Algorithm:** DecisionTreeClassifier
* **Training Data:** `incident_event_log.csv`
* **Features:** Priority, Urgency, and other log fields
* **Output Label:**

  * `0 = Normal Alert`
  * `1 = High Priority Alert`

This allows the dashboard to **highlight critical alerts instantly**.

---

## 📸 Dashboard Preview

![Dashboard Screenshot](https://github.com/Saiprasanna888/soc-ai-dashboard/blob/e7e88ac21c8f323d0e90501a5b8956264da1fdaa/ScreenShots/alerts_dashboard.png)

> The dashboard updates automatically and displays high-priority alerts with clear visuals.

---

## 👨‍💻 Author

**Saiprasanna Muppalla**

* Security Analyst | SOC Enthusiast | Blue Team Learner
* [LinkedIn](https://linkedin.com/in/YOUR-LINKEDIN)
* [GitHub](https://github.com/Saiprasanna888)

---

## 🛡️ License

This project is open-source and available under the **MIT License**.
