import os
import asyncio
import math
import subprocess
import sys

# 1. Kütüphane Yükleme
def install_dependencies():
    try:
        import edge_tts
        from moviepy.editor import ImageClip
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3", "edge-tts", "requests"])

install_dependencies()
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
import edge_tts

async def main():
    print("🚀 Video üretim süreci senin dosyalarına göre başlıyor...")
    
    # SENİN KLASÖRÜNDEKİ GERÇEK İSİMLER
    bg_path = "assets/background.jpg.avif"
    papi_path = "assets/papi.png" # Klasöründe 'papi.png' olarak görünüyor
    
    # Dosya var mı kontrol et
    if not os.path.exists(bg_path) or not os.path.exists(papi_path):
        print(f"❌ HATA: Dosyalar bulunamadı! Arananlar: {bg_path} ve {papi_path}")
        return

    # Ses üret
    text = "Selam! Ben Kaplumbağa Papi, denizin altı harika!"
    communicate = edge_tts.Communicate(text, "tr-TR-AhmetNeural")
    await communicate.save("s1.mp3")
    audio = AudioFileClip("s1.mp3")

    # Görselleri hazırla
    bg = ImageClip(bg_path).set_duration(audio.duration).resize(width=1920)
    char = ImageClip(papi_path).set_duration(audio.duration).resize(height=500)
    
    # Karakteri ekrana yerleştir ve yüzme efekti ver
    char = char.set_position(("center", "center"))
    char = char.set_position(lambda t: ("center", 400 + 30 * math.sin(t * 3)))

    # Birleştir ve kaydet
    final = CompositeVideoClip([bg, char]).set_audio(audio)
    final.write_videofile("ilk_cizgi_filmim.mp4", fps=24, codec="libx264")
    print("✅ BAŞARILI! ilk_cizgi_filmim.mp4 oluşturuldu.")

if __name__ == "__main__":
    asyncio.run(main())
