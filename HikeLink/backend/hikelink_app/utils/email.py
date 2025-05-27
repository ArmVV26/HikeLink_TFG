import os, logging
import requests
from django.template.loader import render_to_string

def send_welcome_email(to_email, full_name):
    logger = logging.getLogger(__name__)
    
    html_content = render_to_string('emails/welcome_email.html', {
        'full_name': full_name,
        'year': 2025
    })

    api_key = os.getenv("BREVO_API_KEY")
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {"name": "HikeLink", "email": "hikelink.notifications@gmail.com"},
        "to": [{"email": to_email}],
        "subject": "¡Bienvenido a HikeLink!",
        "htmlContent": html_content
    }

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except Exception as e:
        logger.critical(f"Error al enviar el correo por API: {e}")
