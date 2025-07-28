# study_sensei.py

import streamlit as st
import time
import pandas as pd
import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt
import os

# Setup
LOG_FILE = "study_log.csv"

# Create the log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    df_init = pd.DataFrame(columns=["Date", "Subject", "Duration (mins)", "Feedback", "Sentiment", "Suggestions"])
    df_init.to_csv(LOG_FILE, index=False)

# App Title
st.set_page_config(page_title="StudySensei", page_icon="📚")
st.title("📚 StudySensei - Your Personalized Study Coach AI")
st.markdown("Welcome to **Panda Hacks 2025**! This AI-powered study coach tracks your sessions, analyzes your mood, and gives personalized tips.")

# Input Section
subject = st.text_input("🧠 What subject/topic are you studying?")
start_btn = st.button("▶️ Start Session")
stop_btn = st.button("⏹️ End Session")

# Pomodoro Timer
if st.button("🍅 Start 25-min Pomodoro"):
    st.info("Pomodoro Started! Focus for 25 minutes...")
    pomodoro_bar = st.progress(0)
    for i in range(25 * 60):
        time.sleep(1)
        pomodoro_bar.progress((i + 1) / (25 * 60))
    st.success("🎉 Pomodoro complete! Take a short break.")

# Session Timer Handling
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None

if start_btn:
    if subject:
        st.session_state['start_time'] = time.time()
        st.success(f"✅ Started studying: {subject}")
    else:
        st.warning("⚠️ Please enter a subject before starting.")

if stop_btn and st.session_state['start_time']:
    duration = int((time.time() - st.session_state['start_time']) / 60)
    st.success(f"✅ Session ended. Duration: {duration} minutes.")
    feedback = st.text_area("💬 Reflect on your session (What went well? Any issues?)")

    if feedback:
        blob = TextBlob(feedback)
        polarity = blob.sentiment.polarity
        sentiment = "Positive" if polarity > 0 else "Neutral" if polarity == 0 else "Negative"

        # AI Suggestions
        if sentiment == "Positive":
            suggestions = "Keep it up! Maybe challenge yourself with a harder topic next time."
        elif sentiment == "Neutral":
            suggestions = "Try using active recall or spaced repetition techniques."
        else:
            suggestions = "It’s okay to have bad sessions. Take a break and come back refreshed."

        # Save to CSV
        new_row = pd.DataFrame({
            "Date": [datetime.date.today()],
            "Subject": [subject],
            "Duration (mins)": [duration],
            "Feedback": [feedback],
            "Sentiment": [sentiment],
            "Suggestions": [suggestions]
        })
        existing = pd.read_csv(LOG_FILE)
        updated = pd.concat([existing, new_row], ignore_index=True)
        updated.to_csv(LOG_FILE, index=False)

        # Display result
        st.markdown("### 🧠 AI Feedback")
        st.write("**Sentiment:**", sentiment)
        st.write("**Suggestion:**", suggestions)
    else:
        st.warning("✍️ Please enter your feedback to get personalized suggestions.")

# Study History Viewer
st.markdown("---")
if st.checkbox("📊 Show My Study History"):
    df = pd.read_csv(LOG_FILE)
    st.dataframe(df.tail(10))

    if not df.empty:
        st.markdown("### 📈 Study Time by Day")
        df['Date'] = pd.to_datetime(df['Date'])
        daily_summary = df.groupby("Date")["Duration (mins)"].sum()
        fig, ax = plt.subplots()
        daily_summary.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title("Study Duration by Date")
        ax.set_ylabel("Minutes")
        ax.set_xlabel("Date")
        st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ ")
