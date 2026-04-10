import os
import random
import google.generativeai as genai
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS

def main():
    print("🎬 Bot başlatıldı...")
    
    # 1. API Ayarı ve Model Tanımlama
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: GEMINI_API_KEY bulunamadı!")
        return
        
    genai.configure(api_key=api_key)
    
    # 404 hatasını önlemek için tam model yolu kullanıyoruz
    model_name = 'models/gemini-1.5-flash'
    print(f"🤖 {model_name} modeline bağlanılıyor...")
    model = genai.GenerativeModel(model_name)

    # 2. Senaryo Yazımı
    try:
        istek = "Çocuklar için 15 saniyelik çok ilginç bir hayvan bilgisi yaz. Sadece seslendirme metni olsun."
        response = model.generate_content(istek)
        metin = response.text.strip()
        print(f"📝 Senaryo hazır: {metin[:50]}...")
    except Exception as e:
        print(f"❌ Gemini Hatası: {e}")
        return
    
    # 3. Ses Dosyası Oluşturma
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 4. Video Klasörü ve Dosya Kontrolü
    folder = "videos"
    if not os.path.exists(folder):
        print(f"❌ HATA: '{folder}' klasörü ana dizinde bulunamadı!")
        return

    video_files = [f for f in os.listdir(folder) if f.lower().endswith('.mp4')]
    if not video_files:
        print(f"❌ HATA: '{folder}' içinde .mp4 dosyası yok! Mevcutlar: {os.listdir(folder)}")
        return

    secilen = random.choice(video_files)
    video_path = os.path.join(folder, secilen)
    print(f"🎥 Seçilen Video: {secilen}")

    # 5. Video Montaj
    clip = VideoFileClip(video_path)
    
    # Videoyu sese göre ayarla (Döngü veya Kesme)
    if clip.duration < audio.duration:
        clip = clip.loop(duration=audio.duration)
    else:
        clip = clip.subclip(0, audio.duration)
    
    final_video = clip.set_audio(audio)
    final_video.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("✅ VİDEO BAŞARIYLA OLUŞTURULDU!")

if __name__ == "__main__":
    main()
