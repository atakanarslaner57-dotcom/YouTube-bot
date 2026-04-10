import os
import random
import requests
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS

def get_gemini_text(api_key):
    # Kütüphane kullanmadan doğrudan API'ye istek atıyoruz
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": "Çocuklar için 10 saniyelik, tek cümlelik çok ilginç bir hayvan bilgisi yaz."}]
        }]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()
    else:
        print(f"❌ API Hatası: {result}")
        return "Deniz analarının kalbi, beyni ve kemikleri yoktur." # Hata durumunda yedek metin

def main():
    print("🎬 Bot başlatıldı (Saf API Modu)...")
    api_key = os.getenv("GEMINI_API_KEY")
    
    # 1. Senaryo
    metin = get_gemini_text(api_key)
    print(f"📝 Senaryo: {metin}")
    
    # 2. Ses Üretimi
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 3. Video Seçimi
    video_files = [f for f in os.listdir("videos") if f.lower().endswith('.mp4')]
    secilen = os.path.join("videos", random.choice(video_files))
    
    # 4. Hızlı Render
    clip = VideoFileClip(secilen)
    clip = clip.subclip(0, audio.duration) if clip.duration > audio.duration else clip.loop(duration=audio.duration)
    
    final = clip.set_audio(audio)
    final.write_videofile("final_video.mp4", fps=24, codec="libx264", preset='ultrafast')
    print("✅ BAŞARILI!")

if __name__ == "__main__":
    main()
