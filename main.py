import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip
import google.generativeai as genai
from gtts import gTTS

def main():
    print("🎬 İşlem başlıyor...")
    
    # API ve Model (models/ ekledik)
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    # 1. Kısa ve Öz Senaryo (Render süresini kısaltmak için)
    response = model.generate_content("Çocuklar için 10 saniyelik, tek cümlelik çok ilginç bir bilgi yaz.")
    metin = response.text.strip()
    print(f"📝 Senaryo: {metin}")
    
    # 2. Ses
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 3. Klasör Kontrolü
    video_list = [f for f in os.listdir("videos") if f.lower().endswith(".mp4")]
    if not video_list:
        print("❌ HATA: videos klasörü boş!")
        return
        
    secilen_video = os.path.join("videos", random.choice(video_list))
    print(f"🎥 Seçilen dosya: {secilen_video}")

    # 4. Hızlı Render Ayarları
    clip = VideoFileClip(secilen_video)
    
    # Eğer video sesten kısaysa sadece o kadarını kullan (loop riskine girmeyelim)
    # Eğer video uzunsa ses kadar kes
    if clip.duration > audio.duration:
        clip = clip.subclip(0, audio.duration)
    
    final = clip.set_audio(audio)
    
    # preset='ultrafast' ekledik: Kaliteden biraz ödün verip 10 kat hızlı bitirir
    final.write_videofile("final_video.mp4", fps=24, codec="libx264", preset='ultrafast')
    print("✅ BİTTİ!")

if __name__ == "__main__":
    main()
