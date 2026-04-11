import os
import asyncio
import math
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, vfx
import edge_tts
import PIL.Image

# Eski Pillow sürümleri için yama
if not hasattr(PIL.Image, 'Resampling'):
    PIL.Image.Resampling = PIL.Image

async def main():
    print("📱 YouTube Shorts üretimi otonom modda başladı...")
    assets_dir = "assets"
    
    # 1. Dosya Tespiti (Shorts için dikey format)
    files = os.listdir(assets_dir)
    bg_path = next((os.path.join(assets_dir, f) for f in files if "arka" in f.lower() or "back" in f.lower()), None)
    papi_path = next((os.path.join(assets_dir, f) for f in files if "papi" in f.lower()), None)
    tori_path = next((os.path.join(assets_dir, f) for f in files if "tori" in f.lower()), None)

    if not bg_path or not papi_path or not tori_path:
        print("❌ HATA: Görsel dosyaları (arka plan, papi, tori) bulunamadı! İsimleri kontrol et.")
        return

    # 2. Seslendirme (Karakterlere özel tonlar)
    print("🎙️ Ses dosyası hazırlanıyor...")
    
    # Papi (Ahtapot) için tiz ve hızlı ses
    papi_text = "Selam Tori! Şu dikey dünyaya bak, her şey ne kadar uzun görünüyor!"
    papi_comm = edge_tts.Communicate(papi_text, "tr-TR-AhmetNeural", pitch="+15Hz", rate="+10%")
    await papi_comm.save("ses_papi.mp3")
    
    # Tori (Kaplumbağa) için kalın ve yavaş ses
    tori_text = "Haklısın Papi. Ama endişelenme, kabuğum hala her yere sığıyor."
    tori_comm = edge_tts.Communicate(tori_text, "tr-TR-EmelNeural", pitch="-10Hz", rate="-5%")
    await tori_comm.save("ses_tori.mp3")

    # Sesleri birleştirme
    from moviepy.editor import concatenate_audioclips
    final_audio = concatenate_audioclips([AudioFileClip("ses_papi.mp3"), AudioFileClip("ses_tori.mp3")])

    # 3. Görsel Kurgu (Shorts Boyutu: 1080 x 1920)
    bg = ImageClip(bg_path).set_duration(final_audio.duration).resize(height=1920)
    
    # Arka plana yavaş bir zoom efekti
    bg = bg.fx(vfx.resize, lambda t: 1 + 0.01 * t)

    # Karakterleri dikey ekrana yerleştirme (Merkeze odaklı)
    papi = ImageClip(papi_path).set_duration(final_audio.duration).resize(width=600)
    papi = papi.set_position(lambda t: ('center', 1000 + 30 * math.sin(t * 2)))

    tori = ImageClip(tori_path).set_duration(final_audio.duration).resize(width=500)
    tori = tori.set_position(lambda t: ('center', 1400 + 20 * math.cos(t)))

    # 4. Final Birleştirme
    final = CompositeVideoClip([bg, papi, tori], size=(1080, 1920)).set_audio(final_audio)
    final.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")
    print("✅ Shorts videosu hazır: otonom_shorts.mp4")

if __name__ == "__main__":
    asyncio.run(main())
