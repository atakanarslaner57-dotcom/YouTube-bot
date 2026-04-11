import os
import asyncio
import math
import subprocess
import sys

# 1. KÜTÜPHANE VE HATA DÜZELTME (Patch)
def install_dependencies():
    try:
        import PIL.Image
        # Yeni Pillow sürümlerinde ANTIALIAS kaldırıldı, MoviePy için geri ekliyoruz
        if not hasattr(PIL.Image, 'ANTIALIAS'):
            PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
        import edge_tts
        from moviepy.editor import ImageClip
    except (ImportError, AttributeError):
        # Kütüphaneleri en uyumlu sürümleriyle kuruyoruz
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3", "edge-tts", "requests", "Pillow==9.5.0"])
        # Kurulumdan sonra yamayı tekrar kontrol et
        import PIL.Image
        PIL.Image.ANTIALIAS = getattr(PIL.Image, 'LANCZOS', None)

install_dependencies()

from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
import edge_tts

async def main():
    print("🚀 Video üretim süreci başlatıldı (Hata düzeltme modu aktif)...")
    
    bg_path = "assets/background.jpg.avif"
    papi_path = "assets/papi.png"
    
    if not os.path.exists(bg_path) or not os.path.exists(papi_path):
        print(f"❌ HATA: Dosyalar eksik! {bg_path} veya {papi_path} bulunamadı.")
        return

    # Ses üretimi
    text = "Selam! Ben Kaplumbağa Papi, denizin altı harika!"
    communicate = edge_tts.Communicate(text, "tr-TR-AhmetNeural")
    await communicate.save("s1.mp3")
    audio = AudioFileClip("s1.mp3")

    # Görsel klipleri oluştur
    # ANTIALIAS hatası burada çözüldü
    bg = ImageClip(bg_path).set_duration(audio.duration).resize(width=1920)
    char = ImageClip(papi_path).set_duration(audio.duration).resize(height=500)
    
    # Karakteri yerleştir ve hareket ver
    char = char.set_position(lambda t: ("center", 450 + 25 * math.sin(t * 3)))

    # Birleştir ve kaydet
    final = CompositeVideoClip([bg, char]).set_audio(audio)
    output_name = "ilk_cizgi_filmim.mp4"
    final.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")
    
    print(f"✅ BAŞARILI! {output_name} başarıyla oluşturuldu.")

if __name__ == "__main__":
    asyncio.run(main())
