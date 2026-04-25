# Foundry Chat Application

This project is a chat application that interacts with the Microsoft Foundry API. It consists of a backend built with Python and Flask, and a frontend developed using React and TypeScript.

## Project Structure

```
foundry-chat-app
├── backend
│   ├── src
│   │   ├── app.py                # Entry point of the backend application
│   │   ├── api
│   │   │   └── chat.py           # API endpoints for chat interactions
│   │   ├── services
│   │   │   ├── auth.py           # Authentication functions
│   │   │   ├── foundry_client.py  # Client for interacting with Foundry API
│   │   │   ├── agent_service.py   # Logic for managing agents
│   │   │   └── chat_service.py    # Chat-related functionalities
│   │   └── models
│   │       └── schemas.py        # Data models and schemas
│   ├── requirements.txt          # Python dependencies
│   └── pyproject.toml            # Project configuration
├── frontend
│   ├── src
│   │   ├── App.tsx               # Main component of the frontend application
│   │   ├── components
│   │   │   ├── ChatWindow.tsx     # Chat window component
│   │   │   ├── MessageList.tsx     # Component for rendering messages
│   │   │   └── MessageInput.tsx    # Component for user input
│   │   └── services
│   │       └── api.ts            # API call functions
│   ├── package.json              # Frontend configuration
│   └── tsconfig.json             # TypeScript configuration
├── .env.example                   # Example environment variables
└── README.md                     # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd foundry-chat-app
   ```

2. **Backend Setup:**
   - Navigate to the `backend` directory.
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the backend application:
     ```bash
     python src/app.py
     ```

3. **Frontend Setup:**
   - Navigate to the `frontend` directory.
   - Install the required Node.js packages:
     ```bash
     npm install
     ```
   - Start the frontend application:
     ```bash
     npm start
     ```

## Usage

- The chat application allows users to send and receive messages in real-time.
- The backend handles authentication and manages chat interactions through the Microsoft Foundry API.
- Ensure that you have the necessary Azure credentials set up in the `.env` file.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.