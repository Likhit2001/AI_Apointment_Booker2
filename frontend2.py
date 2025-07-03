import streamlit as st
import requests
from audio_recorder_streamlit import audio_recorder
from datetime import date, time

st.set_page_config(page_title="Smart Appointment Booking Assistant", layout="centered")
st.title("🏥 Smart Appointment Booking Assistant")

# === Input Method Selection ===
mode = st.radio("Choose your preferred method:", ["🎙️ Voice Input", "✍️ Fill Form"], horizontal=True)

# === Voice Input Mode ===
if mode == "🎙️ Voice Input":
    st.subheader("🎤 Speak your appointment details")
    audio_bytes = audio_recorder(pause_threshold=2.0, sample_rate=44100)

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

        if st.button("🚀 Submit to AI Agent"):
            with st.spinner("📡 Uploading and Processing..."):
                files = {"file": ("recording.wav", audio_bytes, "audio/wav")}
                response = requests.post("http://localhost:8000/transcribe_audio/", files=files)

                if response.ok:
                    data = response.json()
                    st.success("✅ Appointment Information Extracted:")
                    st.markdown(f"- **Transcription:** {data['transcription']}")
                    st.markdown(f"- **Name:** {data['name']}")
                    st.markdown(f"- **Doctor:** {data['doctor']}")
                    st.markdown(f"- **Date:** {data['date']}")
                    st.markdown(f"- **Time:** {data['time']}")
                    st.markdown(f"- **Reason:** {data['reason']}")
                    st.markdown(f"- **Contact:** {data['contact'] or 'Not mentioned'}")
                    st.markdown(f"- **Email Status:** {data['email_status']}")
                else:
                    st.error("❌ Error during transcription or information extraction.")

# === Manual Form Input Mode ===
elif mode == "✍️ Fill Form":
    st.subheader("📝 Enter Appointment Details")

    with st.form("appointment_form"):
        name = st.text_input("Full Name")
        doctor = st.text_input("Doctor Name")
        appointment_date = st.date_input("Date", value=date.today())
        appointment_time = st.time_input("Time")
        reason = st.text_area("Reason for Visit")
        email = st.text_input("Contact Email")

        submit = st.form_submit_button("✅ Book Appointment")

    if submit:
        payload = {
            "name": name,
            "doctor": doctor,
            "date": str(appointment_date),
            "time": str(appointment_time),
            "reason": reason,
            "email": email
        }

        st.info("⏳ Sending to backend...")
        response = requests.get("https://n9t1ztj3h7.execute-api.us-east-1.amazonaws.com/V1", params=payload)

        if response.ok:
            st.success("🎉 Appointment booked and email confirmation sent!")
        else:
            st.error("❌ Booking failed. Please check your details or try again later.")