import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()



password = os.getenv("password_correo")

def EnviarCorreo(email_reciver,nombre):

    email_sender = os.getenv("email_sender")

    subject = "📩 ¡Verificación de Registro Exitosa!"

    body = f"""
    ¡Hola! 👋

        Hermano/a {nombre} nos complace informarte que tu usuario ha sido creado exitosamente. 🎉

        🔹 Para acceder, usa tu número de documento.
        ❓ Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.

        📖 "Todo lo que hagan, háganlo con amor." – 1 Corintios 16:14

        ¡Bendiciones! ✨

        Celulas Iglesia Betel ⛪
    """
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_reciver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_reciver, em.as_string())
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
   