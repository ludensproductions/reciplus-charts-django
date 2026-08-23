import os.path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    """Gets the Gmail API service."""
    creds = None

    # Detectar si estamos en Jenkins
    USE_JENKINS_PATH = os.environ.get("GMAIL_TOKEN_JENKINS_PATH_FLAG", "False").lower() == "true"
    token_file = "/tmp/token.json" if USE_JENKINS_PATH else os.path.join(os.path.dirname(__file__), "token.json")

    # Cargar credenciales si existen
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # Si no hay credenciales válidas, intentar refrescar o abrir flujo local (solo fuera de Jenkins)
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refrescando token con refresh_token...")
                creds.refresh(Request())
            else:
                if USE_JENKINS_PATH:
                    raise Exception("Token inválido en Jenkins. No se puede abrir navegador para autenticación.")
                else:
                    print("🌐 Abriendo navegador para autenticación...")
                    client_secrets_file = os.path.join(os.path.dirname(__file__), "credentials.json")
                    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                    creds = flow.run_local_server(port=0)
        except RefreshError as e:
            if USE_JENKINS_PATH:
                raise Exception(f"❌ Error al refrescar token en Jenkins: {e}")
            else:
                print("⚠️ No se pudo refrescar el token, iniciando flujo manual...")
                client_secrets_file = os.path.join(os.path.dirname(__file__), "credentials.json")
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                creds = flow.run_local_server(port=0)

        # Guardar token actualizado (ya sea local o Jenkins)
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service
