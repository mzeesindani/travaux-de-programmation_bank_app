
import streamlit as st
import sqlite3

def  create_database():
    conn = sqlite3.connect('bank_app.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL, 
    password TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS bank_accounts 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INTEGER, 
    account_number TEXT NOT NULL,
    balance REAL, FOREIGN KEY (user_id) REFERENCES users (id))''')

    conn.commit()
    conn.close()



def create_connection():

    conn = sqlite3.connect('bank_app.db')
    return conn

def authenticate(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username))
    result = c.fetchone()
    conn.close()
    return result is not None




def login_page():
    st.title("Authentification")

    usernam = st.text_input("Nom d'utilisateur_")

    if st.button("Se connecter"):
        if usernam:

            if authenticate(usernam):
                st.success("Authentification réussie. Redirection vers la page principale...")
                # Redirection vers la page principale
                main_page()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")
        else:
            st.write("veillez saisir le nom et le mot de pass")
    else:
        st.write("le bouton a un probleme")








def create_account(username, password):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        conn.rollback()
        conn.close()
        return False



def create_account_page():
    st.title("Créer un compte")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Créer le compte"):
        if username and password:
            if create_account(username, password):

                st.success("Compte créé avec succès. Vous pouvez maintenant vous connecter.")

                #login_page()
            else:
                st.error("Erreur lors de la creation du compte. Veuillez réessayer")
        else:
            st.error("Veuillez saisir un nom d'utilisateur et un mot de passe")

    st.write("Déja un compte ?")
    if st.button("S'authentifier"):
        login_page()


def create_bank_account(user_id, account_number):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO bank_accounts (user_id, account_number, balance) VALUES (?, ?, 0.0)", (user_id, account_number))
        conn.commit()
        conn.close()
        return  True
    except sqlite3.Error:
        conn.rollback()
        conn.close()
        return False

def main():
    login_page()
    create_database()
def main_page():
    st.write("vous pouvez creer maintenant un compte bancaire")
if __name__ == "__main__":
    main()
