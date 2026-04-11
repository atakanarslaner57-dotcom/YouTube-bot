import os
import asyncio
import math
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
import edge_tts
import PIL.Image

# GitHub Actions üzerindeki eski kütüphane hatalarını önlemek için yama
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = getattr(PIL.Image, 'LANCZOS', PIL.Image.BICUBIC)

async def main():
    print("🚀 Video üretim süreci başladı...")
    assets_dir = "assets"
    
    # 1. Akıllı Dosya Tespiti (İsim hatalarını tolere eder)
    files = os.listdir(assets_dir)
    bg_path = next((os.path.join(assets_dir, f) for f in files if "arka" in f.lower() or "back" in f.lower()), None)
    papi_path = next((os.path.join(assets_dir, f) for f in files if "papi" in f.lower()), None)
    ahtapot_path = next((os.path.join(assets_dir, f) for f in files if "ahtapot" in f.lower() or "tori" in f.lower()), None)

    if not bg_path or not papi_path:
        print("❌ HATA: Arka plan veya Papi dosyası bulunamadı!")
        return

    # 2. Seslendirme (Doğal Ses)
    print("🎙️ Ses dosyası hazırlanıyor...")
    text = "Selam dostlar! Ben Kaplumbağa Papi. Yanımda en yakın arkadaşım Ahtapot var. Birlikte denizin derinliklerini keşfediyoruz!"
    communicate = edge_tts.Communicate(text, "tr-TR-AhmetNeural")
    await communicate.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # 3. Görsel Kurgu
    bg = ImageClip(bg_path).set_duration(audio.duration).resize(width=1920)
    papi = ImageClip(papi_path).set_duration(audio.duration).resize(height=450)
    
    # Papi'ye yüzme efekti (sol alt)
    papi = papi.set_position(lambda t: (300 + 10 * math.sin(t), 600 + 15 * math.cos(t)))

    katmanlar = [bg, papi]

    # Eğer ahtapot resmi de varsa ekle (sağ alt)
    if ahtapot_path:
        ahtapot = ImageClip(ahtapot_path).set_duration(audio.duration).resize(height=400)
        ahtapot = ahtapot.set_position(lambda t: (1200, 550 + 20 * math.sin(t * 1.5)))
        katmanlar.append(ahtapot)

    # 4. Kayıt (Dosya ismi sistemin aradığı isimle aynı: ilk_cizgi_filmim.mp4)
    final = CompositeVideoClip(katmanlar).set_audio(audio)
    final.write_videofile("ilk_cizgi_filmim.mp4", fps=24, codec="libx264")
    print("✅ Video başarıyla oluşturuldu: ilk_cizgi_filmim.mp4")

if __name__ == "__main__":
    asyncio.run(main())
