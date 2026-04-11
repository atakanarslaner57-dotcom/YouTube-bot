import asyncio
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from moviepy.editor import VideoClip, AudioFileClip, concatenate_audioclips
import edge_tts

# --- Profesyonel Çizim Motoru ---
def ciz_deniz(draw, t):
    # Gradyan Deniz (Yukarıdan aşağıya koyulaşan)
    for y in range(0, 1920, 10):
        color = (0, int(20 + y/40), int(60 + y/30))
        draw.rectangle([0, y, 1080, y+10], fill=color)
    
    # Işık huzmeleri (Yüzeyden gelen)
    for i in range(3):
        x_pos = 200 + i*300 + math.sin(t)*50
        draw.polygon([(x_pos, 0), (x_pos+100, 0), (x_pos-200, 1920), (x_pos-300, 1920)], fill=(20, 80, 120, 100))

def ciz_papi(draw, x, y, t, konusuyor=False):
    # Kollar (Vantuzlu ve Yumuşak Hatlı)
    for i in range(8):
        ang = i * (math.pi/4) + math.sin(t*3 + i)*0.3
        pts = [(x, y)]
        for d in range(6):
            kx = x + (d*35) * math.cos(ang + math.sin(t*2+d)*0.2)
            ky = y + (d*35) * math.sin(ang + math.cos(t*2+d)*0.2)
            pts.append((kx, ky))
            # Vantuzlar (Küçük beyaz noktalar)
            if d > 2: draw.ellipse([kx-5, ky-5, kx+5, ky+5], fill=(255, 200, 200))
        draw.line(pts, fill=(255, 100, 80), width=25-d*3)
    
    # Kafa ve Yüz
    draw.ellipse([x-70, y-90, x+70, y+50], fill=(255, 100, 80), outline=(180, 50, 40), width=3)
    # Gözler (Canlı)
    for ex in [x-30, x+30]:
        draw.ellipse([ex-18, y-40, ex+18, y], fill="white", outline="black")
        draw.ellipse([ex-6, y-25, ex+6, y-13], fill="black") # Göz bebeği
    # Ağız (Konuşma Efekti)
    ağız_genislik = 20 + (15 * math.sin(t*15) if konusuyor else 0)
    draw.chord([x-ağız_genislik, y+10, x+ağız_genislik, y+30], 0, 180, fill=(100, 0, 0))

def make_frame(t):
    img = Image.new("RGBA", (1080, 1920))
    draw = ImageDraw.Draw(img)
    
    ciz_deniz(draw, t)
    
    # Karakterler (Papi ve Tori)
    # Papi konuşma süresi (0-4 saniye arası varsayalım)
    papi_konusuyor = True if t < 4 else False
    ciz_papi(draw, 540 + 50*math.sin(t), 700 + 40*math.cos(t*0.8), t, papi_konusuyor)
    
    # Arka Plan Baloncukları
    for i in range(10):
        bx = (i*200 + t*60) % 1080
        by = (1800 - t*150 - i*120) % 1920
        draw.ellipse([bx, by, bx+15, by+15], outline=(200, 230, 255, 150))

    return np.array(img.convert("RGB"))

async def uret():
    diyaloglar = [
        ("tr-TR-AhmetNeural", "Bak Tori! Sonunda kollarımda vantuzlarım, senin kabuğunda desenlerin var!", "+15Hz"),
        ("tr-TR-EmelNeural", "Evet Papi, şimdi gerçekten okyanusun bir parçası gibi hissettim.", "-12Hz")
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
    asyncio.run(uret())
