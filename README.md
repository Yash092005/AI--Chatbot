# AI Chatbot for Water Conservation Awareness

This repository is a submission-ready student project implementing a multilingual chatbot (English/Hindi/Marathi) to promote water conservation. It contains a simple FastAPI backend, a minimal React frontend, a knowledge base, and a SQLite schema.

## Quick start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# create sqlite DB
sqlite3 ../database.sqlite < ../database.sql
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open the frontend at http://localhost:5173 (Vite default) and ensure backend runs at http://localhost:8000

