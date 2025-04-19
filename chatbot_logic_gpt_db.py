import sqlite3
import os
from openai import OpenAI

# 🔑 Initialise le client OpenAI avec la clé API depuis les variables d’environnement
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📦 Connexion à la base SQLite
conn = sqlite3.connect("faq.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS faq (
    question TEXT,
    answer TEXT
)
""")
conn.commit()

# 🔍 Cherche une réponse dans la BDD
def get_answer_from_db(question):
    cursor.execute("SELECT answer FROM faq WHERE question LIKE ?", ('%' + question + '%',))
    result = cursor.fetchone()
    return result[0] if result else None

# ➕ Ajoute une nouvelle Q/R
def add_to_db(question, answer):
    cursor.execute("INSERT INTO faq (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()

# 🤖 Logique du chatbot
def get_response(user_input):
    answer = get_answer_from_db(user_input)
    if answer:
        return answer

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant professionnel pour une entreprise."},
                {"role": "user", "content": user_input}
            ]
        )
        gpt_answer = response.choices[0].message.content.strip()
        add_to_db(user_input, gpt_answer)
        return gpt_answer
    except Exception as e:
        if "insufficient_quota" in str(e):
            return "🚫 GPT : Vous avez dépassé votre quota d’utilisation. Veuillez vérifier votre abonnement sur platform.openai.com."
        return f"Erreur GPT : {str(e)}"

def search_faq(question):
    cursor.execute("SELECT question, answer FROM faq WHERE question LIKE ?", ('%' + question + '%',))
    results = cursor.fetchall()
    return results

