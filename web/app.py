from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/chat')
def serve_chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    if question:
        response = requests.post(
            'http://localhost:5005/webhooks/rest/webhook',
            json={"sender": "user", "message": question}
        )
        response_json = response.json()
        if response_json:
            answer = response_json[0].get('text')
            return jsonify({'response': answer})
    return jsonify({'response': "Désolé, je n'ai pas compris la question."})

if __name__ == '__main__':
    app.run(debug=True)
