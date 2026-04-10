import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip
import google.generativeai as genai
from gtts import gTTS

def main():
    print("🎬 Bot başlatıldı...")
    
    # 1. Klasör Dedektifi
    print(f"Mevcut dizindeki dosyalar: {os.listdir('.')}")
    if os.path.exists("videos"):
        print(f"videos klasörü içeriği: {os.listdir('videos')}")
    else:
        print("❌ HATA: 'videos' klasörü ana dizinde bulunamadı!")
        return

    # 2. API ve Senaryo
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    metin = model.generate_content("Çocuklar için 15 saniyelik ilginç bir bilgi yaz.").text.strip()
    
    # 3. Ses ve Video Birleştirme
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")
    
    video_list = [f for f in os.listdir("videos") if f.lower().endswith(".mp4")]
    if not video_list:
        print("❌ HATA: videos klasöründe hiç mp4 yok!")
        return
        
    secilen_video = os.path.join("videos", random.choice(video_list))
    clip = VideoFileClip(secilen_video).loop(duration=audio.duration)
    
    final = clip.set_audio(audio)
    final.write_videofile("final_video.mp4", fps=24, codec="libx264")
    print("✅ Video hazır!")

if __name__ == "__main__":
    main()
