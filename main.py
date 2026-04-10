import os
import random
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip

def main():
    print("🎬 Profesyonel Video Üretimi Başladı...")
    
    # 1. API Ayarları
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: API Anahtarı bulunamadı!")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')

    # 2. Gemini'ye Çocuklar İçin Senaryo Yazdırıyoruz
    # Not: Videolarının süresine göre bu isteği uzatıp kısaltabilirsin.
    istek = (
        "Sen popüler bir çocuk kanalı yazarısın. 20-30 saniyelik, "
        "heyecan verici bir 'Biliyor muydunuz?' bilgisi yaz. "
        "Konu: Hayvanlar veya doğa olsun. Çok neşeli bir dil kullan. "
        "Sadece seslendirme metnini ver, sahne tarifi yapma."
    )
    
    try:
        response = model.generate_content(istek)
        metin = response.text.strip()
        print(f"📝 Senaryo Hazır: {metin}")

        # 3. Seslendirme Oluşturma (Türkçe)
        print("🎙️ Ses dosyası hazırlanıyor...")
        tts = gTTS(text=metin, lang='tr')
        tts.save("ses.mp3")
        audio = AudioFileClip("ses.mp3")

        # 4. Arka Plan Videosunu Seçme
        video_folder = "videos"
        # Klasördeki tüm dosyaları listele (sadece .mp4 olanları al)
        video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]

        if not video_files:
            print("❌ HATA: 'videos' klasöründe hiç .mp4 dosyası bulunamadı!")
            return

        secilen_video = random.choice(video_files)
        video_path = os.path.join(video_folder, secilen_video)
        print(f"🎥 Seçilen Arka Plan: {secilen_video}")

        # 5. Videoyu ve Sesi Birleştirme
        clip = VideoFileClip(video_path)
        
        # Eğer video sesten kısaysa, videoyu döngüye sok (loop)
        if clip.duration < audio.duration:
            clip = clip.loop(duration=audio.duration)
        else:
            # Eğer video sesten uzunsa, sesin bittiği yerde videoyu kes
            clip = clip.subclip(0, audio.duration)

        final_video = clip.set_audio(audio)
        
        # 6. Dosyayı Kaydetme (YouTube Shorts formatı için yüksek kalite)
        print("⚙️ Video render ediliyor (birleştiriliyor)...")
        final_video.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
        print("✅ BAŞARILI! 'final_video.mp4' hazır.")

    except Exception as e:
        print(f"❌ Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
