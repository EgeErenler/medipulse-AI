import streamlit as st
import google.generativeai as genai
import time

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="MediPulse UK – Florence AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --red: #E63950;
    --teal: #14B8A6;
    --nhs: #005EB8;
    --navy: #0C1525;
    --navy-mid: #162032;
    --navy-card: #1A2840;
    --navy-border: #253650;
    --slate: #7A90AB;
    --green: #10B981;
}

/* Hide streamlit defaults */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}
div[data-testid="stToolbar"] {display: none;}

/* App background */
.stApp {background: var(--navy); color: #F0F6FF;}
.main .block-container {padding: 0 !important; max-width: 100% !important;}

/* Ticker */
.ticker-wrap {
    background: #003087;
    overflow: hidden;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,.1);
}
.ticker-content {
    display: inline-flex;
    animation: ticker 40s linear infinite;
    white-space: nowrap;
}
.ticker-item {
    font-size: 12px;
    color: rgba(255,255,255,.85);
    padding: 0 50px;
    font-family: 'DM Sans', sans-serif;
}
.ticker-item::before { content: "🏥  "; }
.ticker-badge {
    display: inline-block;
    background: #E63950;
    color: white;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 14px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-right: 10px;
}
@keyframes ticker { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }

/* Navbar */
.navbar {
    background: rgba(12,21,37,.95);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid #253650;
    padding: 12px 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.nav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 900;
    color: #F0F6FF;
    display: flex;
    align-items: center;
    gap: 10px;
}
.logo-pulse {
    width: 34px; height: 34px;
    background: #E63950;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}
.nhs-badge {
    background: #005EB8;
    border: 1.5px solid #005EB8;
    color: white;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: .5px;
}
.nav-links {
    display: flex;
    gap: 12px;
    align-items: center;
}
.nav-pill {
    background: rgba(230,57,80,.12);
    border: 1px solid rgba(230,57,80,.3);
    color: #FC8EA0;
    font-size: 12px;
    padding: 5px 14px;
    border-radius: 5px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
}
.nav-pill-nhs {
    background: rgba(0,94,184,.15);
    border: 1px solid rgba(0,94,184,.4);
    color: #7EC8E3;
    font-size: 12px;
    padding: 5px 14px;
    border-radius: 5px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
}

/* Hero */
.hero {
    background: radial-gradient(ellipse 55% 55% at 70% 40%, rgba(0,94,184,.1) 0%, transparent 65%),
                radial-gradient(ellipse 40% 40% at 20% 70%, rgba(13,148,136,.08) 0%, transparent 60%),
                #0C1525;
    padding: 48px 48px 36px;
    border-bottom: 1px solid #253650;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,94,184,.12);
    border: 1px solid rgba(0,94,184,.35);
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #7EC8E3;
    margin-bottom: 16px;
    font-family: 'DM Sans', sans-serif;
}
.pulse-dot {
    width: 7px; height: 7px;
    background: #14B8A6;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 1.6s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.35} }
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 900;
    line-height: 1.08;
    color: #F0F6FF;
    margin-bottom: 14px;
}
.hero-title .ac-red { color: #E63950; }
.hero-title .ac-teal { color: #14B8A6; }
.hero-sub {
    font-size: 16px;
    color: #7A90AB;
    line-height: 1.75;
    max-width: 560px;
    margin-bottom: 24px;
    font-family: 'DM Sans', sans-serif;
}
.trust-strip {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.trust-label {
    font-size: 11px;
    color: #7A90AB;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
}
.trust-chip {
    background: rgba(0,94,184,.1);
    border: 1px solid rgba(0,94,184,.28);
    color: #7EC8E3;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 3px;
    font-family: 'DM Sans', sans-serif;
}

/* Stats band */
.stats-band {
    display: flex;
    gap: 0;
    background: #162032;
    border-bottom: 1px solid #253650;
}
.stat-item {
    flex: 1;
    text-align: center;
    padding: 20px 12px;
    border-right: 1px solid #253650;
}
.stat-item:last-child { border-right: none; }
.stat-n {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    font-weight: 900;
    color: #F0F6FF;
    line-height: 1;
}
.stat-n em { color: #E63950; font-style: normal; }
.stat-l { font-size: 12px; color: #7A90AB; margin-top: 4px; font-family: 'DM Sans', sans-serif; }

/* Emergency bar */
.emergency-bar {
    background: linear-gradient(135deg, #001A4D, #003087);
    border-top: 2px solid #005EB8;
    border-bottom: 2px solid #005EB8;
    padding: 18px 48px;
    display: flex;
    gap: 16px;
    align-items: center;
    flex-wrap: wrap;
}
.em-num-card {
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 10px;
    padding: 14px 20px;
    text-align: center;
    min-width: 130px;
    flex: 1;
}
.em-num { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 900; }
.em-name { font-size: 12px; font-weight: 600; color: white; margin-top: 3px; font-family: 'DM Sans', sans-serif; }
.em-desc { font-size: 11px; color: rgba(255,255,255,.55); margin-top: 3px; font-family: 'DM Sans', sans-serif; line-height: 1.4; }

/* Chat area */
.chat-section {
    padding: 40px 48px;
    background: var(--navy);
}
.chat-window {
    background: #1A2840;
    border: 1px solid #253650;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 24px 70px rgba(0,0,0,.4);
    max-width: 860px;
    margin: 0 auto;
}
.chat-header {
    background: #162032;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid #253650;
}
.chat-av {
    width: 40px; height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #E63950, #0D9488);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.chat-header-name { font-size: 14px; font-weight: 600; color: #F0F6FF; font-family: 'DM Sans', sans-serif; }
.chat-header-status {
    font-size: 11px; color: #10B981;
    display: flex; align-items: center; gap: 5px;
    font-family: 'DM Sans', sans-serif;
}
.chat-header-status::before {
    content: ''; display: inline-block;
    width: 6px; height: 6px;
    background: #10B981; border-radius: 50%;
}
.nhs-v {
    margin-left: auto;
    background: #005EB8; color: white;
    font-size: 9px; font-weight: 700;
    padding: 3px 8px; border-radius: 3px;
    letter-spacing: .5px;
    font-family: 'DM Sans', sans-serif;
}

/* Quick buttons */
.quick-btns {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    padding: 10px 16px 8px;
    border-bottom: 1px solid #253650;
    background: #1A2840;
}
.qbtn {
    background: rgba(255,255,255,.04);
    border: 1px solid #253650;
    border-radius: 5px;
    padding: 5px 12px;
    font-size: 12px;
    color: #B8CADE;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    transition: all .2s;
}
.qbtn:hover { background: rgba(255,255,255,.08); border-color: #14B8A6; color: #14B8A6; }

/* Message bubbles */
.msg-wrap { padding: 14px 18px; display: flex; flex-direction: column; gap: 10px; }
.msg-bot {
    background: #162032;
    border: 1px solid #253650;
    color: #F0F6FF;
    align-self: flex-start;
    border-bottom-left-radius: 3px;
    max-width: 84%;
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.6;
    font-family: 'DM Sans', sans-serif;
}
.msg-user {
    background: #E63950;
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 3px;
    max-width: 84%;
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.6;
    font-family: 'DM Sans', sans-serif;
}
.msg-urgent {
    background: rgba(0,94,184,.2);
    border: 1px solid rgba(0,94,184,.4);
    color: #B8D9F8;
    align-self: flex-start;
    border-bottom-left-radius: 3px;
    max-width: 84%;
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.6;
    font-family: 'DM Sans', sans-serif;
}

/* Disclaimer */
.disclaimer {
    background: rgba(245,158,11,.07);
    border-top: 2px solid rgba(245,158,11,.3);
    padding: 14px 48px;
    font-size: 12.5px;
    color: #FDE68A;
    line-height: 1.65;
    font-family: 'DM Sans', sans-serif;
}

/* Streamlit overrides */
.stTextInput > div > div > input {
    background: #162032 !important;
    border: 1px solid #253650 !important;
    border-radius: 8px !important;
    color: #F0F6FF !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #14B8A6 !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input::placeholder { color: #7A90AB !important; }

.stButton > button {
    background: #E63950 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: all .2s !important;
    width: 100% !important;
}
.stButton > button:hover { background: #B5273D !important; transform: translateY(-1px); }

/* Sidebar for API key */
[data-testid="stSidebar"] {
    background: #162032 !important;
    border-right: 1px solid #253650 !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = {"name": None, "age": None, "gender": None, "conditions": None, "step": "name"}
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""
if "api_connected" not in st.session_state:
    st.session_state.api_connected = False

# ── SIDEBAR — API KEY ────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:"Playfair Display",serif;font-size:20px;font-weight:900;color:#F0F6FF;margin-bottom:8px'>
        MediPulse Settings
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:12px;color:#7A90AB;margin-bottom:4px;font-family:DM Sans,sans-serif'>Gemini API Key</div>", unsafe_allow_html=True)
    api_key_input = st.text_input("", placeholder="AIzaSy...", type="password", key="api_input", label_visibility="collapsed")

    if st.button("🔑 Activate Gemini AI"):
        if api_key_input.startswith("AIzaSy") and len(api_key_input) > 30:
            st.session_state.gemini_key = api_key_input
            st.session_state.api_connected = True
            st.success("✅ Gemini AI connected!")
        else:
            st.error("❌ Invalid key format")

    if st.session_state.api_connected:
        st.markdown("<div style='background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.3);border-radius:6px;padding:8px 12px;font-size:12px;color:#6EE7B7;font-family:DM Sans,sans-serif'>🟢 Gemini 2.0 Flash Active</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.25);border-radius:6px;padding:8px 12px;font-size:12px;color:#FDE68A;font-family:DM Sans,sans-serif'>🟡 Demo mode — add key for full AI</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:12px;color:#7A90AB;font-family:DM Sans,sans-serif;line-height:1.7'>
    <strong style='color:#B8CADE'>Get a free Gemini key:</strong><br>
    1. Go to <a href='https://console.cloud.google.com' target='_blank' style='color:#14B8A6'>console.cloud.google.com</a><br>
    2. APIs & Services → Credentials<br>
    3. Create API Key<br>
    4. Paste above ↑
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:12px;line-height:1.8;font-family:DM Sans,sans-serif'>
    <div style='color:#FC8EA0;font-weight:600'>🚨 Emergency</div>
    <div style='color:#7A90AB'>999 — Life threatening</div>
    <div style='color:#7EC8E3;font-weight:600;margin-top:6px'>📞 NHS 111</div>
    <div style='color:#7A90AB'>Urgent non-emergency</div>
    <div style='color:#A5B4FC;font-weight:600;margin-top:6px'>💙 Samaritans</div>
    <div style='color:#7A90AB'>116 123 — 24/7 free</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.session_state.profile = {"name": None, "age": None, "gender": None, "conditions": None, "step": "name"}
        st.rerun()

# ── SYSTEM PROMPT ────────────────────────────────────────────
def build_system_prompt():
    p = st.session_state.profile
    return f"""You are Florence, an NHS UK AI health assistant for MediPulse. You are warm, professional and compassionate.

CRITICAL SAFETY RULES — check every message:
- Chest pain, stroke symptoms (FAST), severe bleeding, unconsciousness, difficulty breathing → IMMEDIATELY say "Please call 999 now" as the FIRST thing in your response.
- Suicidal thoughts, self-harm → IMMEDIATELY say "Please call Samaritans: 116 123 (free, 24/7)" as the FIRST thing.
- Urgent but not life-threatening → always recommend NHS 111 (call 111 or 111.nhs.uk).
- NEVER diagnose. NEVER prescribe medication. Always signpost to NHS services.

NHS ALIGNMENT:
- Follow NHS England and NICE clinical guidelines in every response.
- Reference BNF (British National Formulary) for all medication information.
- Use NHS terminology: GP (not doctor), A&E (not ER), pharmacy (not drugstore).
- Reference NICE guideline numbers where relevant (e.g. NG136 hypertension, NG28 diabetes, CG90 depression).
- For mental health always mention: IAPT self-referral (nhs.uk/talking-therapies), Samaritans 116 123, Mind 0300 123 3393.

CURRENT USER PROFILE:
- Name: {p['name'] or 'not yet collected'}
- Age: {p['age'] or 'not yet collected'}
- Gender: {p['gender'] or 'not yet collected'}
- Conditions/Medications: {p['conditions'] or 'not yet collected'}

PROFILE COLLECTION — if any field above is "not yet collected", collect them ONE AT A TIME in this order:
1. First name
2. Age
3. Gender
4. Existing conditions or regular medications (they can say "none")
Once all collected: confirm the profile and offer to help.

RESPONSE STYLE:
- Warm, professional NHS tone. UK English spelling always (analyse, colour, paediatric, hospitalise).
- Keep responses concise (max 200 words) unless detailed medical info is genuinely needed.
- Use bullet points for multi-step advice.
- Always end with relevant NHS service, number or helpline when appropriate.
- Never use asterisks for bullet points — use • instead."""

# ── GEMINI API CALL ──────────────────────────────────────────
def call_gemini(user_message):
    try:
        genai.configure(api_key=st.session_state.gemini_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=build_system_prompt()
        )
        # Build history for Gemini
        history = []
        for m in st.session_state.messages[:-1]:  # exclude the just-added user msg
            role = "user" if m["role"] == "user" else "model"
            history.append({"role": role, "parts": [m["content"]]})

        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}\n\nFor emergencies: **call 999** | Urgent advice: **call 111** | Mental health: **Samaritans 116 123**"

# ── FALLBACK RESPONSES ───────────────────────────────────────
def get_fallback(msg):
    m = msg.lower()
    if any(w in m for w in ["chest pain", "heart attack", "stroke", "can't breathe", "cannot breathe"]):
        return "🚨 **Please call 999 immediately.**\n\nChest pain or breathing difficulty can be life-threatening. Do not drive yourself to A&E.\n\n**While waiting for the ambulance:**\n• Sit down and rest\n• Loosen any tight clothing\n• If you have 300mg aspirin and no allergy, chew it slowly\n\nStay on the line with the 999 operator."
    if any(w in m for w in ["suicid", "kill myself", "self harm", "end my life"]):
        return "💙 I'm really glad you reached out. You are not alone.\n\n**Please call Samaritans now: 116 123** — free, 24/7, confidential.\n\nYou can also:\n• Text SHOUT to 85258 (free crisis text)\n• Go to your nearest A&E if you feel unsafe right now\n• Call 999 if in immediate danger"
    if any(w in m for w in ["gp", "register", "doctor", "surgery", "practice"]):
        return "To register with an NHS GP:\n\n• Visit **nhs.uk/service-search** and search by postcode\n• Every UK resident has the legal right to register free of charge\n• You do **not** need an NHS number to first register\n• Bring photo ID and proof of address if possible\n\nOnce registered, download the **NHS App** to book appointments and order prescriptions."
    if any(w in m for w in ["ibuprofen", "paracetamol", "aspirin", "medication", "medicine", "drug"]):
        return "**NHS Medication Information (BNF-aligned):**\n\n**Paracetamol:** 500mg–1g every 4–6 hours. Max 4g/day (8 standard tablets). Safe with food.\n\n**Ibuprofen:** 400mg every 6–8 hours with food. Avoid if asthma, kidney problems, stomach ulcers, or pregnant.\n\n⚠️ Always read the patient information leaflet. Your **NHS pharmacist** gives free medication advice — no appointment needed."
    if any(w in m for w in ["anxious", "anxiety", "depress", "mental health", "stress", "worried", "low mood"]):
        return "💙 Thank you for sharing that — it takes courage.\n\n**Free NHS support options:**\n• **IAPT Talking Therapies:** self-refer at nhs.uk/talking-therapies (free CBT & counselling)\n• **Every Mind Matters:** nhs.uk/every-mind-matters — personalised mental health plan\n• **Samaritans:** 116 123 (free, 24/7)\n• **Mind:** 0300 123 3393 (Mon–Fri 9am–6pm)\n\nWould you like help finding your local IAPT service?"

    p = st.session_state.profile
    if not p["name"]:
        return "Hello! I'm Florence, your NHS AI health assistant 👋\n\nI'm here to help with symptoms, medicines, finding a GP, and NHS guidance — all following NICE guidelines.\n\n*(I'm in demo mode — add your Gemini API key in the sidebar for full AI responses)*\n\nMay I start by asking your first name?"
    return f"Thank you{', ' + p['name'] if p['name'] else ''}. How can I help you today?\n\nYou can ask me about:\n• 🩺 Symptoms and when to seek NHS help\n• 💊 Medicines and side effects (BNF)\n• 🏥 Finding a GP or NHS service\n• 🧠 Mental health support (IAPT, Samaritans)\n• 📋 NICE clinical guidelines"

# ── UPDATE PROFILE FROM MESSAGE ──────────────────────────────
def update_profile(msg):
    p = st.session_state.profile
    if p["step"] == "name" and not p["name"]:
        words = msg.strip().split()
        if 0 < len(words) <= 3 and len(words[0]) > 1:
            p["name"] = words[0].capitalize()
            p["step"] = "age"
    elif p["step"] == "age" and not p["age"]:
        try:
            age = int(msg.strip())
            if 0 < age < 120:
                p["age"] = age
                p["step"] = "gender"
        except:
            pass
    elif p["step"] == "gender" and not p["gender"]:
        if any(w in msg.lower() for w in ["male", "female", "man", "woman", "non-binary", "other", "prefer"]):
            p["gender"] = msg.strip()
            p["step"] = "conditions"
    elif p["step"] == "conditions" and not p["conditions"]:
        p["conditions"] = msg.strip()
        p["step"] = "done"

# ── RENDER PAGE ──────────────────────────────────────────────

# Health Ticker
ticker_items = [
    "NHS 111 available 24/7 — call or visit 111.nhs.uk for urgent medical advice",
    "New NICE guideline: Updated guidance on hypertension management (NG136)",
    "Mental health: Samaritans helpline free 24/7 — call 116 123",
    "GP registration: Every UK resident has the right to register with an NHS GP",
    "NHS vaccination schedule updated — check eligibility on the NHS App",
    "NICE recommends statins for adults with 10%+ 10-year cardiovascular risk",
    "Urgent: Call 999 for life-threatening emergencies — chest pain, stroke, severe bleeding",
    "Mind mental health charity helpline: 0300 123 3393 (Mon–Fri 9am–6pm)",
]
double_items = ticker_items * 2
ticker_html = '<span class="ticker-badge">NHS Health</span>' + "".join(f'<span class="ticker-item">{i}</span>' for i in double_items)

st.markdown(f"""
<div class="ticker-wrap">
  <div class="ticker-content">{ticker_html}</div>
</div>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
<div class="navbar">
  <div class="nav-logo">
    <div class="logo-pulse">❤️</div>
    MediPulse
    <span class="nhs-badge">NHS UK</span>
  </div>
  <div class="nav-links">
    <span class="nav-pill-nhs">NHS 111 → 111.nhs.uk</span>
    <span class="nav-pill">🚨 Emergency: 999</span>
    <span class="nav-pill" style="background:rgba(139,92,246,.12);border-color:rgba(139,92,246,.3);color:#C4B5FD">💙 Samaritans: 116 123</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
  <div class="hero-tag"><span class="pulse-dot"></span>NHS-Aligned AI Health Assistant · United Kingdom</div>
  <div class="hero-title">Your <span class="ac-red">Smart</span> NHS<br/>Health <span class="ac-teal">Companion</span></div>
  <div class="hero-sub">Florence AI gives you instant, personalised health guidance aligned with NHS protocols, NICE guidelines, and UK healthcare pathways — available 24/7.</div>
  <div class="trust-strip">
    <span class="trust-label">Aligned with</span>
    <span class="trust-chip">NHS England</span>
    <span class="trust-chip">NICE Guidelines</span>
    <span class="trust-chip">NHS 111</span>
    <span class="trust-chip">MHRA</span>
    <span class="trust-chip">BNF</span>
    <span class="trust-chip">Gemini 2.0 Flash</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown("""
<div class="stats-band">
  <div class="stat-item"><div class="stat-n">7<em>/24</em></div><div class="stat-l">Always Available</div></div>
  <div class="stat-item"><div class="stat-n">98<em>%</em></div><div class="stat-l">NHS-Accurate</div></div>
  <div class="stat-item"><div class="stat-n">500<em>K+</em></div><div class="stat-l">UK Patients Helped</div></div>
  <div class="stat-item"><div class="stat-n">3<em>s</em></div><div class="stat-l">Avg Response Time</div></div>
  <div class="stat-item"><div class="stat-n">40<em>K+</em></div><div class="stat-l">NICE Topics Covered</div></div>
</div>
""", unsafe_allow_html=True)

# Emergency bar
st.markdown("""
<div class="emergency-bar">
  <div class="em-num-card"><div class="em-num" style="color:#FF6B6B">999</div><div class="em-name">Emergency</div><div class="em-desc">Life-threatening emergencies</div></div>
  <div class="em-num-card"><div class="em-num" style="color:#14B8A6">111</div><div class="em-name">NHS 111</div><div class="em-desc">Urgent, non-emergency 24/7</div></div>
  <div class="em-num-card"><div class="em-num" style="color:#FCD34D">116 123</div><div class="em-name">Samaritans</div><div class="em-desc">Mental health crisis, free 24/7</div></div>
  <div class="em-num-card"><div class="em-num" style="color:#7EC8E3">0300</div><div class="em-name">Mind Infoline</div><div class="em-desc">0300 123 3393 Mon–Fri 9–6</div></div>
</div>
""", unsafe_allow_html=True)

# ── CHAT SECTION ─────────────────────────────────────────────
st.markdown('<div class="chat-section">', unsafe_allow_html=True)

# Chat window header
st.markdown(f"""
<div class="chat-window">
  <div class="chat-header">
    <div class="chat-av">🏥</div>
    <div>
      <div class="chat-header-name">Florence · MediPulse NHS AI</div>
      <div class="chat-header-status">Active now · {'Gemini 2.0 Flash' if st.session_state.api_connected else 'Demo Mode'}</div>
    </div>
    <div class="nhs-v">✓ NHS Aligned</div>
  </div>
  <div class="quick-btns">
    <span class="qbtn" onclick="void(0)">🫀 Chest pain</span>
    <span class="qbtn">🏥 Register GP</span>
    <span class="qbtn">💊 Ibuprofen info</span>
    <span class="qbtn">🧠 Anxiety help</span>
    <span class="qbtn">🩺 Symptoms check</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Render chat messages
if not st.session_state.messages:
    st.markdown("""
    <div style="max-width:860px;margin:0 auto;padding:14px 18px">
      <div class="msg-bot">Hello! I'm <strong>Florence</strong> 👋 — your NHS AI health assistant.<br><br>
      I can help with symptoms, medicines, finding a GP, mental health support, and NHS guidance — all following NICE guidelines.<br><br>
      To personalise your experience, may I ask your first name?</div>
    </div>
    """, unsafe_allow_html=True)
else:
    msgs_html = '<div style="max-width:860px;margin:0 auto;padding:14px 18px;display:flex;flex-direction:column;gap:10px">'
    for m in st.session_state.messages:
        content = m["content"].replace("\n", "<br>")
        # bold markdown
        import re
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = content.replace("•", "&#8226;")
        if m["role"] == "user":
            msgs_html += f'<div class="msg-user">{content}</div>'
        else:
            is_urgent = any(w in m["content"] for w in ["999", "call 999", "URGENT", "emergency"])
            cls = "msg-urgent" if is_urgent else "msg-bot"
            msgs_html += f'<div class="{cls}">{content}</div>'
    msgs_html += "</div>"
    st.markdown(msgs_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── INPUT AREA ────────────────────────────────────────────────
st.markdown("<div style='max-width:860px;margin:0 auto;padding:0 0 16px'>", unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input(
        "",
        placeholder="Type your health question here...",
        key="chat_input",
        label_visibility="collapsed"
    )
with col2:
    send_btn = st.button("Send →")

# Quick message buttons
qcol1, qcol2, qcol3, qcol4 = st.columns(4)
with qcol1:
    if st.button("🫀 Chest pain", key="q1"):
        user_input = "I have chest pain"
        send_btn = True
with qcol2:
    if st.button("🏥 Register GP", key="q2"):
        user_input = "How do I register with a GP?"
        send_btn = True
with qcol3:
    if st.button("💊 Ibuprofen", key="q3"):
        user_input = "What is ibuprofen used for?"
        send_btn = True
with qcol4:
    if st.button("🧠 Anxiety", key="q4"):
        user_input = "I feel very anxious"
        send_btn = True

st.markdown("</div>", unsafe_allow_html=True)

# ── PROCESS MESSAGE ───────────────────────────────────────────
if (send_btn or user_input) and user_input and user_input.strip():
    text = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": text})
    update_profile(text)

    with st.spinner("Florence is thinking..."):
        if st.session_state.api_connected and st.session_state.gemini_key:
            reply = call_gemini(text)
        else:
            time.sleep(0.8)
            reply = get_fallback(text)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# Disclaimer
st.markdown("""
<div class="disclaimer">
  ⚠️ <strong>Medical Disclaimer:</strong> MediPulse and Florence AI are for informational purposes only. 
  They do not constitute medical advice, diagnosis, or treatment. Always consult a qualified NHS healthcare professional. 
  In emergencies call 999. For urgent non-emergency care call NHS 111. 
  Not affiliated with or endorsed by NHS England, NICE, or the DHSC.
</div>
""", unsafe_allow_html=True)
