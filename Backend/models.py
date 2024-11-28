from pymongo import MongoClient
from config import Config

def initialize_db(app):
    
    mongo_client = MongoClient(Config.MONGO_URI)
    app.mongo_client = mongo_client
    app.db = mongo_client[Config.DATABASE_NAME]

    # Set default prompts
    system_prompts_collection = app.db["system_prompts"]
    default_prompts = [
        {"content": "You are an expert assistant capable of solving any problem efficiently, providing clear, accurate, and concise information to achieve desired outcomes."},
        {"content": "Act as a knowledgeable and versatile advisor, adapting to any scenario to deliver actionable insights, solutions, and support."},
        {"content": "Be a reliable, resourceful, and creative problem solver, equipped to handle any task with clarity, precision, and professionalism."}
    ]

    if system_prompts_collection.count_documents({}) == 0:
        system_prompts_collection.insert_many(default_prompts)
