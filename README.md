# Emotion Platform (MVP Skeleton)

This repository contains a minimal skeleton for the emotion recognition platform:

- `backend/`: FastAPI API with stubbed auth, submissions, and admin endpoints.
- `admin/`: React admin UI (Vite) that calls the admin submissions endpoint.
- `mobile/`: React Native placeholder app.
- `docs/`: Architecture, product plan, and handover notes.
- `.devcontainer/`: GitHub Codespaces configuration for Python + Node.

## Getting Started in Codespaces

1. Open this repo in GitHub Codespaces.
2. In one terminal:

   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. In another terminal:

   ```bash
   cd admin
   npm install
   npm run dev
   ```

Backend will be available on port 8000; admin on port 3000 (both forwarded by Codespaces).
