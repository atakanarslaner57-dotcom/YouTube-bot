import asyncio
import math
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import VideoClip, AudioFileClip, concatenate_audioclips
import edge_tts

# --- Çizim Motoru (Detaylı Karakterler) ---
def ciz_papi(draw, x, y, t):
    # Kollar (8 adet, kıvrımlı)
    for i in range(8):
        offset = i * (math.pi / 4)
        ex = x + 100 * math.cos(offset + math.sin(t*3)*0.5)
        ey = y + 100 * math.sin(offset + math.cos(t*3)*0.5)
        draw.line([x, y, ex, ey], fill=(255, 80, 50), width=15)
    # Kafa ve Gözler
    draw.ellipse([x-60, y-70, x+60, y+50], fill=(255, 80, 50), outline="black")
    draw.ellipse([x-30, y-40, x-10, y-20], fill="white") # Sol göz
    draw.ellipse([x+10, y-40, x+30, y-20], fill="white") # Sağ göz

def ciz_tori(draw, x, y, t):
    salinim = 10 * math.sin(t*2)
    # Ayaklar
    for dx, dy in [(-80, 60), (80, 60), (-80, -20), (80, -20)]:
        draw.ellipse([x+dx-20, y+dy+salinim, x+dx+20, y+dy+40+salinim], fill=(34, 100, 34))
    # Kabuk (Desenli)
    draw.ellipse([x-120, y-40+salinim, x+120, y+100+salinim], fill=(40, 150, 40), outline="black", width=3)
    # Kafa
    draw.ellipse([x-40, y-80+salinim, x+40, y-20+salinim], fill=(50, 200, 50), outline="black")

def make_frame(t):
    img = Image.new("RGB", (1080, 1920), (0, 15, 40)) # Derin Deniz
    draw = ImageDraw.Draw(img)
    
    # Arka plan baloncukları
    for i in range(15):
        bx = (i * 150 + t * 40) % 1080
        by = (1800 - t * 120 - i * 100) % 1920
        draw.ellipse([bx, by, bx+10, by+10], outline=(100, 100, 200))

    # Karakterleri yerleştir
    ciz_papi(draw, 540 + 30*math.sin(t), 600 + 20*math.cos(t), t)
    ciz_tori(draw, 540, 1400, t)
    
    return np.array(img)

async def uret():
    diyaloglar = [
        ("tr-TR-AhmetNeural", "Tori, bak! Artik cok daha detayli ve canli gorunuyoruz!", "+15Hz"),
        ("tr-TR-EmelNeural", "Evet Papi, sonunda gercek birer karaktere donustuk.", "-10Hz")
    ]
    klipler = []
    for i, (ses, metin, perde) in enumerate(diyaloglar):
        path = f"s_{i}.mp3"
        await edge_tts.Communicate(metin, ses, pitch=perde).save(path)
        klipler.append(AudioFileClip(path))
    
    audio = concatenate_audioclips(klipler)
    video = VideoClip(make_frame, duration=audio.duration).set_audio(audio)
    video.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    asyncio.run(uret())
