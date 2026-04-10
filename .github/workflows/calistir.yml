import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip
import google.generativeai as genai
from gtts import gTTS

def main():
    print("🎬 Video Üretimi Başladı...")
    
    # API Kurulumu
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 1. Gemini'den Hikaye Al
    response = model.generate_content("Çocuklar için 15 saniyelik bir ilginç bilgi yaz. Sadece seslendirme metni.")
    metin = response.text.strip()
    print(f"📝 Senaryo: {metin}")
    
    # 2. Ses Üret
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 3. Klasör ve Video Kontrolü
    video_folder = "videos"
    if not os.path.exists(video_folder):
        print(f"❌ HATA: '{video_folder}' klasörü bulunamadı!")
        return

    video_files = [f for f in os.listdir(video_folder) if f.lower().endswith('.mp4')]
    
    if not video_files:
        print(f"❌ HATA: '{video_folder}' klasörü boş veya .mp4 dosyası yok!")
        # Klasördeki her şeyi yazdır (Hata ayıklama için)
        print("Klasör içeriği:", os.listdir(video_folder))
        return

    secilen = random.choice(video_files)
    video_path = os.path.join(video_folder, secilen)
    print(f"🎥 Kullanılan Video: {secilen}")

    # 4. Video Montaj
    clip = VideoFileClip(video_path)
    
    # Süre Ayarı (Döngü veya Kesme)
    if clip.duration < audio.duration:
        clip = clip.loop(duration=audio.duration)
    else:
        clip = clip.subclip(0, audio.duration)
    
    final = clip.set_audio(audio)
    # Hata vermemesi için codec ayarları eklendi
    final.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
    print("✅ Video başarıyla oluşturuldu!")

if __name__ == "__main__":
    main()
