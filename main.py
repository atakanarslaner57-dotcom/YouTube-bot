import asyncio
import math
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import VideoClip, AudioFileClip, concatenate_audioclips
import edge_tts

# --- Karakterleri 'Canlı' Çizme Motoru ---
def ciz_papi_detayli(draw, x, y, t):
    # Kollar (Vantuzlu ve kıvrımlı)
    for i in range(8):
        ang = i * (math.pi/4) + math.sin(t*2)*0.2
        points = []
        for d in range(5): # Kolu 5 parçada çizerek kıvırıyoruz
            kx = x + (d*30) * math.cos(ang + math.sin(t*3+d)*0.3)
            ky = y + (d*30) * math.sin(ang + math.cos(t*3+d)*0.3)
            points.append((kx, ky))
            # Vantuzlar
            draw.ellipse([kx-4, ky-4, kx+4, ky+4], fill=(255, 150, 150))
        draw.line(points, fill=(255, 80, 50), width=18-d*2)
    # Kafa ve Yüz
    draw.ellipse([x-60, y-80, x+60, y+40], fill=(255, 80, 50), outline=(150, 0, 0))
    # Gözler (Canlı bakış)
    for ex in [x-25, x+25]:
        draw.ellipse([ex-15, y-30, ex+15, y], fill="white")
        draw.ellipse([ex-5, y-20, ex+5, y-10], fill="black")

def ciz_tori_detayli(draw, x, y, t):
    s = 8 * math.sin(t*2)
    # Yüzgeçler
    for fx, fy in [(-90, 20), (90, 20)]:
        draw.ellipse([x+fx-30, y+fy+s, x+fx+30, y+fy+20+s], fill=(46, 139, 87))
    # Kabuk ve Desenler
    draw.ellipse([x-130, y-50+s, x+130, y+110+s], fill=(107, 142, 35), outline="black")
    for i in range(3): # Altıgen desenleri taklit et
        draw.regular_polygon((x, y+30+s, 60-i*15), 6, rotation=30, outline=(50, 80, 20), width=2)
    # Kafa
    draw.ellipse([x-35, y-90+s, x+35, y-20+s], fill=(144, 238, 144), outline="black")

def make_frame(t):
    # Derinlik efektli deniz
    img = Image.new("RGB", (1080, 1920), (0, 25, 60))
    draw = ImageDraw.Draw(img)
    
    # Hareketli Mercanlar (Arka Plan Yaşamı)
    for i in range(6):
        h = 180 + 60 * math.sin(t + i)
        draw.chord([i*180, 1920-h, i*180+200, 1920+100], 0, 180, fill=(200, 80, 120))

    # Karakterler
    ciz_papi_detayli(draw, 540 + 40*math.sin(t), 700 + 30*math.cos(t), t)
    ciz_tori_detayli(draw, 540, 1450, t)
    
    return np.array(img)

async def uret_shorts():
    # Seslendirme (Daha vurgulu ve karakter bazlı)
    diyaloglar = [
        ("tr-TR-AhmetNeural", "Bak Tori! Sonunda kollarimda vantuzlarim, senin kabugunda desenlerin var!", "+15Hz"),
        ("tr-TR-EmelNeural", "Evet Papi, simdi gercekten okyanusun bir parcasi gibi hissettim.", "-12Hz")
    ]
    clips = []
    for i, (ses, metin, perde) in enumerate(diyaloglar):
        p = f"s_{i}.mp3"
        await edge_tts.Communicate(metin, ses, pitch=perde).save(p)
        clips.append(AudioFileClip(p))
    
    audio = concatenate_audioclips(clips)
    video = VideoClip(make_frame, duration=audio.duration).set_audio(audio)
    video.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    asyncio.run(uret_shorts())
