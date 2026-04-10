import os
import random
import google.generativeai as genai
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS

def main():
    print("🎬 Bot başlatıldı...")
    
    # 1. API Ayarı
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: GEMINI_API_KEY eksik!")
        return
        
    genai.configure(api_key=api_key)
    
    # EN GARANTİ MODEL: gemini-pro
    # Eğer 1.5 çalışmıyorsa bu model her türlü çalışır.
    model_id = 'gemini-pro'
    print(f"🤖 {model_id} modeline bağlanılıyor...")
    
    try:
        model = genai.GenerativeModel(model_id)
        
        # Senaryo İsteği
        istek = "Çocuklar için 10 saniyelik, tek cümlelik ilginç bir hayvan bilgisi yaz."
        response = model.generate_content(istek)
        metin = response.text.strip()
        print(f"📝 Senaryo: {metin}")
        
    except Exception as e:
        print(f"❌ Gemini Hatası: {e}")
        return
    
    # 2. Ses Üretimi
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 3. Video Seçimi
    folder = "videos"
    video_files = [f for f in os.listdir(folder) if f.lower().endswith('.mp4')]
    if not video_files:
        print("❌ HATA: videos klasöründe video yok!")
        return

    secilen = random.choice(video_files)
    video_path = os.path.join(folder, secilen)
    print(f"🎥 Kullanılan Video: {secilen}")

    # 4. Hızlı Render (Hız: Ultrafast)
    clip = VideoFileClip(video_path)
    if clip.duration > audio.duration:
        clip = clip.subclip(0, audio.duration)
    
    final_video = clip.set_audio(audio)
    # 40 dk beklemeyi engelleyen satır:
    final_video.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac", preset='ultrafast')
    print("✅ İŞLEM BAŞARIYLA TAMAMLANDI!")

if __name__ == "__main__":
    main()
