import os
import asyncio
import math
import subprocess
import sys

# 1. Klasör Kontrolü ve Raporlama (Hata nerede anlayacağız)
def list_assets():
    print("--- KLASÖR KONTROLÜ BAŞLADI ---")
    if not os.path.exists("assets"):
        print("❌ HATA: 'assets' klasörü ana dizinde bulunamadı!")
        return []
    
    files = os.listdir("assets")
    print(f"✅ Klasör bulundu. İçindeki dosyalar: {files}")
    return files

# 2. Kütüphane Yükleme
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
    asset_list = list_assets()
    if not asset_list:
        return

    # OTOMATİK DOSYA SEÇİCİ (Dosya adı ne olursa olsun bulur)
    bg_file = next((f for f in asset_list if "coral" in f.lower() or "underwater" in f.lower()), None)
    papi_file = next((f for f in asset_list if "papi" in f.lower() or "turtle" in f.lower()), None)
    
    print(f"🔍 Seçilen Arka Plan: {bg_file}")
    print(f"🔍 Seçilen Karakter: {papi_file}")

    if not bg_file or not papi_file:
        print("❌ HATA: Arka plan veya Papi dosyası eşleşmedi. İsimleri kontrol et!")
        return

    # Ses üret ve videoyu birleştir
    communicate = edge_tts.Communicate("Selam! Ben Papi!", "tr-TR-AhmetNeural")
    await communicate.save("s1.mp3")
    audio = AudioFileClip("s1.mp3")

    bg = ImageClip(f"assets/{bg_file}").set_duration(audio.duration).resize(width=1920)
    char = ImageClip(f"assets/{papi_file}").set_duration(audio.duration).resize(height=500)
    char = char.set_position(lambda t: ("center", 400 + 30 * math.sin(t * 3)))

    final = CompositeVideoClip([bg, char]).set_audio(audio)
    final.write_videofile("ilk_cizgi_filmim.mp4", fps=24, codec="libx264")
    print("🚀 BAŞARILI! Video oluşturuldu.")

if __name__ == "__main__":
    asyncio.run(main())
