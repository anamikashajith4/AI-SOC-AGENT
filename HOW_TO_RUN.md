# How to Run This Project (Every Time)

## 1. Open project in VS Code
File → Open Folder → ai-soc-agent

## 2. Start Backend (Terminal 1)

cd C:\Users\LOQ\OneDrive\Desktop\ai-soc-agent
.\venv\Scripts\Activate.ps1
cd backend
uvicorn main:app --reload

Wait for: "Uvicorn running on http://127.0.0.1:8000"

## 3. Start Frontend (Terminal 2 - click + for new terminal)
cd C:\Users\LOQ\OneDrive\Desktop\ai-soc-agent\frontend
npm run dev

Wait for: "Local: http://localhost:5173"

## 4. Open browser
Go to: http://localhost:5173

## Notes
- Both terminals must stay open and running while you work
- To stop a server: click in that terminal, press Ctrl+C
- If anything breaks, close VS Code fully and repeat steps 1-4