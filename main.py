import os
import subprocess
import sys
import asyncio
import math

# --- 1. KÜTÜPHANE YÜKLEME ---
def install_dependencies():
    try:
        import edge_tts
        from moviepy.editor import ImageClip
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3", "edge-tts", "requests"])

install_dependencies()

import edge_tts
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip

# --- 2. DOSYALARI BULMA FONKSİYONU ---
def get_asset_path(filename_or_keyword):
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        print(f"❌ HATA: '{assets_dir}' klasörü bulunamadı!")
        return None
        
    # Önce tam adı dene (papi.png gibi)
    full_path = os.path.join(assets_dir, filename_or_keyword)
    if os.path.exists(full_path):
        return full_path
        
    # Bulamazsa klasör içinde o kelimeyi içeren ilk png'yi bul
    for file in os.listdir(assets_dir):
        if filename_or_keyword.lower() in file.lower() and file.endswith(".png"):
            return os.path.join(assets_dir, file)
    return None

async def generate_audio(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    return AudioFileClip(filename)

def create_scene(image_path, audio_clip):
    duration = audio_clip.duration
    # Arka planı 'coral' veya 'underwater' kelimesinden bulur
    bg_path = get_asset_path("coral") or get_asset_path("underwater")
    
    if not bg_path or not image_path:
        print(f"❌ Eksik dosya: BG={bg_path}, Karakter={image_path}")
        return None

    bg = ImageClip(bg_path).set_duration(duration).resize(width=1920)
    char = ImageClip(image_path).set_duration(duration).resize(height=500)
    # Karakteri ekranda hafifçe yüzüyormuş gibi hareket ettirir
    char = char.set_position(lambda t: ("center", 400 + 30 * math.sin(t * 3)))
    
    return CompositeVideoClip([bg, char]).set_audio(audio_clip)

async def main():
    print("🚀 Video üretim süreci başladı (.png modunda)...")
    
    # Karakter dosyalarını senin verdiğin isimlere göre ara
    papi_img = get_asset_path("papi.png")
    fini_img = get_asset_path("fini.png")
    
    # Sesleri üret
    s1_ses = await generate_audio("Selam! Ben Kaplumbağa Papi!", "tr-TR-AhmetNeural", "s1.mp3")
    s2_ses = await generate_audio("Ben de Fini! Hadi yüzelim!", "tr-TR-EmelNeural", "s2.mp3")
    
    sahne1 = create_scene(papi_img, s1_ses)
    sahne2 = create_scene(fini_img, s2_ses)
    
    if sahne1 and sahne2:
        from moviepy.editor import concatenate_videoclips
        final_video = concatenate_videoclips([sahne1, sahne2], method="compose")
        final_video.write_videofile("ilk_cizgi_filmim.mp4", fps=24, codec="libx264")
        print("✅ BAŞARILI: ilk_cizgi_filmim.mp4 oluşturuldu!")
    else:
        print("❌ HATA: Karakter veya arka plan dosyaları assets klasöründe bulunamadı.")

if __name__ == "__main__":
    asyncio.run(main())
