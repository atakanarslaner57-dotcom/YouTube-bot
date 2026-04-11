import os
import asyncio
import math
import subprocess
import sys

# --- 1. SİSTEM VE KÜTÜPHANE HAZIRLIĞI ---
def initialize_environment():
    """Gerekli yamaları uygular ve kütüphane desteğini kontrol eder."""
    try:
        import pillow_avif  # AVIF desteği için kritik
        import PIL.Image
        # MoviePy'nin aradığı ama yeni sürümlerde kalkmış olan komutu yamalıyoruz
        if not hasattr(PIL.Image, 'ANTIALIAS'):
            PIL.Image.ANTIALIAS = getattr(PIL.Image, 'LANCZOS', None)
        print("✅ Sistem yamaları başarıyla uygulandı.")
    except ImportError:
        print("⚠️ Eksik kütüphaneler var, yükleme başlatılıyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                               "Pillow==9.5.0", "pillow-avif-plugin", 
                               "moviepy==1.0.3", "edge-tts"])
        # Yüklemeden sonra tekrar dene
        import pillow_avif
        import PIL.Image
        PIL.Image.ANTIALIAS = getattr(PIL.Image, 'LANCZOS', None)

initialize_environment()

from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
import edge_tts

# --- 2. VİDEO ÜRETİM MANTIĞI ---

async def main():
    print("🎬 Video üretim süreci başlatıldı...")
    
    # Dosya yollarını senin klasöründeki gerçek isimlere göre belirledik
    assets_dir = "assets"
    bg_path = os.path.join(assets_dir, "background.jpg.avif")
    papi_path = os.path.join(assets_dir, "papi.png") # Loglarda 'papi.png' görünüyordu
    
    # Dosya kontrolü
    if not os.path.exists(bg_path) or not os.path.exists(papi_path):
        print(f"❌ HATA: Dosyalar bulunamadı!")
        print(f"Aranan Arka Plan: {bg_path}")
        print(f"Aranan Karakter: {papi_path}")
        return

    # 1. Ses üretimi
    print("🎙️ Ses dosyası oluşturuluyor...")
    text = "Selam! Ben Kaplumbağa Papi, denizin altı harika! Arkadaşım Fini nerede?"
    communicate = edge_tts.Communicate(text, "tr-TR-AhmetNeural")
    audio_file = "ses.mp3"
    await communicate.save(audio_file)
    audio = AudioFileClip(audio_file)

    # 2. Görsel katmanları oluşturma
    print("🖼️ Görsel katmanlar işleniyor...")
    # .avif dosyası burada pillow_avif sayesinde açılacak
    bg = ImageClip(bg_path).set_duration(audio.duration).resize(width=1920)
    
    papi = ImageClip(papi_path).set_duration(audio.duration).resize(height=550)
    
    # Karakteri ekrana yerleştirme ve basit bir 'yüzme' hareketi (yukarı-aşağı)
    # math.sin ile dalgalı bir hareket veriyoruz
    papi = papi.set_position(lambda t: ("center", 420 + 35 * math.sin(t * 2.5)))

    # 3. Birleştirme
    print("🎞️ Video birleştiriliyor...")
    final_video = CompositeVideoClip([bg, papi]).set_audio(audio)
    
    output_filename = "ilk_cizgi_filmim.mp4"
    final_video.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    
    print(f"✅ İŞLEM TAMAMLANDI: {output_filename} dosyası hazır!")

if __name__ == "__main__":
    asyncio.run(main())
