# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 18:48:06 2026

@author: Varad
"""

import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Probabilis", layout="wide")

# --- Encode local image as base64 ---
# Save a painting image in same folder as this file, name it: bg.jpg
def get_base64_of_image(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Make sure you place a painting image named "bg.jpg" in same directory
img_base64 = get_base64_of_image("bg.jpg")

def go_to_app():
    st.switch_page("pages/newapp.py")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&display=swap');

/* Hide Streamlit UI */
[data-testid="stHeader"] {{visibility: hidden;}}
[data-testid="stSidebar"] {{display: none;}}
.block-container {{padding-top: 0rem; padding-bottom: 0rem;}}

/* Background */
.stApp {{
    background:
        linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.85)),
        url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Wrapper */
.wrapper {{
    text-align: center;
    margin-top: 10vh;
}}

/* Title */
.title {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(4rem, 8vw, 6rem);
    color: #E8D8A9;
    letter-spacing: 0.15em;
}}

/* Subtitle */
.subtitle {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    color: #C6A75E;
    font-style: italic;
    margin-top: 0.5rem;
}}

/* Divider */
.divider {{
    width: 60%;
    margin: 2rem auto;
    height: 1px;
    background: linear-gradient(to right, transparent, #C6A75E, transparent);
}}

/* Body */
.text {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem;
    color: #F2F2F2;
    line-height: 1.7;
    max-width: 700px;
    margin: auto;
}}

/* Center button container */
div.stButton {{
    display: flex;
    justify-content: center;
}}

/* Button */
.stButton>button {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    padding: 0.6em 2.5em;
    margin-top: 2rem;
    background-color: #C6A75E;
    color: black;
    border-radius: 6px;
    border: none;
    transition: 0.3s ease;
}}

.stButton>button:hover {{
    background-color: #E8D8A9;
    transform: scale(1.05);
}}

/* Corner Motto */
.corner {{
    position: fixed;
    bottom: 15px;
    right: 25px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.85rem;
    color: rgba(232,216,169,0.6);
    font-style: italic;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 10vh;
    text-align: center;
">
    <div class='title'>PROBABILIS</div>
    <div class='subtitle'>In Probabilitate Veritas</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown("""
<div class='text'>
Probabilis is not a password checker.<br><br>

It is a probabilistic intelligence engine where uncertainty is quantified,
behavior is modeled, and cultural semantics are evaluated.<br><br>

Shannon entropy measures structural unpredictability.<br>
Expectation entropy evaluates statistical likelihood.<br>
Markov chains model behavioral sequence patterns.<br>
Dynamic Cultural Activity Index detects semantic gravity.<br><br>

Four analytical pillars. One synthesized verdict.
</div>
""", unsafe_allow_html=True)

if st.button("Enter the Analysis"):
    go_to_app()


st.markdown("<div class='corner'>Veritas per Numeros</div>", unsafe_allow_html=True)