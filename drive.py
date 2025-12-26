import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import json
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

token_json = os.getenv("GOOGLE_TOKEN_JSON")
if not token_json:
    raise RuntimeError("❌ GOOGLE_TOKEN_JSON not found in .env")

creds = Credentials.from_authorized_user_info(
    info=json.loads(token_json),
    scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=creds)

def create_folder(folder_name):
    folder = drive_service.files().create(
        body={
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        },
        fields="id"
    ).execute()
    return folder["id"]


def upload_file_to_folder(file_path, file_name, folder_id):
    media = MediaFileUpload(file_path, resumable=True)
    drive_service.files().create(
        body={
            "name": file_name,
            "parents": [folder_id]
        },
        media_body=media,
        fields="id"
    ).execute()


def get_folder_link(folder_id):
    return f"https://drive.google.com/drive/folders/{folder_id}"
