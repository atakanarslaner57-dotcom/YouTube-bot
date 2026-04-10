import os
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import ColorClip, AudioFileClip, TextClip, CompositeVideoClip

def main():
    print("🎬 Video Üretimi Yeniden Deneniyor...")
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')

    # 1. Senaryo
    response = model.generate_content("Çocuklar için çok kısa, 5 kelimelik ilginç bir hayvan bilgisi yaz.")
    metin = response.text.strip()
    print(f"📝 Metin: {metin}")

    # 2. Ses
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 3. Görsel (Daha basit bir yöntemle)
    # 10 saniyelik mavi ekran
    bg = ColorClip(size=(720, 1280), color=[0, 153, 255]).set_duration(audio.duration)
    
    # Videoyu birleştir
    video = bg.set_audio(audio)
    
    # Dosyayı yazdır
    video.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("✅ Video başarıyla oluşturuldu!")

if __name__ == "__main__":
    main()
