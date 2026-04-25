import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT.parent / ".env", override=False)

from api.chat import chat_bp  # noqa: E402
from services.agent_service import AgentService  # noqa: E402

app = Flask(__name__)
CORS(app)
app.register_blueprint(chat_bp)

_agent_service = AgentService()


@app.get('/api/health')
def healthcheck():
    return jsonify({'status': 'ok', 'foundry': _agent_service.status()}), 200


if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    app.run(host='127.0.0.1', port=port, debug=debug)
