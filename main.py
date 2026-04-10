import os
import random
import subprocess
import sys

# 1. Kütüphane Kontrolü (Hatanın Çözümü)
def install_requirements():
    try:
        import moviepy.editor
    except ImportError:
        print("⚙️ Kütüphaneler eksik, yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy", "google-generativeai", "gTTS"])

install_requirements()

from moviepy.editor import VideoFileClip, AudioFileClip
import google.generativeai as genai
from gtts import gTTS

def main():
    print("🎬 Video Üretimi Başladı...")
    
    # 2. API ve Model Kurulumu
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. Senaryo ve Ses
    metin_isteği = "Çocuklar için 20 saniyelik çok ilginç bir hayvan bilgisi yaz. Sadece seslendirme metni ver."
    response = model.generate_content(metin_isteği)
    metin = response.text.strip()
    
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 4. Video Klasörü Kontrolü
    video_folder = "videos"
    # Sadece .mp4 ile biten dosyaları küçük/büyük harf bakmaksızın bulur
    video_files = [f for f in os.listdir(video_folder) if f.lower().endswith('.mp4')]

    if not video_files:
        print(f"❌ HATA: '{video_folder}' klasöründe hiç .mp4 video bulunamadı!")
        return

    secilen_video_adi = random.choice(video_files)
    video_yolu = os.path.join(video_folder, secilen_video_adi)
    print(f"🎥 Kullanılan Video: {secilen_video_adi}")

    # 5. Video Montaj
    clip = VideoFileClip(video_yolu)
    
    # Video sesten kısaysa döngüye sok, uzunsa kes
    if clip.duration < audio.duration:
        clip = clip.loop(duration=audio.duration)
    else:
        clip = clip.subclip(0, audio.duration)

    final = clip.set_audio(audio)
    final.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("✅ İşlem Tamamlandı!")

if __name__ == "__main__":
    main()
