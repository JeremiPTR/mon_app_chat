import streamlit as st
import pandas as pd
import os


# Chargement des utilisateurs
def load_users():
    return pd.read_csv("users.csv")


def save_users(df):
    df.to_csv("users.csv", index=False)


def authenticate(username, password, users_df):
    user = users_df[users_df["name"] == username]
    if not user.empty:
        if user.iloc[0]["password"] == password:
            return True
    return False


# Authentification
def login():
    st.title("Page de connexion")
    users = load_users()

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    login_button = st.button("Se connecter")

    if login_button:
        if authenticate(username, password, users):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[users["name"] == username].iloc[0]["role"]
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")


# Galerie d’images
def display_gallery():
    st.header("Album Photo 🐱")
    image_dir = "images"
    image_files = [
        f for f in os.listdir(image_dir) if f.endswith((".png", ".jpg", ".jpeg"))
    ]

    cols = st.columns(3)
    for idx, img in enumerate(image_files):
        with cols[idx % 3]:
            st.image(os.path.join(image_dir, img), use_column_width=True)


# Accueil
def home():
    st.header("Bienvenue 🏠")
    st.write("Vous êtes connecté en tant que :", st.session_state.username)


# Menu latéral
def sidebar():
    with st.sidebar:
        st.success(f"Bienvenue {st.session_state.username} 👋")
        page = st.radio("Navigation", ["Accueil", "Album Photo", "Déconnexion"])
        return page


# App principale
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        page = sidebar()

        if page == "Accueil":
            home()
        elif page == "Album Photo":
            display_gallery()
        elif page == "Déconnexion":
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()


if __name__ == "__main__":
    main()
