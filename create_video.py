import os
import requests
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ColorClip
import random

def download_pexels_videos(query="rolls royce luxury car", num_videos=3):
    """Download Rolls Royce video clips from Pexels"""
    api_key = os.environ.get("PEXELS_API_KEY")
    headers = {"Authorization": api_key}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={num_videos}&orientation=portrait"
    try:
        print("📥 Downloading car videos...")
        response = requests.get(url, headers=headers)
        data = response.json()
        video_files = []
        for i, video in enumerate(data.get("videos", [])[:num_videos]):
            # Get HD video file
            video_file = None
            for file in video["video_files"]:
                if file.get("quality") == "hd":
                    video_file = file
                    break
            if not video_file:
                video_file = video["video_files"][0]
            video_url = video_file["link"]
            filename = f"clip_{i}.mp4"
            print(f"📥 Downloading clip {i+1}...")
            video_content = requests.get(video_url).content
            with open(filename, "wb") as f:
                f.write(video_content)
            video_files.append(filename)
            print(f"✅ Downloaded {filename}")
        return video_files
    except Exception as e:
        print(f"❌ Error downloading videos: {e}")
        return []

def create_audio_from_script(script, output_file="voiceover.mp3"):
    """Convert script to audio using free Google voice"""
    print("🎤 Creating voice...")
    try:
        tts = gTTS(text=script, lang='en', slow=False)
        tts.save(output_file)
        print(f"✅ Voice created: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ Voice creation error: {e}")
        return None

def create_vertical_video(video_files, audio_file, output_file="final_video.mp4"):
    """Make a vertical video perfect for YouTube Shorts"""
    print("🎬 Making your video...")
    try:
        # Load the voice
        audio = AudioFileClip(audio_file)
        audio_duration = audio.duration
        clips = []
        if video_files:
            # Use downloaded car videos
            for video_file in video_files:
                clip = VideoFileClip(video_file)
                # Make it vertical (like phone screen)
                clip = clip.resize(height=1920)
                # Crop to perfect size
                w, h = clip.size
                target_width = 1080
                x_center = w / 2
                x1 = x_center - (target_width / 2)
                x2 = x_center + (target_width / 2)
                clip = clip.crop(x1=x1, y1=0, x2=x2, y2=1920)
                clips.append(clip)
        else:
            # If no videos, create black screen
            print("⚠️ No videos found - using black background")
            black_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=audio_duration)
            clips = [black_clip]
        # Make sure video is as long as the voice
        total_duration = sum([c.duration for c in clips])
        if total_duration < audio_duration:
            # Loop videos to match voice length
            loops_needed = int(audio_duration / total_duration) + 1
            clips = clips * loops_needed
        final_video = concatenate_videoclips(clips, method="compose")
        final_video = final_video.subclip(0, audio_duration)
        # Add the voice to the video
        final_video = final_video.set_audio(audio)
        # Save the final video
        print("💾 Saving your video...")
        final_video.write_videofile(
            output_file,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            preset='ultrafast'
        )
        print(f"✅ Video created: {output_file}")
        # Clean up
        audio.close()
        for clip in clips:
            clip.close()
        return output_file
    except Exception as e:
        print(f"❌ Video creation error: {e}")
        return None

if __name__ == "__main__":
    # Test the functions
    script = "Rolls Royce. The pinnacle of luxury."
    audio = create_audio_from_script(script)
    videos = download_pexels_videos()
    create_vertical_video(videos, audio)
