import os
import asyncio
import edge_tts
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, concatenate_audioclips

# --- AYARLAR ---
SHORTS_SIZE = (1080, 1920)
FPS = 24

# Karakter Ses Tanımlamaları (Çizgi film ruhuna uygun tonlar)
CHARACTERS = {
    "Papi": {"voice": "tr-TR-AhmetNeural", "pitch": "+10Hz", "rate": "+10%"}, # Enerjik/Tiz
    "Tori": {"voice": "tr-TR-EmelNeural", "pitch": "-5Hz", "rate": "-5%"}    # Sakin/Bilge
}

async def generate_voice(text, char_name, filename):
    cfg = CHARACTERS[char_name]
    communicate = edge_tts.Communicate(text, cfg["voice"], pitch=cfg["pitch"], rate=cfg["rate"])
    await communicate.save(filename)

async def main():
    print("🚀 Otonom Çizgi Film Üretimi Başladı...")
    
    # 1. SENARYO VE SESLENDİRME
    script = [
        ("Papi", "Hey Tori! Şu dikey dünyaya bak, her şey ne kadar uzun görünüyor!"),
        ("Tori", "Haklısın Papi. Ama endişelenme, kabuğum hala her yere sığıyor."),
        ("Papi", "O zaman hadi, Shorts izleyenlere küçük bir su altı dansı gösterelim!")
    ]

    audio_clips = []
    for i, (char, text) in enumerate(script):
        fname = f"voice_{i}.mp3"
        await generate_voice(text, char, fname)
        audio_clips.append(AudioFileClip(fname))

    final_audio = concatenate_audioclips(audio_clips)
    final_audio.write_audiofile("final_audio.mp3")

    # 2. GÖRSEL KURGU (Bot burada mevcut assets klasörünü kullanır)
    # Not: Görsel üretim araçlarını (DALL-E vb.) API ile bağlamadıysan, 
    # bot 'assets' içindeki en uygun resimleri seçip dikey formata adapte eder.
    
    bg = ImageClip("assets/arka_plan.png").set_duration(final_audio.duration).resize(height=1920)
    
    # Karakterleri sahneye yerleştirme (Dikey Merkeze Odaklı)
    papi = ImageClip("assets/papi.png").set_duration(final_audio.duration).resize(width=600)
    papi = papi.set_position(('center', 800))
    
    tori = ImageClip("assets/tori.png").set_duration(final_audio.duration).resize(width=500)
    tori = tori.set_position(('center', 1300))

    # 3. BİRLEŞTİRME
    video = CompositeVideoClip([bg, papi, tori], size=SHORTS_SIZE).set_audio(final_audio)
    video.write_videofile("otonom_shorts.mp4", fps=FPS, codec="libx264")
    print("✨ İşlem Tamam! Dikey Shorts videon hazır.")

if __name__ == "__main__":
    asyncio.run(main())
