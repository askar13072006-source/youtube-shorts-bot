import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import datetime

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """Authenticate with YouTube API"""
    creds = None
    if os.path.exists('token.pickle'):
        print("📂 Found saved credentials")
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds and os.environ.get('YOUTUBE_CREDENTIALS'):
        print("📂 Using credentials from secrets")
        import json
        creds_data = json.loads(os.environ.get('YOUTUBE_CREDENTIALS'))
        creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing credentials...")
            creds.refresh(Request())
        else:
            print("🔐 Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        print("💾 Credentials saved!")
        print("\n" + "="*50)
        print("🔑 COPY THIS TO GITHUB SECRETS:")
        print("="*50)
        print(creds.to_json())
        print("="*50 + "\n")
    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, video_file, title, description, tags):
    """Upload video to YouTube"""
    print(f"📤 Uploading: {title}")
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '2'  # Autos & Vehicles
        },
        'status': {
            'privacyStatus': 'public',  # or 'private', 'unlisted'
            'selfDeclaredMadeForKids': False
        }
    }
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype='video/mp4')
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"⏳ Upload progress: {progress}%")
    video_id = response['id']
    video_url = f"https://youtube.com/watch?v={video_id}"
    print(f"✅ Upload complete!")
    print(f"🔗 Video URL: {video_url}")
    return video_url

if __name__ == "__main__":
    youtube = get_authenticated_service()
    today = datetime.date.today().strftime("%B %d, %Y")
    title = f"Rolls Royce Luxury & Power - {today} #Shorts"
    description = "Experience the ultimate in automotive luxury. Rolls Royce represents engineering excellence and timeless elegance. 🏎️✨ #RollsRoyce #LuxuryCars #Shorts"
    tags = ["rolls royce", "luxury cars", "supercars", "automotive", "shorts"]
    upload_video(youtube, "final_video.mp4", title, description, tags)
