# 🩺 MediVoice: AI Appointment Booking Assistant

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

**Voice Input Voice Mode**  
![Voice Input] <img width="759" alt="Screenshot 2025-07-04 at 3 53 18 AM" src="https://github.com/user-attachments/assets/1d3efb50-af6d-4ad5-8154-c5245a68d2cd" />

**Form Input & Confirmation**  
![Form Input] <img width="996" alt="Screenshot 2025-07-04 at 3 54 32 AM" src="https://github.com/user-attachments/assets/ab2d3651-c90c-49b9-a38f-c9ca6cf9719e" />

**Email Confirmation Received**  
![Email Sent] <img width="1012" alt="Screenshot 2025-07-04 at 3 55 28 AM" src="https://github.com/user-attachments/assets/758ac590-d572-45b3-b28f-572ec15d5f6c" />


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
**Enjoy using MediVoice?** If you find it helpful, feel free to ⭐ the repository!
