import os
import asyncio
import math
from moviepy.editor import ColorClip, CompositeVideoClip, AudioFileClip, concatenate_audioclips
import edge_tts

async def main():
    # 1. Seslendirme (İki farklı karakter tonu)
    papi_text = "Selam Tori! YouTube Shorts dünyasına hoş geldin, her şey ne kadar dikey!"
    tori_text = "Sakin ol Papi... Derin suların bilgeliği her formata sığar."
    
    await edge_tts.Communicate(papi_text, "tr-TR-AhmetNeural", pitch="+15Hz", rate="+15%").save("papi.mp3")
    await edge_tts.Communicate(tori_text, "tr-TR-EmelNeural", pitch="-10Hz", rate="-5%").save("tori.mp3")

    audio = concatenate_audioclips([AudioFileClip("papi.mp3"), AudioFileClip("tori.mp3")])

    # 2. Görsel Katmanlar (1080x1920 Shorts Boyutu)
    # Arka Plan: Koyu Mavi Deniz
    bg = ColorClip(size=(1080, 1920), color=(0, 45, 90)).set_duration(audio.duration)
    
    # Karakterler (Görsel yoksa renkli bloklar/daireler olarak canlandırılır)
    # Papi (Ahtapot - Kırmızımsı)
    papi = ColorClip(size=(400, 400), color=(255, 80, 80)).set_duration(audio.duration)
    papi = papi.set_position(lambda t: ('center', 700 + 40 * math.sin(t * 3)))

    # Tori (Kaplumbağa - Yeşilimsi)
    tori = ColorClip(size=(350, 350), color=(80, 255, 80)).set_duration(audio.duration)
    tori = tori.set_position(lambda t: ('center', 1200 + 20 * math.cos(t)))

    # 3. Birleştirme
    final_video = CompositeVideoClip([bg, papi, tori], size=(1080, 1920)).set_audio(audio)
    final_video.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    asyncio.run(main())
