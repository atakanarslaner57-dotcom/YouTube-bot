import os
import asyncio
import math
import subprocess
import sys

# 1. Kütüphane ve Hata Önleme
def setup():
    try:
        import PIL.Image
        if not hasattr(PIL.Image, 'ANTIALIAS'):
            PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3", "edge-tts", "Pillow==9.5.0"])

setup()
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
import edge_tts

async def main():
    print("🚀 Video üretim süreci zorlamalı modda başlıyor...")
    
    # Assets içindeki tüm dosyaları tara
    files = os.listdir("assets")
    print(f"📁 Klasördeki dosyalar: {files}")

    # Dosyaları akıllıca seç (Uzantıdan bağımsız, isme göre)
    bg_file = next((f for f in files if "background" in f.lower() or "coral" in f.lower()), None)
    papi_file = next((f for f in files if "papi" in f.lower()), None)

    if not bg_file or not papi_file:
        print(f"❌ Kritik dosyalar eksik! Bulunanlar: BG={bg_file}, Karakter={papi_file}")
        return

    # Ses Üretimi
    print("🎙️ Ses üretiliyor...")
    communicate = edge_tts.Communicate("Selam! Ben Kaplumbağa Papi!", "tr-TR-AhmetNeural")
    await communicate.save("s1.mp3")
    audio = AudioFileClip("s1.mp3")

    # Görsel İşleme (Hata verirse durmaması için try-except içinde)
    try:
        bg_path = f"assets/{bg_file}"
        papi_path = f"assets/{papi_file}"
        
        bg = ImageClip(bg_path).set_duration(audio.duration).resize(width=1920)
        papi = ImageClip(papi_path).set_duration(audio.duration).resize(height=550)
        papi = papi.set_position(lambda t: ("center", 450 + 30 * math.sin(t * 2)))

        final = CompositeVideoClip([bg, papi]).set_audio(audio)
        final.write_videofile("ilk_cizgi_filmim.mp4", fps=24, codec="libx264")
        print("✅ BAŞARILI! Video dosyası oluşturuldu.")
    except Exception as e:
        print(f"❌ Görsel işleme hatası: {e}")
        print("💡 ÖNERİ: Assets klasöründeki .avif dosyalarını silip yerine .png hallerini yüklemeyi dene.")

if __name__ == "__main__":
    asyncio.run(main())
