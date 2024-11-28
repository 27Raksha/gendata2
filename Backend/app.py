from flask import Flask
from flask_cors import CORS
from models import initialize_db
from routes.conversation_routes import conversation_bp
from routes.prompt_routes import prompt_bp

# Initialize Flask App
app = Flask(__name__)
CORS(app)


initialize_db(app)


app.register_blueprint(conversation_bp)
app.register_blueprint(prompt_bp)

@app.route('/')
def home():
    return "Welcome to the Modularized Flask API!"

if __name__ == '__main__':
    app.run(debug=True)
