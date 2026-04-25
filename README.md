# GitHub Copilot DevDays — Microsoft Foundry samples

Sample full-stack chat application that connects a React frontend to a Python (Flask) backend, which in turn talks to a **Microsoft Foundry** agent through the Azure AI Agents SDK.

Built live during the **GitHub Copilot DevDay (São José dos Campos)** to showcase how Copilot can scaffold and evolve a real Foundry-powered app.

---

## Repository layout

```
.
├── .gitignore
└── foundry-chat-app/
    ├── .env.example          # Copy to .env and fill in your Foundry values
    ├── README.md             # App-specific docs
    ├── backend/              # Flask API + Foundry SDK integration
    │   ├── requirements.txt
    │   └── src/
    │       ├── app.py
    │       ├── api/chat.py
    │       └── services/
    │           ├── agent_service.py
    │           ├── chat_service.py
    │           └── foundry_client.py
    └── frontend/             # React + TypeScript UI
        ├── package.json
        └── src/
            ├── App.tsx
            ├── components/
            └── services/api.ts
```

## Architecture

```
Browser  ──>  React (CRA, port 3001)  ──>  Flask API (port 5000)  ──>  Microsoft Foundry agent
```

- The backend uses `azure-ai-agents` (`AgentsClient`) and `DefaultAzureCredential`.
- It either looks up an existing agent (`FOUNDRY_AGENT_ID`) or creates one from a model deployment (`FOUNDRY_MODEL_DEPLOYMENT`).
- A single chat thread is created per process; `/api/chat/reset` starts a new conversation.
- If no Foundry env vars are set, the backend falls back to a local "echo" mode for offline development.

## Prerequisites

- Python 3.11+ and a virtual environment
- Node.js 18+ (the dev server runs with `NODE_OPTIONS=--openssl-legacy-provider` for Node 22 compatibility)
- Azure CLI and an Azure account with access to a **Microsoft Foundry / Azure AI Projects** resource — `az login`

## Quick start

```bash
git clone https://github.com/renatoromao/ghcopilot-devdays-samples-msfoundry.git
cd ghcopilot-devdays-samples-msfoundry

# 1) Configure environment
cp foundry-chat-app/.env.example foundry-chat-app/.env
# Edit foundry-chat-app/.env and set AZURE_AI_PROJECT_ENDPOINT and FOUNDRY_MODEL_DEPLOYMENT (or FOUNDRY_AGENT_ID)

# 2) Authenticate to Azure
az login

# 3) Backend
python -m venv .venv
source .venv/bin/activate
pip install -r foundry-chat-app/backend/requirements.txt
python foundry-chat-app/backend/src/app.py
# → http://127.0.0.1:5000

# 4) Frontend (in a second terminal)
cd foundry-chat-app/frontend
npm install
NODE_OPTIONS=--openssl-legacy-provider PORT=3001 npm start
# → http://localhost:3001
```

The status pill in the header shows **Connected to Foundry** when the env vars are valid, or **Local mode** when running offline.

## API endpoints

| Method | Path                | Description                              |
| ------ | ------------------- | ---------------------------------------- |
| GET    | `/api/health`       | Health + Foundry config status           |
| POST   | `/api/agents`       | Get-or-create the Foundry agent          |
| POST   | `/api/chat/send`    | Send a message and get the thread back   |
| GET    | `/api/chat/history` | Return the current thread messages       |
| POST   | `/api/chat/reset`   | Start a new thread / clear local history |

## Environment variables

See [foundry-chat-app/.env.example](foundry-chat-app/.env.example). Key variables:

- `AZURE_AI_PROJECT_ENDPOINT` — required, e.g. `https://<resource>.services.ai.azure.com/api/projects/<project>`
- `FOUNDRY_AGENT_ID` — optional, real agent id like `asst_xxx`
- `FOUNDRY_MODEL_DEPLOYMENT` — used to create an agent on the fly when no agent id is provided
- `AGENT_NAME`, `AGENT_DESCRIPTION`, `AGENT_INSTRUCTIONS` — applied when creating an agent

`.env` is git-ignored — never commit secrets.

## License

Sample code, MIT-style — use freely for learning and demos.
