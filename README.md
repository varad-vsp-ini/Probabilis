# Probabilis
# Probabilis | Password Analyzer & Security Trainer

Probabilis is an interactive password analysis and learning platform built using **Streamlit**. It helps users understand password strength, vulnerabilities, and the principles behind secure password creation. The app combines educational challenges, quick checks, and deep analysis using metrics like Shannon entropy, Markov scores, and DCAI.

---

## Features

- 🔐 **Three Modes:**
  - **LEARN:** Persona-based challenges to teach social engineering awareness.
  - **QUICK CHECK:** Instant password scoring with actionable feedback.
  - **DEEP ANALYSIS:** Detailed breakdown including entropy and Markov analysis.

- 🎓 **Educational Quotes:** Each mode shows a contextual quote to motivate and educate users.
- ✨ **Neon-Pulse UI:** Cyberpunk-inspired neon-glow interface for an engaging experience.
- 🛠️ **Custom Analysis Engine:** Combines Shannon entropy, Expectation entropy, Markov score, DCAI, and vulnerabilities.

---

## File Overview

- `newapp.py` — Frontend Streamlit application.  
- `pass_analyzer.py` — Backend analysis module containing the core password evaluation logic.  
- `training_data/` — Directory containing datasets used for Markov-based analysis.

---

## Setup Instructions

### 1. Clone the Repository

`git clone <your-repo-url>
cd <repo-folder>`

### 2. Install Dependencies

Make sure you have Python 3.8+ installed. Then install required packages:
* numpy
* pandas
*streamlit

### 3. Run the app

`streamlit run newapp.py`
