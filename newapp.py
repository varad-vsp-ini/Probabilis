import streamlit as st
import math
import random
#from zxcvbn import zxcvbn
from pass_analyzer import analyze_password

# --- PAGE CONFIG ---
st.set_page_config(page_title="Password Analyzer | Team Ve", layout="centered")

# --- CUSTOM STYLING (The Pink/Dark Theme) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap" rel="stylesheet">
    <style>
    body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { 
        background-color: #0F0F1A !important; 
        color: #FFFFFF; 
        font-family: 'Georgia', serif !important; 
    }
    h1, h2, h3, h4, h5, h6, .header, .stTitle {
        font-family: 'Delicious Handrawn', cursive !important;
    }
    @keyframes neonPulse {
        0%, 100% { box-shadow: 0 0 15px rgba(255,75,145,0.3), 0 0 30px rgba(255,75,145,0.2); }
        50% { box-shadow: 0 0 25px rgba(255,75,145,0.6), 0 0 50px rgba(255,75,145,0.4); }
    }
    .window-box {
        background-color: #1A1A2E;
        border: 3px solid #FF4B91;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(255, 75, 145, 0.2);
        color: #FF4B91;
        font-family: 'Georgia', serif;
        text-align: center;
        font-size: 1.3rem;
        text-shadow: 0 0 5px #FF4B91, 0 0 10px #FF4B91, 0 0 15px #FF4B91;
        animation: neonPulse 2s infinite ease-in-out;
    }
    .stTextInput>div>div>input, .stText, .stMarkdown, .stButton>button {
        color: #FFFFFF !important;
        font-family: 'Delicious Handrawn', cursive !important;
    }
    p, span, .stMarkdown p, .stMarkdown span {
        font-family: 'Georgia', serif !important;
    }
    .stButton>button {
        background-color: #000000 !important;
    }
    [data-testid="stSidebar"] .css-1aumxhk label, [data-testid="stSidebar"] .css-ckOyDo {
        color: #FFFFFF !important;
    }
    [data-testid="collapseSidebarButton"] svg {
        display: none !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-family: 'Delicious Handrawn', cursive !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Delicious Handrawn', cursive !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1C1A26 !important;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: #1C1A26 !important;
    }
    .header { 
        text-align: center; 
        padding: 40px 0; 
        color: #FF4B91; 
        font-size: 4.5rem; 
        font-weight: 800; 
        font-family: 'Delicious Handrawn', cursive !important; 
        letter-spacing: 2px; 
    }
    .stProgress>div>div>div>div { background-color: #FF4B91; }
    .stTextInput>div>div>input { background-color: #2D2D2D; color: #FF4B91; border: 2px solid #FF4B91; }
    [data-testid="collapseSidebarButton"] {
        background: transparent !important;
        border: none !important;
        width: 2.2rem !important;
        height: 2.2rem !important;
        padding: 0 !important;
    }

    [data-testid="collapseSidebarButton"]::after {
        content: "";
        display: inline-block;
        width: 24px;
        height: 24px;
        background-image: url("Probabilis/assets/sidebar_icon.png");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }


    
    </style>
""", unsafe_allow_html=True)
st.markdown("<div class='header'>🔐 PROBABILIS</div>", unsafe_allow_html=True)
# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Select Mode")
mode = st.sidebar.radio("Navigation", ["(A) LEARN", "(B) QUICK CHECK", "(C) DEEP ANALYSIS"])

# --- MODE-SPECIFIC QUOTES ---
mode_quotes = {
    "(A) LEARN": '"Security is not a product, but a process." — Bruce Schneier',
    "(B) QUICK CHECK": '"A password is only as strong as your weakest link."',
    "(C) DEEP ANALYSIS": '"Problem Solving is Often a Matter of Cooking Up an Appropriate Markov Chain." — Olle Häggström'
}

# --- DISPLAY NEON QUOTE ---
quote = mode_quotes.get(mode, "")
st.markdown(f"<div class='window-box'>{quote}</div>", unsafe_allow_html=True)

# --- PERSONA DATABASE ---
# Characters from Hollywood and Bollywood
personas = [
    {"name": "Tony Stark", "dob": "29/05/1970", "info": "AI Assistant: Jarvis", "keywords": ["tony", "stark", "jarvis", "1970"]},
    {"name": "Kabir Singh", "dob": "25/08/1981", "info": "Medical Field: Surgeon", "keywords": ["kabir", "singh", "surgeon", "1981"]},
    {"name": "Harry Potter", "dob": "31/07/1980", "info": "Pet: Hedwig", "keywords": ["harry", "potter", "hedwig", "1980"]},
    {"name": "Simran Singh", "dob": "12/10/1975", "info": "Favorite Trip: Europe", "keywords": ["simran", "europe", "1975", "singh"]},
    {"name": "Bruce Wayne", "dob": "19/02/1972", "info": "Secret: Batman", "keywords": ["bruce", "wayne", "batman", "1972"]},
    {"name": "Raj Malhotra", "dob": "02/11/1965", "info": "Famous Catchphrase: Senorita", "keywords": ["raj", "malhotra", "senorita", "1965"]},
]



# --- MODE A: LEARN ---
if mode == "(A) LEARN":
    st.markdown("<div class='window-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Indie Flower, cursive; font-size: 2.5rem;'>🎓 LEARN MODE</h1>", unsafe_allow_html=True)
    st.write("Most people create passwords using their personal details. Can you guess what a hacker would try first?")

    # Initialize session state to keep the same character until 'New Challenge' is clicked
    if 'current_persona' not in st.session_state:
        st.session_state.current_persona = random.choice(personas)

    if st.button("🔄 Get New Character"):
        st.session_state.current_persona = random.choice(personas)
        st.rerun()

    p = st.session_state.current_persona
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        st.markdown(f"### Persona: **{p['name']}**")
        st.info(f"📅 **DOB:** {p['dob']}\n\nℹ️ **Extra Info:** {p['info']}")
        
    with col2:
        guess = st.text_input(f"Guess {p['name'].split()[0]}'s password:", placeholder="e.g. NameYear")
        if guess:
            # Check if the guess contains any of the persona keywords
            found_keywords = [word for word in p['keywords'] if word.lower() in guess.lower()]
            
            if found_keywords:
                st.error(f"⚠️ **Vulnerable!** You used '{found_keywords[0]}'.")
                st.write("Hackers use 'Social Engineering' to find these details from your social media and guess your password instantly.")
            else:
                st.success("✅ Good! That's not an obvious guess.")
                st.write("A strong password should have no connection to your name, DOB, or pets.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- MODE B: QUICK CHECK ---
elif mode == "(B) QUICK CHECK":
    # (Kept the same as your original code)
    st.markdown("<div class='window-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Indie Flower, cursive; font-size: 2.5rem;'>⚡ QUICK CHECK</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Enter password to test", type="password")
    
    if pwd:
        results = analyze_password(pwd)
        final_score = results['final_security_score']  # 0 to 1
    
        progress = final_score  # Direct mapping to progress bar
    
        # Flexible threshold logic
        if progress < 0.30:
            label = "WEAK!"
            color = "#FF0000"
        elif progress < 0.55:
            label = "STILL WEAK"
            color = "#FF4500"
        elif progress < 0.70:
            label = "FAIR"
            color = "#FFCC00"
        elif progress < 0.78:
            label = "GOOD"
            color = "#ADFF2F"
        else:
            label = "STRONG!"
            color = "#00FF00"
    
        st.markdown(
            f"<h2 style='color:{color}; text-align:center;'>{label}</h2>",
            unsafe_allow_html=True
        )
    
        st.progress(progress)
        if results['suggestions'] :
            st.markdown("---")
            st.subheader("💡 Suggestions")
            if results['suggestions']:
                st.warning(f"**Warning:** {results['suggestions'][0]}")
            for suggestion in results['suggestions']:
                st.write(f"• {suggestion}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MODE C: DEEP ANALYSIS ---
elif mode == "(C) DEEP ANALYSIS":
    # (Kept the same as your original code)
    st.markdown("<div class='window-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Indie Flower, cursive; font-size: 2.5rem;'>🔬 DEEP ANALYSIS</h1>", unsafe_allow_html=True)
    target_pwd = st.text_input("Enter password for full breakdown")
    if target_pwd:
        results = analyze_password(target_pwd)  # Using the custom analysis function from pass_analyzer.py
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Score", f"{results['final_security_score']}")
            st.metric("Expectation Entropy", f"{results['expectation_entropy']}")
            st.metric("DCAI Score", f"{results['dcai_score']}")
            st.metric("Shannon Entropy", f"{results['shannon_entropy']}")
            st.metric("Markov Score", f"{results['markov_score']}")
           # st.write(f"⏱️ **Crack Time:** {results['crack_times_display']['offline_fast_hashing_1e10_per_second']}")
        with col2:
            st.write("**Vulnerabilities Found:**")
            for suggestion in results['suggestions']:
                st.write(f"- {suggestion}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Powered by Team Ve Analysis Engine")


























