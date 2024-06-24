from flask import Flask, request, jsonify, render_template, send_from_directory
import mysql.connector
from mysql.connector import Error
from difflib import SequenceMatcher
import string
import requests

app = Flask(__name__)



def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def get_best_response(question, responses):
    question = normalize_text(question)
    best_match = None
    highest_similarity = 0.0
    
    for response in responses:
        response_text = response.get("text", "")
        normalized_response_text = normalize_text(response_text)
        similarity = SequenceMatcher(None, question, normalized_response_text).ratio()
        
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = response_text
    
    threshold = 0.6
    if best_match and highest_similarity > threshold:
        return best_match
    else:
        return "Je suis désolé, je n'ai pas la réponse à cette question."

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/chat')
def serve_chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"


    try:
        response = requests.post(rasa_url, json={"sender": "user", "message": question})
        if response.ok:
            responses = response.json()
            messages = [r["text"] for r in responses if "text" in r]
            return jsonify({"response": messages})
        else:
            return jsonify({"response": ["Désolé, une erreur est survenue."]})
    except Exception as e:
        return jsonify({"response": [f"Erreur de communication avec le serveur Rasa: {str(e)}"]})

    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
