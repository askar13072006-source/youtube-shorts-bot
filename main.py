import os
import datetime
from generate_script import generate_rolls_royce_script
from create_video import create_audio_from_script, download_pexels_videos, create_vertical_video
from upload_to_youtube import get_authenticated_service, upload_video

def main():
    print("="*50)
    print("🤖 YOUTUBE SHORTS BOT STARTED")
    print("="*50)
    # Step 1: Generate script
    print("\n📝 Step 1: Generating script...")
    script = generate_rolls_royce_script()
    # Step 2: Create audio
    print("\n🎤 Step 2: Creating voiceover...")
    audio_file = create_audio_from_script(script)
    if not audio_file:
        print("❌ Failed to create audio. Exiting.")
        return
    # Step 3: Download videos
    print("\n📥 Step 3: Downloading video clips...")
    video_files = download_pexels_videos("rolls royce luxury car", num_videos=3)
    # Step 4: Create final video
    print("\n🎬 Step 4: Creating final video...")
    final_video = create_vertical_video(video_files, audio_file, "final_video.mp4")
    if not final_video:
        print("❌ Failed to create video. Exiting.")
        return
    # Step 5: Upload to YouTube
    print("\n📤 Step 5: Uploading to YouTube...")
    try:
        youtube = get_authenticated_service()
        today = datetime.date.today().strftime("%B %d, %Y")
        title = f"Rolls Royce: Luxury Redefined - {today} #Shorts"
        description = f"""Experience the pinnacle of automotive excellence. 
        
{script}

🏎️ Follow for daily luxury car content!

#RollsRoyce #LuxuryCars #Supercars #Automotive #Shorts #CarLovers"""
        tags = ["rolls royce", "luxury cars", "supercars", "automotive", "car review", "shorts"]
        video_url = upload_video(youtube, final_video, title, description, tags)
        print("\n" + "="*50)
        print("✅ SUCCESS! Video uploaded!")
        print(f"🔗 {video_url}")
        print("="*50)
    except Exception as e:
        print(f"❌ Upload failed: {e}")
    # Cleanup
    print("\n🧹 Cleaning up...")
    for file in video_files + [audio_file, final_video]:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Deleted {file}")
    print("\n🎉 Bot finished!")

if __name__ == "__main__":
    main()
