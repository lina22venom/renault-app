import streamlit as st
import pandas as pd
from hashlib import sha256
from datetime import date

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'ko_checks' not in st.session_state:
    st.session_state['ko_checks'] = []
if 'form_data' not in st.session_state:
    st.session_state['form_data'] = {}
if 'page' not in st.session_state:
    st.session_state['page'] = 1
if 'current_menu' not in st.session_state:
    st.session_state['current_menu'] = 'Accueil'

# Hardcoded username and password hash for simplicity
USERNAME = "admin"
PASSWORD_HASH = sha256("password123".encode()).hexdigest()

def authenticate(username, password):
    """Check username and hashed password."""
    return username == USERNAME and sha256(password.encode()).hexdigest() == PASSWORD_HASH

def logout():
    """Log out the current user."""
    st.session_state['authenticated'] = False
    st.session_state['page'] = 1
    st.session_state['current_menu'] = 'Accueil'
    st.experimental_rerun()

def draw_header():
    """Draw Renault Group header."""
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #FFA500; font-size: 50px; margin-bottom: -20px;">GROUP</h1>
            <h1 style="color: black; font-size: 50px;">RENAULT</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

def about_page():
    """Display About information."""
    draw_header()
    st.title("📖 À propos de cette application")
    st.markdown(
        """
        ## Objectif de l'application
        Cette application est conçue pour réduire les **temps d'arrêt** et les **délais de maintenance** en facilitant les contrôles rapides et efficaces des équipements de soudage.

        ### Fonctionnalités :
        - Analyse basée sur un formulaire pour le contrôle d'état des pinces de soudage.
        - Enregistrement automatique des vérifications KO (non conformes) avec plans d'action.
        - Page récapitulative facile à comprendre.

        ## Renault Usine Tanger
        **L'usine Renault Tanger** est l'une des installations de fabrication les plus avancées au monde. Réputée pour sa durabilité environnementale et son efficacité de production, l'usine joue un rôle clé dans les opérations mondiales de Renault.

        ### Points clés :
        - Zéro émission de carbone.
        - Processus hautement automatisés.
        - Technologies avancées de soudage et de peinture.

        ## Langue et droits d'auteur
        - **Langue** : L'application est principalement disponible en français, conformément à son environnement opérationnel.
        - **Droits d'auteur** : Renault Group © 2024.

        Pour toute question, veuillez contacter l'administrateur du système.
        """,
        unsafe_allow_html=True,
    )
    st.button("⬅️ Retour au menu", on_click=lambda: st.session_state.update({'current_menu': 'Accueil'}))

def contact_page():
    """Display contact/help information."""
    st.title("📞 Contact/Help")
    st.markdown(
        """
        ## Besoin d'aide ?
        Vous pouvez nous contacter via les informations suivantes :

        - **Email** : support@renaultapp.com
        - **Téléphone** : +212 600 000 000
        - **Adresse** : Renault Usine Tanger, Zone Industrielle, Tanger, Maroc

        Nous sommes disponibles du **lundi au vendredi** de **9h à 18h**.

        Merci de votre confiance !
        """,
        unsafe_allow_html=True,
    )

def login():
    """Display login form and authenticate user."""
    draw_header()
    st.title("🔒 Login")
    st.markdown("<h3 style='color: #2E86C1;'>Veuillez entrer vos identifiants :</h3>", unsafe_allow_html=True)
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter", help="Cliquez pour vous connecter"):
        if authenticate(username, password):
            st.session_state['authenticated'] = True
            st.success("Connexion réussie !")
            st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe invalide")

def main_app():
    """Main application content after login."""
    draw_header()
    st.title("📋 Fiche d’Analyse et Contrôle d’État de Pince de Soudage")
    st.markdown("<h4 style='color: #2874A6;'>Veuillez remplir le formulaire ci-dessous :</h4>", unsafe_allow_html=True)

    with st.form("fiche_form"):
        st.text_input("Nom", key="Nom")
        st.date_input("Date", key="Date")
        st.text_input("Robot", key="Robot")
        st.text_input("Post", key="Post")
        st.text_input("Ligne", key="Ligne")

        st.subheader("🔍 Vérifications")

        checks = [
            "Vérifier la bonne référence des électrodes",
            "Vérifier l'état des électrodes en fin de vie",
            "Vérifier la qualité de ragéage des électrodes (aspect, alignement) et référence de la fraise (face active)",
            "Vérifier la fréquence changement électrodes",
            "Vérifier la propreté de la fraise (Bourrage fraise, clipsage)",
            "Vérifier le sens de rotation roueuse",
            "Vérifier l'accostage des tôles et la propreté de la zone (Mastic, peinture, etc.)",
            "Vérifier la perpendicularité de la pince par rapport à la tôle au point de soudure",
            "Vérifier le débit d'eau (lecture sur le computer)",
            "Vérifier que l'extrémité du tube de refroidissement est coupée à un angle de 45°",
            "Contrôler Pression et Intensité",
            "Contrôler le programme soudeur par rapport à la fiche paramètre",
            "Contrôler la loi de déphasage par rapport à la fiche paramètre",
            "Vérifier les paramètres de ragéage des électrodes (Fréquence et paramètre rodage)"
        ]

        ko_checks = []
        for check in checks:
            if not st.checkbox(f" {check}", key=check):
                ko_checks.append(check)

        st.selectbox("Qui vérifie ?", ["FAB", "OP", "Maint"], key="Qui vérifie")

        suivant = st.form_submit_button("➡️ Suivant")

        if suivant:
            if ko_checks:
                st.session_state['ko_checks'] = ko_checks
                st.session_state['page'] = 2
                st.experimental_rerun()
            else:
                st.session_state['page'] = 3
                st.experimental_rerun()

def ko_form(ko_checks):
    """Form for KO checks."""
    draw_header()
    st.title("⚙️ Problèmes Identifiés")
    st.markdown("<h4 style='color: #D35400;'>Veuillez remplir les détails pour les vérifications marquées comme KO :</h4>", unsafe_allow_html=True)

    for check in ko_checks:
        st.subheader(f"🚩 Problème : {check}")
        st.text_area("Action à mettre en place", key=f"action_{check}")
        st.text_input("Pilote", key=f"pilote_{check}")
        st.date_input("Délai", key=f"delai_{check}")
        st.selectbox("État", ["En cours", "Terminé"], key=f"etat_{check}")
        st.text_input("Validation CA", key=f"validation_{check}")

    col1, col2 = st.columns(2)
    with col1:
        st.button("⬅️ Retour", on_click=lambda: st.session_state.update({'page': 1}))
    with col2:
        st.button("➡️ Suivant", on_click=lambda: st.session_state.update({'page': 3}))

def summary_page():
    """Summary page with submission confirmation."""
    draw_header()
    st.title("📊 Résumé du Formulaire")

    st.markdown("<h4 style='color: #27AE60;'>Informations Générales</h4>", unsafe_allow_html=True)
    general_data = {
        "Nom": st.session_state['form_data'].get('Nom', ''),
        "Date": st.session_state['form_data'].get('Date', ''),
        "Robot": st.session_state['form_data'].get('Robot', ''),
        "Post": st.session_state['form_data'].get('Post', ''),
        "Ligne": st.session_state['form_data'].get('Ligne', ''),
        "Qui vérifie": st.session_state['form_data'].get('Qui vérifie', ''),
    }
    general_df = pd.DataFrame([general_data])
    st.table(general_df)

    st.markdown("<h4 style='color: #E74C3C;'>Vérifications KO</h4>", unsafe_allow_html=True)
    ko_data = []
    for key, value in st.session_state['form_data'].items():
        if key.startswith("Action_"):
            check_name = key.split("Action_")[1]
            ko_data.append({
                "Vérification": check_name,
                "Action à mettre en place": value,
                "Pilote": st.session_state['form_data'].get(f'Pilote_{check_name}', ''),
                "Délai": st.session_state['form_data'].get(f'Délai_{check_name}', ''),
                "État": st.session_state['form_data'].get(f'État_{check_name}', ''),
                "Validation CA": st.session_state['form_data'].get(f'Validation_CA_{check_name}', ''),
            })
    if ko_data:
        ko_df = pd.DataFrame(ko_data)
        st.table(ko_df)
    else:
        st.write("Aucune vérification KO trouvée.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("⬅️ Retour", on_click=lambda: st.session_state.update({'page': 1}))
    with col2:
        st.button("✔️ Soumettre", on_click=lambda: st.success("Formulaire soumis avec succès !"))
    with col3:
        st.button("🔓 Déconnexion", on_click=logout)

# Sidebar menu
with st.sidebar:
    draw_header()
    menu_option = st.radio("Navigation :", ("Accueil", "À propos", "Contact/Help"))
    st.session_state['current_menu'] = menu_option

# Navigation logic
if st.session_state['current_menu'] == "À propos":
    about_page()
elif st.session_state['current_menu'] == "Contact/Help":
    contact_page()
elif st.session_state['current_menu'] == "Accueil":
    if st.session_state['authenticated']:
        if st.session_state['page'] == 1:
            main_app()
        elif st.session_state['page'] == 2:
            ko_form(st.session_state['ko_checks'])
        elif st.session_state['page'] == 3:
            summary_page()
    else:
        login()
