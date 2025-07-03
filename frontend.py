import streamlit as st
import requests
from audio_recorder_streamlit import audio_recorder

# Page config
st.set_page_config(page_title="MediVoice - AI Appointment Assistant", layout="centered")

# Title and subtitle
st.title("🏥 MediVoice: AI Appointment Booking Assistant")
st.markdown("**Seamlessly book doctor appointments by speaking or filling out a form.**\n")

# Mode toggle
mode = st.radio("Choose your preferred method below:",["🎙️ Voice Input", "✍️ Fill Form"], horizontal=True)

# === Voice Input Mode ===
if mode == "🎙️ Voice Input":
    st.subheader("🎤 Speak Your Appointment Details")
    st.markdown("Click below and speak your full name, doctor name, date, time, and reason for visit.")

    # Record audio
    audio_bytes = audio_recorder(pause_threshold=2.0, sample_rate=44100)

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

        if st.button("Confirm Your Appointment"):
            with st.spinner("Transcribing and processing your appointment..."):
                try:
                    files = {"file": ("recording.wav", audio_bytes, "audio/wav")}
                    response = requests.post("http://localhost:8000/transcribe_audio/", files=files)

                    if response.ok:
                        data = response.json()
                        st.success("Appointment Details Extracted!")
                        st.write(f"**Transcription:** {data['transcription']}")
                        st.write(f"**Name:** {data['name']}")
                        st.write(f"**Doctor:** {data['doctor']}")
                        st.write(f"**Date:** {data['date']}")
                        st.write(f"**Time:** {data['time']}")
                        st.write(f"**Email:** {data['contact']}")
                        st.write(f"**Status:** {data['email_status']}")
                    else:
                        st.error("Transcription failed. Please try again.")
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

# === Fill Form Mode ===
elif mode == "✍️ Fill Form":
    st.subheader("📝 Manual Form Booking")
    st.markdown("Enter your details below to book your appointment:")

    with st.form("form_booking"):
        name = st.text_input("Full Name")
        doctor = st.text_input("Doctor Name")
        date = st.date_input("Appointment Date")
        time = st.time_input("Appointment Time")
        reason = st.text_area(" Reason for Visit")
        contact = st.text_input("Email")

        submitted = st.form_submit_button("Book Appointment")

    if submitted:
        payload = {
            "name": name,
            "doctor": doctor,
            "date": str(date),
            "time": str(time),
            "reason": reason,
            "email": contact
        }

        res = requests.get("https://n9t1ztj3h7.execute-api.us-east-1.amazonaws.com/V1", params=payload)

        if res.ok:
            st.success("Appointment booked and confirmation sent to your email!")
        else:
            st.error("Booking failed. Please check your details and try again.")