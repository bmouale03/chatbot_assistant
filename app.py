from flask import Flask, render_template, request, jsonify, redirect, session
from chatbot_logic_gpt_db import get_response


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["message"]
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session


app.secret_key = 'ton_secret_key'  # Nécessaire pour utiliser `session`

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            reponse = "Réponse fictive à : " + question
            session['chat_history'].append(('Vous', question))
            session['chat_history'].append(('Bot', reponse))
            session.modified = True

    return render_template('chat.html', chat_history=session['chat_history'])

@app.route('/refresh', methods=['POST'])
def refresh():
    session['chat_history'] = []
    return redirect('/')
