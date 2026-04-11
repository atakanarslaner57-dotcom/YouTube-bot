import os
import subprocess
import sys
import asyncio
import math

# --- 1. OTOMATİK KÜTÜPHANE YÜKLEME ---
def install_dependencies():
    try:
        import edge_tts
        from moviepy.editor import ImageClip
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3", "edge-tts", "requests"])

install_dependencies()

import edge_tts
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip

# --- 2. AYARLAR (Dosya isimlerini kontrol et!) ---
RESIMLER = {
    "bg": "clear-colorful-illustrations-underwater-world-coral-reefs_628444-390.avif",
    "papi": "adorable-3d-illustration-baby-sea-turtle-turtle-has-light-green-shell-yellow-skin-it-is-smiling-looking-up-viewer_14117-541083.avif",
    "fini": "view-animated-cartoon-3d-fish_23-2150985174.avif",
    "tori": "3d-rendering-sea-ocean-icon_23-2151701656.avif"
}

# --- 3. SAHNE OLUŞTURUCU ---
async def generate_audio(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    return AudioFileClip(filename)

def create_scene(char_key, audio_clip):
    duration = audio_clip.duration
    bg = ImageClip(f"assets/{RESIMLER['bg']}").set_duration(duration).resize(width=1920)
    
    char_path = f"assets/{RESIMLER[char_key]}"
    if not os.path.exists(char_path):
        print(f"❌ HATA: {char_path} bulunamadı!")
        return None

    char = ImageClip(char_path).set_duration(duration).resize(height=500)
    char = char.set_position(lambda t: ("center", 400 + 30 * math.sin(t * 3)))
    
    return CompositeVideoClip([bg, char]).set_audio(audio_clip)

async def main():
    print("🚀 Video üretim süreci başladı...")
    
    # Sesleri üret
    s1_ses = await generate_audio("Selam! Ben Kaplumbağa Papi, bu resif çok güzel!", "tr-TR-AhmetNeural", "s1.mp3")
    s2_ses = await generate_audio("Ben de Fini! Hadi beraber yüzelim!", "tr-TR-EmelNeural", "s2.mp3")
    
    # Sahneleri oluştur
    sahne1 = create_scene("papi", s1_ses)
    sahne2 = create_scene("fini", s2_ses)
    
    if sahne1 and sahne2:
        from moviepy.editor import concatenate_videoclips
        final_video = concatenate_videoclips([sahne1, sahne2], method="compose")
        
        # DOSYA ADI YAML İLE AYNI OLMALI
        output_name = "ilk_cizgi_filmim.mp4"
        final_video.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")
        print(f"✅ VİDEO KAYDEDİLDİ: {output_name}")
    else:
        print("❌ Sahne oluşturulamadığı için video kaydedilmedi.")

if __name__ == "__main__":
    asyncio.run(main())
