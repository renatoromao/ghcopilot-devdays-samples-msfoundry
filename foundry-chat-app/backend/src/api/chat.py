from flask import Blueprint, request, jsonify

from services.agent_service import AgentService
from services.chat_service import ChatService

chat_bp = Blueprint('chat', __name__)

agent_service = AgentService()
chat_service = ChatService(agent_service=agent_service, foundry_client=agent_service.client)


@chat_bp.route('/api/agents', methods=['POST'])
def create_agent():
    try:
        agent = agent_service.get_or_create_agent()
        return jsonify({'agent': agent, 'status': agent_service.status()}), 200
    except Exception as exc:  # noqa: BLE001
        return jsonify({'error': str(exc), 'status': agent_service.status()}), 500


@chat_bp.route('/api/chat', methods=['POST'])
@chat_bp.route('/api/chat/send', methods=['POST'])
def send_message():
    data = request.get_json(silent=True) or {}
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        messages = chat_service.send_message(user_message)
        return jsonify({'messages': messages, 'status': agent_service.status()}), 200
    except Exception as exc:  # noqa: BLE001
        return jsonify({'error': str(exc), 'status': agent_service.status()}), 500


@chat_bp.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    try:
        history = chat_service.receive_messages()
        return jsonify({'messages': history, 'status': agent_service.status()}), 200
    except Exception as exc:  # noqa: BLE001
        return jsonify({'error': str(exc), 'status': agent_service.status()}), 500


@chat_bp.route('/api/chat/reset', methods=['POST'])
def reset_chat():
    chat_service.reset()
    return jsonify({'messages': [], 'status': agent_service.status()}), 200
