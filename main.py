import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip
import google.generativeai as genai
from gtts import gTTS

def main():
    print("🎬 Video Üretimi Başladı...")
    
    # 1. API Ayarı
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 2. Senaryo ve Ses (Hızlı Render için kısa tutuldu)
    response = model.generate_content("Çocuklar için 15 saniyelik bir ilginç bilgi yaz. Sadece seslendirme metni.")
    metin = response.text.strip()
    
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 3. Videoları Bulma
    video_folder = "videos"
    video_files = [f for f in os.listdir(video_folder) if f.lower().endswith('.mp4')]

    if not video_files:
        print(f"❌ HATA: '{video_folder}' klasörü boş! Lütfen içine .mp4 dosyaları at.")
        return

    secilen_video = random.choice(video_files)
    video_path = os.path.join(video_folder, secilen_video)
    print(f"🎥 Seçilen Video: {secilen_video}")

    # 4. Montaj
    clip = VideoFileClip(video_path)
    # Sesin süresine göre videoyu ayarla
    clip = clip.loop(duration=audio.duration) if clip.duration < audio.duration else clip.subclip(0, audio.duration)

    final = clip.set_audio(audio)
    final.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("✅ Video Başarıyla Tamamlandı!")

if __name__ == "__main__":
    main()
