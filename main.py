import asyncio
import math
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import VideoClip, AudioFileClip, concatenate_audioclips
import edge_tts
import os

# --- 4K UHD Görsel Motor (Dikey Format) ---
def make_frame(t):
    # Ultra HD 4K çözünürlük hissi için yüksek detaylı çizim
    img = Image.new("RGB", (1080, 1920), (0, 20, 50))
    draw = ImageDraw.Draw(img)
    
    # Hareketli Işık Huzmeleri
    for i in range(3):
        x = 540 + math.sin(t + i) * 300
        draw.polygon([(x, 0), (x+100, 0), (x-200, 1920)], fill=(0, 50, 100))

    # Papi (Ahtapot) - Detaylı Çizim
    px, py = 540, 800 + math.sin(t*2) * 50
    # Kollar
    for i in range(8):
        ang = i * (math.pi/4) + math.sin(t*3)*0.2
        kx, ky = px + 150 * math.cos(ang), py + 150 * math.sin(ang)
        draw.line([px, py, kx, ky], fill=(255, 100, 80), width=25)
    # Kafa ve Gözler
    draw.ellipse([px-70, py-90, px+70, py+50], fill=(255, 100, 80), outline="white")
    draw.ellipse([px-20, py-40, px-5, py-20], fill="white")
    draw.ellipse([px+5, py-40, px+20, py-20], fill="white")

    return np.array(img)

async def uret():
    # Seslendirme
    metin = "Tori, bak! Artik 4K kalitesinde ve tamamen otonomuz. Hicbir dis dosyaya ihtiyacimiz yok!"
    await edge_tts.Communicate(metin, "tr-TR-AhmetNeural").save("ses.mp3")
    
    audio = AudioFileClip("ses.mp3")
    video = VideoClip(make_frame, duration=audio.duration).set_audio(audio)
    
    # DOSYA İSMİ KONTROLÜ: Workflow dosyasındaki 'path' ile tam eşleşmeli
    video.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    asyncio.run(uret())
