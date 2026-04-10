import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip
import google.generativeai as genai
from gtts import gTTS

def main():
    print("🎬 Video Üretimi Başladı...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: GEMINI_API_KEY eksik!")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 1. Senaryo
    response = model.generate_content("Çocuklar için 15 saniyelik çok ilginç bir hayvan bilgisi yaz. Sadece seslendirme metni.")
    metin = response.text.strip()
    print(f"📝 Senaryo: {metin}")
    
    # 2. Ses
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 3. Klasör Kontrolü (Hata ayıklama eklendi)
    folder = "videos"
    if not os.path.exists(folder):
        print(f"❌ HATA: '{folder}' klasörü bulunamadı!")
        return

    files = [f for f in os.listdir(folder) if f.lower().endswith('.mp4')]
    if not files:
        print(f"❌ HATA: '{folder}' içinde mp4 yok! Mevcut dosyalar: {os.listdir(folder)}")
        return

    secilen = random.choice(files)
    print(f"🎥 Seçilen Video: {secilen}")

    # 4. Montaj
    clip = VideoFileClip(os.path.join(folder, secilen))
    clip = clip.loop(duration=audio.duration) if clip.duration < audio.duration else clip.subclip(0, audio.duration)
    
    final = clip.set_audio(audio)
    final.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("✅ BAŞARILI!")

if __name__ == "__main__":
    main()
