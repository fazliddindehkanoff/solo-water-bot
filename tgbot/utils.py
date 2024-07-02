import requests
from src.settings import API_TOKEN

TELEGRAM_API_BASE_URL = f"https://api.telegram.org/bot{API_TOKEN}"


def send_message(chat_id, text):
    url = f"{TELEGRAM_API_BASE_URL}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text,
    }
    try:
        response = requests.post(url, json=params)
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
