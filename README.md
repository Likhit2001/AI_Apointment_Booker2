# 🩺 MediVoice: AI Appointment Booking Assistant

![App Preview](./screenshots/voice_input.png)

MediVoice lets users book medical appointments either by **voice input** or a **manual form**. You speak your appointment details, and the app transcribes and parses the info to schedule an appointment and sends confirmation via email.

---

## ✨ Features

- 🎤 **Voice Input**: Speak your full name, doctor name, date, time, reason for visit, and email.
- 📝 **Form Input**: Manual form filler for traditional users.
- 🤖 **Speech-to-Text**: Uses OpenAI Whisper for transcription.
- 🧠 **LLM-Based Parsing**: Leverages LangChain, LangGraph, and ChatGroq to extract structured appointment info.
- 📧 **Email Confirmations**: Sends confirmation emails via AWS SES.
- 🐳 **Dockerized**: Frontend (Streamlit) and Backend (FastAPI) are containerized.
- 🚀 **One-Command Deployment**: Fully launchable via `docker-compose up`.

---

## 🖼️ Screenshots

**Voice Input Mode**  
![Voice Input](./screenshots/voice_input.png)

**Form Input & Confirmation**  
![Form Input](./screenshots/form_booking.png)

**Email Confirmation Received**  
![Email Sent](./screenshots/email.png)

---

## 🛠️ Tech Stack

| Component      | Technology |
|----------------|------------|
| Frontend       | Streamlit  |
| Backend        | FastAPI    |
| Speech-to-Text | OpenAI Whisper |
| LLM Parsing    | LangChain + LangGraph + ChatGroq |
| Email Service  | AWS SES    |
| Containerization | Docker & Docker Compose |

---

## 🚀 Quick Start

Follow these steps to run the app locally or via Docker:

### 1. Clone the repo

```bash
git clone https://github.com/your-username/medivoice-app.git
cd medivoice-app
```

### 2. Add your API key

Create a `.env` file in the repo root:

```env
GROQ_API_KEY=your-groq-api-key
```

### 3. Launch with Docker Compose

```bash
docker-compose up --build
```

- Frontend → http://localhost:8501  
- Backend Docs → http://localhost:8000/docs

You can alternate voice/form input and receive email confirmations.

---

## 🐳 Use Prebuilt Docker Images

Skip local builds and use the public Docker images:

```yaml
services:
  backend:
    image: kotho2001/voice-backend:latest
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}

  frontend:
    image: kotho2001/voice-frontend:latest
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
```

Then run:

```bash
cp .env.example .env
docker-compose up
```

---

## 📬 Email Delivery (AWS SES)

To enable email functionality:

1. Set up and verify your sender email in AWS SES.
2. Verify recipient email if you're in SES sandbox mode.
3. Credentials are already configured in the backend to send confirmations.

---

## 🛡️ Security Setup

- API keys are stored in `.env` and accessed via `docker-compose`.
- `.env` should be listed in `.gitignore` to avoid accidental publishing.

---

## 🧑‍💻 Contributors

- **Likhit Kothapalli** – Project Creator & Lead Developer

---

## 📄 License

This project is licensed under the **MIT License**.

---

**Enjoy using MediVoice?** If you find it helpful, feel free to ⭐ the repository!
