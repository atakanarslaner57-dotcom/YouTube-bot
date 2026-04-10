import os
import random
import google.generativeai as genai
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS

def main():
    print("🎬 Bot başlatıldı...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: GEMINI_API_KEY bulunamadı!")
        return
        
    genai.configure(api_key=api_key)
    
    # 404 HATASINI ÇÖZEN KRİTİK DEĞİŞİKLİK:
    # Bazı kütüphane sürümleri direkt ismi kabul etmez, tam yol ister.
    model_id = 'models/gemini-1.5-flash'
    print(f"🤖 {model_id} modeline bağlanılıyor...")
    
    try:
        model = genai.GenerativeModel(model_name=model_id)
        
        # Senaryo İsteği
        istek = "Çocuklar için 10 saniyelik, tek cümlelik ilginç bir hayvan bilgisi yaz."
        response = model.generate_content(istek)
        metin = response.text.strip()
        print(f"📝 Senaryo: {metin}")
        
    except Exception as e:
        print(f"❌ Gemini Hatası: {e}")
        print("İpucu: Eğer hala 404 alıyorsan, model ismini 'gemini-pro' olarak değiştirmeyi deneyebiliriz.")
        return
    
    # Ses Üretimi
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # Video Seçimi
    folder = "videos"
    video_files = [f for f in os.listdir(folder) if f.lower().endswith('.mp4')]
    if not video_files:
        print(f"❌ HATA: {folder} klasöründe video yok!")
        return

    secilen = random.choice(video_files)
    video_path = os.path.join(folder, secilen)
    print(f"🎥 Kullanılan Video: {secilen}")

    # Hızlı Render (preset='ultrafast')
    clip = VideoFileClip(video_path)
    if clip.duration > audio.duration:
        clip = clip.subclip(0, audio.duration)
    
    final_video = clip.set_audio(audio)
    final_video.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac", preset='ultrafast')
    print("✅ BAŞARILI!")

if __name__ == "__main__":
    main()
