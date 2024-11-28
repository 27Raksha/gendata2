from flask import Blueprint, request, jsonify
from services import get_prompts, add_prompt, edit_prompt, delete_prompt


prompt_bp = Blueprint('prompt', __name__)

@prompt_bp.route('/prompts', methods=['GET'])
def get_prompts_route():
    return get_prompts()

@prompt_bp.route('/prompts', methods=['POST'])
def add_prompt_route():
    new_prompt = request.json.get('content')
    return add_prompt(new_prompt)

@prompt_bp.route('/prompts/<string:prompt_id>', methods=['PUT'])
def edit_prompt_route(prompt_id):
    updated_content = request.json.get('content')
    return edit_prompt(prompt_id, updated_content)

@prompt_bp.route('/prompts/<string:prompt_id>', methods=['DELETE'])
def delete_prompt_route(prompt_id):
    return delete_prompt(prompt_id)
