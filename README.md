# MediPulse UK — Florence AI Health Assistant

NHS-aligned AI health chatbot powered by Google Gemini 2.0 Flash.

## 🚀 Deploy to Streamlit Cloud (Free HTTPS URL — 3 minutes)

### Step 1 — Upload to GitHub
1. Go to [github.com](https://github.com) → New repository → Name: `medipulse-uk`
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`

### Step 2 — Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your `medipulse-uk` repo → Branch: `main` → File: `app.py`
5. Click **"Deploy!"**
6. Your app will be live at: `https://YOUR-NAME-medipulse-uk-app-XXXXX.streamlit.app`

### Step 3 — Add Gemini API Key (Secure)
In Streamlit Cloud dashboard:
1. Go to your app → **Settings** → **Secrets**
2. Add:
```toml
GEMINI_API_KEY = "AIzaSy..."
```
3. The app will auto-read it securely

## 📋 Features
- 🏥 NHS 111 compliant symptom triage
- 💊 BNF medication information
- 🧠 Mental health signposting (IAPT, Samaritans, Mind)
- 🏥 GP registration guidance
- 📋 NICE clinical guidelines (NG136, NG28, CG90+)
- 🚨 Automatic emergency detection (999, Samaritans)
- 👤 Personalised user profile (name, age, gender, conditions)
- 🎨 Full NHS dark-mode design

## ⚠️ Disclaimer
For informational purposes only. Not medical advice. Not affiliated with NHS England.
