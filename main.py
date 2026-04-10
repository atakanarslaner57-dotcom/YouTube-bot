import os
import random
import google.generativeai as genai
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS

def main():
    print("🎬 Bot başlatıldı...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # 404 Hatasını kökten çözen 'gemini-1.5-flash-latest' kullanımı
    model_id = 'gemini-1.5-flash-latest' 
    print(f"🤖 {model_id} modeline bağlanılıyor...")
    
    try:
        model = genai.GenerativeModel(model_id)
        
        # Daha kısa ve öz senaryo isteği
        istek = "Çocuklar için 12 saniyelik, tek cümlelik çok şaşırtıcı bir bilgi yaz."
        response = model.generate_content(istek)
        metin = response.text.strip()
        print(f"📝 Senaryo: {metin}")
        
    except Exception as e:
        print(f"❌ Gemini Hatası: {e}")
        # Eğer hala 404 verirse 'gemini-pro' en sağlam kaledir
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Kısa bir ilginç bilgi yaz.")
        metin = response.text.strip()

    # Ses ve Video Birleştirme (Hızlı Render Ayarlarıyla)
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    folder = "videos"
    video_files = [f for f in os.listdir(folder) if f.lower().endswith('.mp4')]
    secilen = random.choice(video_files)
    
    clip = VideoFileClip(os.path.join(folder, secilen))
    if clip.duration > audio.duration:
        clip = clip.subclip(0, audio.duration)
    
    # preset='ultrafast' sayesinde 35 dakika beklemezsin, 2-3 dakikada biter
    final_video = clip.set_audio(audio)
    final_video.write_videofile("final_video.mp4", fps=24, codec="libx264", preset='ultrafast')
    print("✅ İŞLEM TAMAMLANDI!")

if __name__ == "__main__":
    main()
