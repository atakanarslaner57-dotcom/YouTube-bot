import os
import asyncio
import math
import PIL.Image

# MoviePy'nin hata verdiği o meşhur 'ANTIALIAS' sorununu burada manuel düzeltiyoruz
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
import edge_tts

async def main():
    print("🚀 Video üretim süreci başlıyor...")
    
    bg_path = "assets/background.jpg.avif"
    papi_path = "assets/papi.png"
    
    if not os.path.exists(bg_path) or not os.path.exists(papi_path):
        print(f"❌ Dosya bulunamadı: {bg_path} veya {papi_path}")
        return

    # Ses üretimi
    communicate = edge_tts.Communicate("Selam! Ben Kaplumbağa Papi, denizin altı harika!", "tr-TR-AhmetNeural")
    await communicate.save("s1.mp3")
    audio = AudioFileClip("s1.mp3")

    # Görsel klipler
    bg = ImageClip(bg_path).set_duration(audio.duration).resize(width=1920)
    char = ImageClip(papi_path).set_duration(audio.duration).resize(height=500)
    char = char.set_position(lambda t: ("center", 450 + 25 * math.sin(t * 3)))

    # Birleştir ve kaydet
    final = CompositeVideoClip([bg, char]).set_audio(audio)
    final.write_videofile("ilk_cizgi_filmim.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("✅ BAŞARILI! Video oluşturuldu.")

if __name__ == "__main__":
    asyncio.run(main())
