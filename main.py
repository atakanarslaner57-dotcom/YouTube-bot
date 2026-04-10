import os
import random
import subprocess
import sys

# Eksik kütüphaneleri otomatik yükle
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from moviepy.editor import VideoFileClip, AudioFileClip
except ImportError:
    install('moviepy')
    from moviepy.editor import VideoFileClip, AudioFileClip

import google.generativeai as genai
from gtts import gTTS

def main():
    print("🎬 Video Üretimi Başladı...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Gemini Senaryosu
    istek = "Çocuklar için 20 saniyelik ilginç bir hayvan bilgisi yaz. Sadece seslendirme metni olsun."
    response = model.generate_content(istek)
    metin = response.text.strip()
    
    # Ses Oluşturma
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # ❗ KRİTİK NOKTA: Videoların Olduğu Klasör
    video_folder = "videos"
    # Sadece mp4 dosyalarını bul
    video_files = [f for f in os.listdir(video_folder) if f.lower().endswith('.mp4')]

    if not video_files:
        print(f"❌ HATA: '{video_folder}' klasörü boş veya bulunamadı!")
        return

    secilen_video = random.choice(video_files)
    video_path = os.path.join(video_folder, secilen_video)
    print(f"🎥 Kullanılan Video: {secilen_video}")

    # Video İşleme
    clip = VideoFileClip(video_path)
    if clip.duration < audio.duration:
        clip = clip.loop(duration=audio.duration)
    else:
        clip = clip.subclip(0, audio.duration)

    final_video = clip.set_audio(audio)
    final_video.write_videofile("final_video.mp4", fps=24, codec="libx264")
    print("✅ Video Başarıyla Oluşturuldu!")

if __name__ == "__main__":
    main()
