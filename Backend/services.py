from bson import ObjectId
from flask import jsonify
from flask import current_app
from config import groq_client
conversation_log = []

# prompts updates
def get_prompts():
    db = current_app.db
    system_prompts_collection = db["system_prompts"]
    prompts = list(system_prompts_collection.find({}, {"_id": 1, "content": 1}))
    for prompt in prompts:
        prompt["_id"] = str(prompt["_id"])
    return jsonify({"prompts": prompts})

def add_prompt(new_prompt):
    if not new_prompt:
        return jsonify({"error": "Prompt content is required."}), 400

    db = current_app.db
    system_prompts_collection = db["system_prompts"]
    result = system_prompts_collection.insert_one({"content": new_prompt})
    prompt = {"_id": str(result.inserted_id), "content": new_prompt}
    return jsonify({"message": "Prompt added.", "prompt": prompt})

def edit_prompt(prompt_id, updated_content):
    if not updated_content:
        return jsonify({"error": "Updated content is required."}), 400

    db = current_app.db
    system_prompts_collection = db["system_prompts"]
    result = system_prompts_collection.update_one(
        {"_id": ObjectId(prompt_id)},
        {"$set": {"content": updated_content}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Prompt not found."}), 404

    return jsonify({"message": "Prompt updated.", "id": prompt_id, "content": updated_content})

def delete_prompt(prompt_id):
    db = current_app.db
    system_prompts_collection = db["system_prompts"]
    result = system_prompts_collection.delete_one({"_id": ObjectId(prompt_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Prompt not found."}), 404

    return jsonify({"message": "Prompt deleted.", "id": prompt_id})




# for conversation
def generate_responses(user_input, system_prompts):
    responses = []
    for system_prompt in system_prompts:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

   
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.2,
            max_tokens=100,
            top_p=1,
            stream=False
        )
        response_content = completion.choices[0].message.content
        responses.append(response_content)
    return responses

def start_conversation(user_input):
    if not user_input:
        return jsonify({"error": "user_input is required."}), 400

    db = current_app.db
    system_prompts_collection = db["system_prompts"]
    system_prompts = [prompt["content"] for prompt in system_prompts_collection.find({}, {"_id": 0, "content": 1})]

    responses = generate_responses(user_input, system_prompts)
    conversation_entry = {
        "user_input": user_input,
        "system_prompts": system_prompts,
        "response_options": responses,
        "chosen_response": None
    }
    conversation_log.append(conversation_entry)

    return jsonify({"responses": responses, "message": "Responses generated."})

def select_response(selected_index):
    if selected_index is None:
        return jsonify({"error": "selected_index is required."}), 400

    if not conversation_log or "response_options" not in conversation_log[-1]:
        return jsonify({"error": "No responses available to select from."}), 400

    try:
        selected_response = conversation_log[-1]["response_options"][selected_index]
        conversation_log[-1]["chosen_response"] = selected_response
        return jsonify({"message": "Response selected.", "chosen_response": selected_response})
    except IndexError:
        return jsonify({"error": "Invalid selected_index."}), 400

def stop_conversation():
    db = current_app.db
    conversations_collection = db["conversations"]
    global conversation_log
    mongo_result = conversations_collection.insert_one({"conversation": conversation_log})
    conversation_log = []
    return jsonify({
        "message": "Conversation ended and saved to MongoDB as JSON.",
        "mongo_id": str(mongo_result.inserted_id)
    })

def continue_conversation():
    return jsonify({"message": "Conversation ongoing. You can send more user input."})