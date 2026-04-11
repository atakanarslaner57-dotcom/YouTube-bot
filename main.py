import os
import asyncio
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, ColorClip
import edge_tts

# 4K Ayarları
WIDTH, HEIGHT = 2160, 3840 

async def create_cartoon():
    # 1. Seslendirme Oluştur
    metin = "Tori, Papi, Fini! İşte hayal ettiğimiz o muhteşem 4K dünyası!"
    await edge_tts.Communicate(metin, "tr-TR-AhmetNeural").save("voice.mp3")
    audio = AudioFileClip("voice.mp3")
    duration = audio.duration

    # 2. Arka Plan (Derin Okyanus Mavisi)
    bg = ColorClip(size=(WIDTH, HEIGHT), color=(0, 20, 50)).set_duration(duration)

    # 3. Senin Yüklediğin 3D Karakterleri Yerleştir
    # Papi (Ahtapot) - Merkeze yakın
    papi = (ImageClip("papi.png")
            .set_duration(duration)
            .resize(width=1000)
            .set_position(('center', 1000)))

    # Tori (Kaplumbağa) - Sol Alt
    tori = (ImageClip("tori.png")
            .set_duration(duration)
            .resize(width=800)
            .set_position((200, 2200)))

    # Fini (Balık) - Sağ Alt
    fini = (ImageClip("fini.png")
            .set_duration(duration)
            .resize(width=600)
            .set_position((1300, 2800)))

    # 4. Sahneyi Birleştir
    final_video = CompositeVideoClip([bg, papi, tori, fini]).set_audio(audio)
    
    # 5. 4K Render
    final_video.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264", bitrate="15M")

if __name__ == "__main__":
    asyncio.run(create_cartoon())
