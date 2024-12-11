import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aes import _encrypt_body, decrypt_body



def envoyer_email_gmail(destinataire, sujet, message):
    expediteur = "ndismgl@gmail.com"
    mot_de_passe = "vdcbrpaclcwazpse"
    serveur_smtp = "smtp.gmail.com"
    port = 587


    message_chiffre = _encrypt_body(message)

    email = MIMEMultipart()
    email['From'] = expediteur
    email['To'] = destinataire
    email['Subject'] = sujet
    email.attach(MIMEText(message_chiffre, 'plain'))

    try:
        with smtplib.SMTP(serveur_smtp, port) as serveur:
            serveur.starttls()
            serveur.login(expediteur, mot_de_passe)
            serveur.send_message(email)
        print("Email envoyé avec succès!")
    except Exception as e:
        print(f"Erreur: {e}")


