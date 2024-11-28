from flask import Blueprint, request, jsonify
from services import start_conversation, select_response, stop_conversation, continue_conversation


conversation_bp = Blueprint('conversation', __name__)

@conversation_bp.route('/start', methods=['POST'])
def start_conversation_route():
    user_input = request.json.get('user_input')
    return start_conversation(user_input)

@conversation_bp.route('/select', methods=['POST'])
def select_response_route():
    selected_index = request.json.get('selected_index')
    return select_response(selected_index)

@conversation_bp.route('/stop', methods=['POST'])
def stop_conversation_route():
    return stop_conversation()

@conversation_bp.route('/continue', methods=['POST'])
def continue_conversation_route():
    return continue_conversation()
