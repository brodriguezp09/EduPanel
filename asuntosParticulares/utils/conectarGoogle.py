import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = os.path.join('#')
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    """Autentica y crea el objeto de servicio de la API de Google Drive."""
    creds = None
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    except Exception as e:
        print(f"Error al cargar las credenciales: {e}")
        return None
    
    service = build('drive', 'v3', credentials=creds)
    return service