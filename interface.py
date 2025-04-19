
import gradio as gr
from chatbot_logic_gpt_db import get_response, add_to_db, search_faq
from dotenv import load_dotenv
import os

load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
authentifie = False

def login(username, password):
    global authentifie
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        authentifie = True
        return "✅ Connecté avec succès."
    return "❌ Identifiants incorrects."

def ajouter_faq(question, answer):
    if authentifie:
        add_to_db(question, answer)
        return "Ajouté à la base de données !"
    return "Non autorisé."

def recherche_faq(question):
    results = search_faq(question)
    return "\n".join([f"Q: {q}\nR: {a}" for q, a in results]) if results else "Aucune correspondance trouvée."

with gr.Blocks(title="Assistant Entreprise") as demo:
    gr.Markdown("## 🤖 Assistant d'Entreprise")

    with gr.Tab("💬 Chatbot"):
        user_input = gr.Textbox(label="Votre question")
        reponse = gr.Textbox(label="Réponse", interactive=False)
        send = gr.Button("Envoyer")
        send.click(get_response, inputs=user_input, outputs=reponse)

    with gr.Tab("🔍 Rechercher dans la FAQ"):
        recherche = gr.Textbox(label="Mot-clé")
        resultats = gr.Textbox(label="Résultats", lines=10, interactive=False)
        rechercher = gr.Button("Rechercher")
        rechercher.click(recherche_faq, inputs=recherche, outputs=resultats)

    with gr.Tab("🔒 Ajouter à la FAQ (admin)"):
        login_user = gr.Textbox(label="Utilisateur")
        login_pass = gr.Textbox(label="Mot de passe", type="password")
        login_btn = gr.Button("Connexion")
        login_status = gr.Textbox(label="", interactive=False)
        login_btn.click(login, inputs=[login_user, login_pass], outputs=login_status)

        with gr.Column(visible=False) as admin_zone:
            q = gr.Textbox(label="Question")
            a = gr.Textbox(label="Réponse")
            ajout = gr.Button("Ajouter")
            ajout_status = gr.Textbox(label="", interactive=False)
            ajout.click(ajouter_faq, inputs=[q, a], outputs=ajout_status)

        def toggle_admin(status):
            return gr.update(visible=status.startswith("✅"))

        login_status.change(toggle_admin, inputs=login_status, outputs=admin_zone)

demo.launch()
