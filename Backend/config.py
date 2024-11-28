import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    DATABASE_NAME = "task"
    GROQ_API_KEY = os.getenv("API_KEY")
    DEBUG = True

groq_client = Groq(api_key=Config.GROQ_API_KEY)