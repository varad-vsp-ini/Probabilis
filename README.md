# Probabilis
# Probabilis | Password Analyzer & Security Trainer

Try now: https://probabilis1.streamlit.app/

Probabilis is an interactive password analysis and learning platform built using **Streamlit**. It helps users understand password strength, vulnerabilities, and the principles behind secure password creation. The app combines educational challenges, quick checks, and deep analysis using metrics like Shannon entropy, Markov scores, and DCAI.

---

## Features

- 🔐 **Three Modes:**
  - **LEARN:** Persona-based challenges to teach social engineering awareness.
  - **QUICK CHECK:** Instant password scoring with actionable feedback.
  - **DEEP ANALYSIS:** Detailed breakdown including entropy and Markov analysis.

- 🎓 **Educational Quotes:** Each mode shows a contextual quote to motivate and educate users.
- 🛠️ **Custom Analysis Engine:** Combines Shannon entropy, Expectation entropy, Markov score, DCAI, and vulnerabilities.

---

## File Overview
- `landingpage.py` - Introduction page
- `newapp.py` — Frontend Streamlit application.  
- `pass_analyzer.py` — Backend analysis module containing the core password evaluation logic.  
  Rest all files are assets and markov training data

---

## Setup Instructions

### 1. Clone the Repository

`git clone https://github.com/varad-vsp-ini/Probabilis.git
cd Probabilis-main`

### 2. Install Dependencies

Make sure you have Python 3.8+ installed. Then install required packages:
* numpy
* pandas
* streamlit

### 3. Run the app

`streamlit run landingpage.py`
