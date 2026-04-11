import os
import math
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, ColorClip

def create_pro_video():
    # Ayarlar
    DURATION = 40
    assets = "assets"
    
    # 1. Arka Planı Hazırla
    bg = ImageClip(f"{assets}/arka plan.png").set_duration(DURATION).resize(width=1920)
    
    # 2. Karakterleri "Temizlenmiş" ve Hareketli Olarak Ekle
    # Not: Bu aşamada görsellerin PNG (şeffaf) olduğunu varsayıyoruz
    papi = ImageClip(f"{assets}/papi.png").set_duration(DURATION).resize(height=400)
    ahtapot = ImageClip(f"{assets}/ahtapot.png").set_duration(DURATION).resize(height=350)

    # Profesyonel Hareket Fonksiyonları (Yüzme Efekti)
    papi_move = lambda t: (400 + 20 * math.sin(t), 600 + 10 * math.cos(t))
    ahtapot_move = lambda t: (1100 + 15 * math.cos(t*0.5), 550 + 30 * math.sin(t))

    papi = papi.set_position(papi_move)
    ahtapot = ahtapot.set_position(ahtapot_move)

    # 3. Profesyonel Seslendirmeyi Ekle
    audio = AudioFileClip(f"{assets}/konusma.mp3")
    
    # Final Birleştirme
    video = CompositeVideoClip([bg, papi, ahtapot]).set_audio(audio)
    
    print("🚀 Video işleniyor, lütfen bekleyin...")
    video.write_videofile("Papi_Ve_Dostu_Final.mp4", fps=24, codec="libx264")
    print("✨ Başardık! Final videosu hazır.")

if __name__ == "__main__":
    create_pro_video()
