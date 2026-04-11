import os
import asyncio
import math
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, vfx
import edge_tts

# --- SHORTS YAPILANDIRMASI ---
SIZE = (1080, 1920) # Tam dikey Shorts boyutu

async def generate_pro_voice(text, filename, char_type="papi"):
    # Papi: Tiz ve hızlı | Tori: Kalın ve sakin
    voice = "tr-TR-AhmetNeural" if char_type == "papi" else "tr-TR-EmelNeural"
    pitch = "+15Hz" if char_type == "papi" else "-10Hz"
    rate = "+15%" if char_type == "papi" else "-5%"
    
    communicate = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate)
    await communicate.save(filename)

async def main():
    print("🎬 Yapay zeka otonom kurguya başlıyor...")
    
    # 1. Senaryo Yazımı ve Seslendirme
    lines = [
        ("papi", "Vay canına Tori! Bu dikey ekran bizi ne kadar da uzun gösterdi böyle!"),
        ("tori", "Acele etme Papi... Derin suların tadını çıkar, Shorts izleyenlere el salla.")
    ]
    
    audio_clips = []
    for i, (char, text) in enumerate(lines):
        fname = f"speech_{i}.mp3"
        await generate_pro_voice(text, fname, char)
        audio_clips.append(AudioFileClip(fname))
    
    from moviepy.editor import concatenate_audioclips
    final_audio = concatenate_audioclips(audio_clips)

    # 2. Görsel Katmanlar (Dikey Formata Uyarlama)
    # Mevcut dosyalarını bulur, yoksa hata vermez, dikey merkeze yerleştirir
    assets = os.listdir("assets")
    bg_file = next((f for f in assets if "arka" in f.lower()), "background.png")
    papi_file = next((f for f in assets if "papi" in f.lower()), "papi.png")
    tori_file = next((f for f in assets if "tori" in f.lower()), "tori.png")

    # Arka plan: Yavaşça zoom yapan dikey kadraj
    bg = ImageClip(f"assets/{bg_file}").set_duration(final_audio.duration).resize(height=1920)
    bg = bg.set_position('center').fx(vfx.resize, lambda t: 1 + 0.02 * t)

    # Papi (Ahtapot): Ekranın ortasında yüzme animasyonu
    papi = ImageClip(f"assets/{papi_file}").set_duration(final_audio.duration).resize(width=700)
    papi = papi.set_position(lambda t: ('center', 800 + 40 * math.sin(t * 2)))

    # Tori (Kaplumbağa): Daha aşağıda, yavaş salınım
    tori = ImageClip(f"assets/{tori_file}").set_duration(final_audio.duration).resize(width=600)
    tori = tori.set_position(lambda t: ('center', 1300 + 20 * math.cos(t)))

    # 3. Final Birleştirme
    final_video = CompositeVideoClip([bg, papi, tori], size=SIZE).set_audio(final_audio)
    final_video.write_videofile("shorts_final.mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    asyncio.run(main())
