import requests
import json
import os
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from models.auth import Auth


def enviar_notificacion(usuario_id, title, body):
    auth = Auth()
    tokens = auth.obtener_token_usuario(usuario_id)
    if not tokens:
        return False

    service_account_path = _obtener_ruta_service_account()
    if not os.path.isfile(service_account_path):
        raise FileNotFoundError(
            f"Archivo de service account no encontrado: {service_account_path}"
        )

    access_token = _obtener_access_token(service_account_path)
    project_id = _obtener_project_id(service_account_path)

    for token_row in tokens:
        _enviar_mensaje(access_token, project_id, token_row['token'], title, body)

    return True


def _obtener_ruta_service_account():
    return os.path.join(os.getcwd(), "firebase", "service-account-file.json")


def _obtener_access_token(service_account_path):
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    credentials = service_account.Credentials.from_service_account_file(
        service_account_path, scopes=SCOPES
    )
    credentials.refresh(Request())
    return credentials.token


def _obtener_project_id(service_account_path):
    with open(service_account_path) as f:
        data = json.load(f)
    return data.get('project_id', 'medical-app')


def _enviar_mensaje(access_token, project_id, device_token, title, body):
    FCM_URL = f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }
    payload = {
        'message': {
            'token': device_token,
            'notification': {
                'title': title,
                'body': body,
            }
        }
    }
    response = requests.post(FCM_URL, headers=headers, json=payload)
    return response.ok
