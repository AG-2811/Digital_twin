import streamlit as st
import numpy as np
import joblib
import tensorflow as tf
import pandas as pd
import os, json
import time
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import base64

def show_meditation_mode():
    st.markdown("""
        <style>
        /* Hide the main streamlit scrollbar */
        .main {
            overflow: hidden !important;
        }
        div[data-testid="stButton"] {
            position: fixed !important;
            top: 70px !important;
            right: 140px !important;
            z-index: 100000 !important;
            width: auto !important;
        }

        div[data-testid="stButton"] > button {
            background-color: rgba(0, 0, 0, 0.5) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            backdrop-filter: blur(5px);
        }
        
        iframe {
            position: fixed !important;
            top: 0 !important;
            left: 10% !important;
            width: 80vw !important;
            height: 100vh !important;
            z-index: 1 !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    if st.button("✖ Exit"):
        st.session_state["active_zen"] = False
        st.rerun()
    st.components.v1.html("""
    <style>
    body { margin: 0; overflow: hidden; }
    
    .zen-container {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.9)),
                    url('https://i.pinimg.com/originals/15/64/c0/1564c0f85bbff284d20c1fb0a542bdbe.gif');
        background-size: cover;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(10px);
        color: white;
        font-family: sans-serif;
        text-align: center;
    }

    /* 🫁 BREATHING CIRCLE */
    .breathing-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: radial-gradient(circle, #00ffcc, #004d40);
        animation: breathe 8s infinite ease-in-out;
        margin-bottom: 25px;
        box-shadow: 0 0 40px #00ffcc;
    }

    @keyframes breathe {
        0%, 100% { transform: scale(0.8); opacity: 0.6; }
        50% { transform: scale(1.2); opacity: 1; }
    }

    /* 🌿 TEXT */
    .text {
        font-size: 38px;
        letter-spacing: 2px;
        margin-top: 10px;
        animation: glow 3s infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #00ffcc; }
        to { text-shadow: 0 0 30px #00ffcc; }
    }

    .subtext {
        font-size: 16px;
        margin-top: 8px;
        opacity: 0.7;
    }

    /* ⏳ PROGRESS BAR */
    .progress-bar {
        width: 260px;
        height: 6px;
        background: rgba(255,255,255,0.2);
        margin-top: 25px;
        border-radius: 10px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        width: 0%;
        background: #00ffcc;
        animation: progressAnim 60s linear forwards;
    }

    @keyframes progressAnim {
        from { width: 0%; }
        to { width: 100%; }
    }

    </style>

    <div class="zen-container">


        <!-- 🫁 BREATH UI -->
        <div class="breathing-circle"></div>
        <div class="text" id="breathText">Breathe In</div>
        <div class="subtext">Calm your mind. Reset your focus.</div>

        <!-- ⏳ PROGRESS -->
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>

        <!-- 🎧 AUDIO -->
        <audio autoplay loop>
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3" type="audio/mp3">
        </audio>
    </div>

    <script>
    // 🫁 BREATHING CYCLE
    const text = document.getElementById("breathText");
    const sequence = ["Breathe In", "Hold", "Breathe Out"];
    let index = 0;

    setInterval(() => {
        index = (index + 1) % sequence.length;
        text.innerText = sequence[index];
    }, 3000);

    </script>
    """, height=700,scrolling=False)
        
st.set_page_config(page_title="Digital_Twin", layout="wide")
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
if "username" not in st.session_state:
    st.session_state.username = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if "active_zen" not in st.session_state:
    st.session_state["active_zen"] = False
    
if st.session_state["active_zen"]:
    show_meditation_mode()
    st.stop()

# ---------------- LOAD MODELS ----------------
ml_model = joblib.load("ml_model.pkl")
dl_model = tf.keras.models.load_model("dl_model.h5")


st.markdown("""
<style>

/* 🔥 PREMIUM METALLIC FONTS */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Rajdhani:wght@500;600&display=swap');

/* Background - deeper metallic */
.stApp {
    background: radial-gradient(circle at top left, #1e293b, #0f172a 60%, #020617);
    color: #e5e7eb;
}

/* Base font */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Glass + metallic card */
.glass {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.12),
        rgba(255,255,255,0.04)
    );
    border-radius: 18px;
    padding: 20px;

    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.15);

    box-shadow:
        inset 0 1px 1px rgba(255,255,255,0.25),
        0 8px 30px rgba(0,0,0,0.7);

    color: #f1f5f9;
    text-align: center;
    transition: 0.3s ease;
}

/* Hover glow (SOFT METALLIC, not neon) */
.glass:hover {
    transform: scale(1.03);
    box-shadow:
        0 0 20px rgba(148,163,184,0.25),
        inset 0 1px 1px rgba(255,255,255,0.3);
}

/* Title metallic glow (refined) */
.title {
    font-family: cursive;
    font-size: 50px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-align: center;
    margin-bottom: 15px;

    
}

/* Buttons metallic */
div.stButton > button {
    background: linear-gradient(145deg,#1e293b,#334155);
    color: #e2e8f0;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
    height: 45px;
    width: 100%;
    font-size: 16px;
    font-family: 'Rajdhani', sans-serif;

    box-shadow:
        inset 0 1px 2px rgba(255,255,255,0.2),
        0 5px 15px rgba(0,0,0,0.6);
}

/* Button hover */
div.stButton > button:hover {
    background: linear-gradient(145deg,#334155,#475569);
    box-shadow: 0 0 10px rgba(148,163,184,0.3);
}

/* Inputs styling (clean glass inputs) */
input, .stNumberInput, .stTextInput, .stSelectbox {
    background-color: rgba(255,255,255,0.04) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e5e7eb !important;
}

/* Subtle divider (optional use) */
hr {
    border: 1px solid rgba(255,255,255,0.08);
}
/* 🔥 HERO SECTION */
.hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 40px;
    border-radius: 20px;
    margin-top: 30px;

    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,0.1);
}

.hero-text {
    width: 50%;
}

.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 42px;
    font-weight: 600;

    background: linear-gradient(90deg,#f1f5f9,#94a3b8,#38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    margin-top: 15px;
    font-size: 16px;
    color: rgba(226,232,240,0.7);
    line-height: 1.6;
}

.hero-img img {
    width: 320px;
    border-radius: 15px;
    animation: float 4s ease-in-out infinite;
}
/* Animated Gradient Background */
.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #334155, #1e293b);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
    100% { transform: translateY(0px); }
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------

if "username" not in st.session_state:
    st.session_state.username = None

# 🚫 NOT LOGGED IN → SHOW ONLY LOGIN PAGE
if st.session_state.username is None:

    components.html("""
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:40px;
        border-radius:20px;
        margin-top:30px;
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.1);
    ">
    
        <div style="width:50%;">
            <div style="
                font-family: Rajdhani;
                font-size:42px;
                font-weight:600;
                background: linear-gradient(90deg,#f1f5f9,#94a3b8,#38bdf8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">
                AI Digital Twin
            </div>
    
            <div style="
                margin-top:15px;
                font-size:16px;
                color: rgba(226,232,240,0.7);
                line-height:1.6;
            ">
                Your intelligent digital replica that learns, adapts, and evolves.
                Predict behavior, optimize health, and unlock your full potential.
            </div>
        </div>
    
        <div>
            <img src="https://i.pinimg.com/originals/71/ff/80/71ff803fbe504006b29e71bbe69779f6.gif"
                 style="width:450px; border-radius:10px; animation: float 4s ease-in-out infinite;">
        </div>
    
    </div>
    
    <style>
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    </style>
    """, height=350)

    username_input = st.text_input("Enter Username")

    if st.button("Login"):
        if username_input:
            st.session_state.username = username_input
            st.rerun()

    # ⛔ STOP EVERYTHING BELOW FROM RUNNING
    st.stop()
username = st.session_state.username
user_file = f"{username}_history.csv"
profile_file = f"{username}_profile.json"


col1, col2, col3 = st.columns([1, 6, 1])

# 🧠 Title (CENTER-LEFT)
with col2:
    st.markdown(f"""
    <div style="
        font-family: Rajdhani;
        text-align:center;
        font-size: 36px;
        font-weight: 600;
        background: linear-gradient(90deg,#e2e8f0,#94a3b8,#64748b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top:10px;
    ">
        AI Digital Twin Dashboard
    </div>
    <div style="font-family: Rajdhani; text-align:center; padding:20px;">
    <div style="font-size:30px; color:#94a3b8;">👋 WELCOME, {username}</div>
    </div>
    """, unsafe_allow_html=True)

# 🚪 Logout (RIGHT)
with col3:
    if st.button("🚪Logout"):
        st.session_state.username = None
        st.rerun()

# ---------------- PROFILE ----------------
if os.path.exists(profile_file):
    with open(profile_file, "r") as f:
        try:
            profile = json.load(f)
        except:
            profile = {}
else:
    profile = {}

# SAFE ACCESS
age = profile.get("age")
gender = profile.get("gender")

# If missing → ask again
if age is None or gender is None:
    st.subheader("👤 Setup Profile")

    age = st.number_input("Age", 10, 80)
    gender = st.selectbox("Gender", ["","Male","Female"])

    if st.button("Save Profile"):
        profile = {"age": age, "gender": gender}
        with open(profile_file, "w") as f:
            json.dump(profile, f)

        st.success("Profile saved! Reload page.")
        st.stop()
# 🧑 Avatar (LEFT)
with col1:
    img_a_base64 = get_base64("boy.jpg")
    img_b_base64 = get_base64("girl.jpg")

    # Clean the input: handle None, strip spaces, and lowercase it
    check_gender = str(gender).lower().strip() if gender else "unknown"

    # Define variables inside a robust logic structure
    if check_gender == "male":
        animation_style = "" 
        img_a_opacity = "1"
        img_b_opacity = "0"
    elif check_gender == "female":
        animation_style = ""
        img_a_opacity = "0"
        img_b_opacity = "1"
    else:
        # This catch-all handles "unknown", "Unknowm", or any other text
        animation_style = "animation: flip 1s infinite;"
        img_a_opacity = "1"
        img_b_opacity = "1"

    st.markdown(f"""
        <style>
            @keyframes flip {{
                0% {{ opacity: 1; }}
                49% {{ opacity: 1; }}
                50% {{ opacity: 0; }}
                100% {{ opacity: 0; }}
            }}
            .img-container {{ position: relative; width: 200px; height: 200px; }}
            .img-a {{ 
                position: absolute; 
                {animation_style} 
                opacity: {img_a_opacity};
                border-radius: 50%; 
            }}
            .img-b {{ 
                position: absolute; 
                {animation_style} 
                animation-direction: reverse;
                opacity: {img_b_opacity};
                border-radius: 50%; 
            }}
        </style>
        <div class="img-container">
            <img class="img-a" src="data:image/jpeg;base64,{img_a_base64}" width="180">
            <img class="img-b" src="data:image/jpeg;base64,{img_b_base64}" width="180">
        </div>
    """, unsafe_allow_html=True)
# ---------------- INPUT ----------------
c1,c2,c3 = st.columns([4,3,4])
with c1:
    st.markdown(f"""
    <div style="
        font-family: cursive;
        text-align:center;
        font-size: 22px;
        font-weight: 600;
        margin-top:10px;
    ">
        💪 Physical Health
    </div>
    """, unsafe_allow_html=True)
    steps = c1.number_input("Steps",0,20000)
    calories = c1.number_input("Calories(kcal)",500,4000)
    sleep = c1.number_input("Sleep(in min)",0,600)
    active = c1.number_input("Active(in min)",0,120)

    sedentary = 1440 - active - sleep
with c2:
    try:
        # Encode the image to base64
        twin_base64 = get_base64("twin.png")
        
        st.markdown(f"""
            <style>
                @keyframes scan {{
                    0% {{ top: 0%; }}
                    100% {{ top: 100%; }}
                }}
                
                .twin-container {{
                    position: relative; /* Needed for the scan line */
                    overflow: hidden;
                }}
                
                .scan-line {{
                    position: absolute;
                    width: 100%;
                    height: 2px;
                    background: rgba(148, 163, 184, 0.5);
                    box-shadow: 0 0 10px #94a3b8;
                    z-index: 10;
                    animation: scan 3s linear infinite;
                }}
                @keyframes float {{
                    0% {{ transform: translateY(0px) rotate(0deg); }}
                    50% {{ transform: translateY(-10px) rotate(1deg); }}
                    100% {{ transform: translateY(0px) rotate(0deg); }}
                }}
                .twin-container {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }}
                .twin-img {{
                    width: 250px;
                    border-radius: 20px;
                    animation: float 4s ease-in-out infinite;
                    /* Added a dark cyber glow */
                    box-shadow: 0 0 30px rgba(148, 163, 184, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    mask-image: radial-gradient(circle, black 60%, transparent 100%);
                    -webkit-mask-image: radial-gradient(circle, black 60%, transparent 100%);
                    filter: drop-shadow(0 0 20px rgba(148, 163, 184, 0.3));
                }}
            </style>
            <div class="twin-container">
                <img src="data:image/png;base64,{twin_base64}" class="twin-img">
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("twin.png not found. Please check the file path!")
with c3:
    st.markdown(f"""
    <div style="
        font-family: cursive;
        text-align:center;
        font-size: 22px;
        font-weight: 600;
        margin-top:10px;
    ">
        🧠 Mental State
    </div>
    """, unsafe_allow_html=True)
    stress = c3.number_input("Stress(1-5)", 1, 5)
    energy = c3.number_input("Energy(1-5)", 1, 5)
    focus = c3.number_input("Focus(1-5)", 1, 5)
    motivation = c3.number_input("Motivation(1-5)", 1, 5)

# Female logic
period = "No"
pain = cramps = cravings = mood_swings = 0

if gender == "Female":
    st.subheader("🌸 Period Health (Optional)")
    period = st.selectbox("On Period?", ["No","Yes"])

    if period == "Yes":
        r1c1, r1c2 = st.columns(2)
        pain = r1c1.number_input("Pain(1-5)",1,5)
        cramps = r1c2.number_input("Cramps(1-5)",1,5)
        r2c1, r2c2 = st.columns(2)
        cravings = r2c1.number_input("Cravings(1-5)",1,5)
        mood_swings = r2c2.number_input("Mood Swings(1-5)",1,5)

# ---------------- ANALYZE ----------------
if st.button("Analyze"):
    progress_text = st.empty()  # Placeholder for text
    bar = st.progress(0)       # The actual bar
    
    # Simulate different stages of analysis
    stages = [
        "🔍 Scanning historical patterns...",
        "🧬 Correlating biometric data...",
        "🧠 Simulating Digital Twin response...",
        "✨ Finalizing predictions..."
    ]
    
    for i, stage in enumerate(stages):
        progress_text.markdown(f"**Status:** {stage}")
        bar.progress((i + 1) * 25)
        time.sleep(0.5)
    
    bar.empty()
    progress_text.empty()
    data = np.array([[steps, active, sedentary, calories, sleep, age]])

    ml_pred = ml_model.predict(data)[0]
    dl_pred = np.argmax(dl_model.predict(data), axis=1)[0]

    score = energy + focus + motivation - stress

    if gender == "Female" and period == "Yes":
        score -= (pain + cramps + mood_swings)/2

    if score < 5:
        q_pred = 0
    elif score < 10:
        q_pred = 1
    elif score < 15:
        q_pred = 2
    else:
        q_pred = 3

    final_pred = int((ml_pred + dl_pred + q_pred)/3)

    moods = ["Sad","Stressed","Happy","Energetic"]
    mood = moods[final_pred]

    # ---------------- SAVE ----------------
    today = datetime.today().strftime("%Y-%m-%d")

    record = pd.DataFrame({
        "date":[today],
        "steps":[steps],
        "calories":[calories],
        "sleep":[sleep],
        "active":[active],
        "mood":[mood]
    })

    if os.path.exists(user_file):
        history = pd.read_csv(user_file)
        history = pd.concat([history,record])
    else:
        history = record

    history.to_csv(user_file,index=False)
    history["date"] = pd.to_datetime(history["date"])
    history["sleep"] = pd.to_numeric(history["sleep"], errors='coerce')
    history["steps"] = pd.to_numeric(history["steps"], errors='coerce')

    # ---------------- GLASS KPI ----------------
    st.markdown(f"""
    <div style="
        font-family: cursive;
        font-size: 30px;
        font-weight: 600;
        margin-top:10px;
    ">
        🚀 Dashboard
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    c1.markdown(f'<div class="glass">👣<br><small>STEPS</small><h2>{steps}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="glass">🔥<br><small>CALORIES</small><h2>{calories}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="glass">😴<br><small>SLEEP</small><h2>{sleep}</h2></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="glass">🧠<br><small>MOOD</small><h2>{mood}</h2></div>', unsafe_allow_html=True)
    st.session_state["last_mood"] = mood
    # ---------------- ANIMATED-STYLE GRAPH ----------------
    st.markdown(f"""
    <div style="
        font-family: cursive;
        font-size: 30px;
        font-weight: 600;
        margin-top:10px;
    ">
        📊 Smart Trends
    </div>
    """, unsafe_allow_html=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
        x=history["date"],
        y=history["steps"],
        mode='lines+markers',
        line=dict(width=4, color='#64748b'),
        name="Steps (Goal: 10000)"
        ),
    secondary_y = False,
    )

    fig.add_trace(go.Scatter(
        x=history["date"],
        y=history["sleep"],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#a78bfa'),
        name="Sleep (Goal: 480 min.)"
        ),
    secondary_y =True,
    )

    fig.update_layout(
        template="plotly_dark",
        transition_duration=800,
        title="Activity + Recovery Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- INSIGHTS ----------------
    
    def glass_card(title, content, color="#94a3b8"):
        return f"""
        <div class="glass" style="margin-bottom:15px; text-align:left;">
            <div style="font-family:Rajdhani; font-size:22px; color:{color}; margin-bottom:8px;">
                {title}
            </div>
            <div style="font-size:18px; color:#e5e7eb;">
                {content}
            </div>
        </div>
        """
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<p class="title">🧠 Insights</p>', unsafe_allow_html=True)
        steps = history["steps"].iloc[-1]
        sleep = history["sleep"].iloc[-1]
        insights_html = ""
        
        if steps < 5000:
            insights_html += glass_card("Low Activity", "Your activity is too low → affecting mood", "#fbbf24")
        
        if sleep < 360:
            insights_html += glass_card("Poor Sleep", "Sleep deficiency impacting performance", "#38bdf8")
        
        if steps > 8000 and sleep > 400:
            insights_html += glass_card("Great Consistency", "Your lifestyle is well balanced", "#4ade80")
        
        st.markdown(insights_html, unsafe_allow_html=True)

    # ---------------- REPORT ----------------
    with c2:
        st.markdown('<p class="title">🧾 AI Report</p>', unsafe_allow_html=True)
    
        report = f"Your current emotional state is <b>{mood}</b>."
        
        if mood == "Sad":
            report += "<br>• Increase sunlight exposure<br>• Engage in social interaction"
        elif mood == "Stressed":
            report += "<br>• Reduce workload<br>• Improve sleep cycle"
        elif mood == "Energetic":
            report += "<br>• Utilize this energy for productivity"
        
        st.markdown(glass_card("Analysis", report, "#a78bfa"), unsafe_allow_html=True)

    # ---------------- PERIOD HEALTH ANALYSIS ----------------

    if gender == "Female":
    
        st.markdown('<p class="title">🌸 Period Health Analysis</p>', unsafe_allow_html=True)
    
        if period == "Yes":
    
            period_score = (pain + cramps + mood_swings + cravings) / 4
    
            # Classification
            if period_score >= 4:
                condition = "Severe"
                color = "#ef4444"
            elif period_score >= 3:
                condition = "Moderate"
                color = "#f59e0b"
            else:
                condition = "Mild"
                color = "#22c55e"
    
            # ✅ CONDITION CARD
            st.markdown(glass_card(
                "Condition Status",
                f"Your current condition is <b>{condition}</b>",
                color
            ), unsafe_allow_html=True)
    
            # ---------------- SMART CARDS (GRID STYLE) ----------------
            col1, col2 = st.columns(2)
    
            with col1:
    
                if pain >= 4:
                    st.markdown(glass_card(
                        "High Pain",
                        "Take proper rest<br>Use heating pad for relief",
                        "#ef4444"
                    ), unsafe_allow_html=True)
    
                elif pain >= 2:
                    st.markdown(glass_card(
                        "Mild Pain",
                        "Light stretching may help",
                        "#f59e0b"
                    ), unsafe_allow_html=True)
    
                if cramps >= 4:
                    st.markdown(glass_card(
                        "Severe Cramps",
                        "Avoid heavy workouts<br>Try yoga or light movement",
                        "#ef4444"
                    ), unsafe_allow_html=True)
    
                elif cramps >= 2:
                    st.markdown(glass_card(
                        "Cramps",
                        "Light walking may reduce discomfort",
                        "#38bdf8"
                    ), unsafe_allow_html=True)
    
            with col2:
    
                if mood_swings >= 4:
                    st.markdown(glass_card(
                        "Mood Swings",
                        "Avoid stress triggers<br>Try music or relaxation",
                        "#a78bfa"
                    ), unsafe_allow_html=True)
    
                elif mood_swings >= 2:
                    st.markdown(glass_card(
                        "Mood Variation",
                        "Stay engaged in light activities",
                        "#60a5fa"
                    ), unsafe_allow_html=True)
    
                if cravings >= 4:
                    st.markdown(glass_card(
                        "High Cravings",
                        "Eat iron-rich & healthy snacks",
                        "#f472b6"
                    ), unsafe_allow_html=True)
    
                elif cravings >= 2:
                    st.markdown(glass_card(
                        "Cravings",
                        "Maintain balanced diet",
                        "#94a3b8"
                    ), unsafe_allow_html=True)
    
            # ---------------- FINAL INSIGHT CARD ----------------
            if condition == "Severe":
                msg = "Your body needs recovery → prioritize rest & hydration"
            elif condition == "Moderate":
                msg = "Manage your routine → avoid overexertion"
            else:
                msg = "You are handling it well → maintain routine"
    
            st.markdown(glass_card("AI Insight", msg, color), unsafe_allow_html=True)
    
        else:
            st.markdown(glass_card(
                "Status",
                "No period-related impact today",
                "#38bdf8"
            ), unsafe_allow_html=True)
    
        
        # ---------------- FINAL AI SUGGESTION BLOCK ----------------
    
    # Calculate overall health score
    health_score = (
        (steps/10000)*25 +
        (sleep/480)*25 +
        (active/60)*20 +
        (energy/5)*15 +
        (focus/5)*15
    )
    
    health_score = round(min(100, max(0, health_score)),1)
    
    # st.write(f"🔢 Overall Health Score: {health_score}/100")
    
    # ---------------- MAIN DECISION ----------------
    c1,c2 = st.columns(2)
    with c1:
    
        st.markdown('<p class="title">💡 Final Recommendation</p>', unsafe_allow_html=True)
    
        if health_score >= 75:
            msg = "Peak performance detected. Maintain routine and push limits."
            color = "#22c55e"
        
        elif health_score >= 50:
            msg = "Stable condition. Improve sleep and activity for optimization."
            color = "#f59e0b"
        
        else:
            msg = "Body recovery required. Focus on rest, hydration, and stress reduction."
            color = "#ef4444"
        
        st.markdown(glass_card(f"Health Score: {health_score}/100", msg, color), unsafe_allow_html=True)

# ---------------- INTELLIGENT ADD-ONS ----------------
    with c2:
        st.markdown('<p class="title">🧠 Smart Insights</p>', unsafe_allow_html=True)
        
        if steps < 4000:
            st.markdown(glass_card("Low Activity", "Increase daily movement", "#fbbf24"), unsafe_allow_html=True)
        
        elif sleep < 360:
            st.markdown(glass_card("Sleep Deficit", "Major impact on focus & mood", "#38bdf8"), unsafe_allow_html=True)
        
        elif active < 20:
            st.markdown(glass_card("Low Exercise", "Energy levels may drop", "#f87171"), unsafe_allow_html=True)
        
        elif energy <= 2:
            st.markdown(glass_card("Low Energy", "Improve diet & sleep", "#a78bfa"), unsafe_allow_html=True)
            
        else:
            st.markdown(glass_card("Good Energy", "Keet it up!!", "#a78bfa"), unsafe_allow_html=True)
    
    # ---------------- FINAL ONE-LINE AI SUMMARY ----------------
    
    st.markdown('<p class="title">🤖 AI Summary</p>', unsafe_allow_html=True)

    if health_score >= 75:
        summary = "Optimal condition. Maximize productivity."
    elif health_score >= 50:
        summary = "Moderate performance. Improve consistency."
    else:
        summary = "Recovery mode required. Focus on rest."
    
    st.markdown(glass_card("Overall Status", summary, "#60a5fa"), unsafe_allow_html=True)

# ✅ GLOBAL ZEN TRIGGER (FIX)
if st.session_state.get("last_mood") in ["Stressed", "Sad"]:
    
    st.warning(f"⚠️ You seem {st.session_state['last_mood']}")
    
    if st.button("🧘 Enter Zen Mode"):
        st.session_state["active_zen"] = True
        st.rerun()
