import os
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import TextClip, ColorClip, AudioFileClip

def main():
    print("🎬 Tam Otomatik Video Üretimi Başladı...")
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')

    # 1. Kısa ve Öz Senaryo Yazımı
    istek = "Çocuklar için 10 saniyelik, tek cümlelik çok ilginç bir hayvan bilgisi yaz. Sadece bilgi cümlesini ver."
    response = model.generate_content(istek)
    metin = response.text.strip()
    print(f"📝 Senaryo: {metin}")

    # 2. Ses Dosyası Oluşturma
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 3. Video Oluşturma (Arka Plan ve Yazı)
    # Shorts formatı için 1080x1920 boyutunda mavi bir ekran
    bg = ColorClip(size=(1080, 1920), color=[0, 153, 255], duration=audio.duration)
    
    # Ekrana yazıyı ekleme
    txt = TextClip(metin, fontsize=70, color='white', method='caption', size=(900, None))
    txt = txt.set_position('center').set_duration(audio.duration)

    # Ses ve görüntüyü birleştirme
    video = bg.set_audio(audio)
    final = video.set_duration(audio.duration)
    
    # Videoyu kaydetme
    final.write_videofile("final_video.mp4", fps=24, codec="libx264")
    print("✅ Video 'final_video.mp4' olarak hazır!")

if __name__ == "__main__":
    main()
