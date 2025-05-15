from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from utils import download_image, generate_banner
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
from dotenv import load_dotenv
import os


app = FastAPI()

# Constants for Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
TARGET_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

def upload_to_drive(image_io: BytesIO, filename: str) -> str:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    media = MediaIoBaseUpload(image_io, mimetype='image/jpeg', resumable=True)
    file_metadata = {
        'name': filename,
        'parents': [TARGET_FOLDER_ID]
    }

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Make file public
    service.permissions().create(
        fileId=file['id'],
        body={'type': 'anyone', 'role': 'reader'},
    ).execute()

    return f"https://drive.google.com/uc?id={file['id']}"

@app.post("/generate-banner")
async def generate_banner_api(image_url: str = Form(...), text: str = Form(...), footer: str = Form("@TheSignalDaily")):
    try:
        bg = download_image(image_url)
        banner_io = generate_banner(bg, text, footer)
        public_url = upload_to_drive(banner_io, "banner.jpg")
        return JSONResponse(content={"image_url": public_url})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
