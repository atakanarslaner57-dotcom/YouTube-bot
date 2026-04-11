import asyncio
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip, AudioFileClip, TextClip, concatenate_audioclips, CompositeVideoClip
import edge_tts
import re
import os

# --- 1. AYARLAR VE VERILER ---
DIKEI_BOYUT = (1080, 1920) # 9:16 Shorts
FPS = 24
ALTYAZI_FONT_BOYUTU = 100 # Büyük ve okunaklı
KARAKTERLER = {
    "Papi": {"ses": "tr-TR-AhmetNeural", "perde": "+15Hz", "hiz": "+15%"},
    "Tori": {"ses": "tr-TR-EmelNeural", "perde": "-10Hz", "hiz": "-10%"}
}

DİYALOGLAR = [
    ("Papi", "Tori, bak! Artik uc boyutlu bir dunyadayiz, her sey cok daha derin!", 0),
    ("Tori", "Inanilmaz Papi! Etrafimizda donen kamera gercek bir film gibi hissettiriyor.", 1)
]

# --- 2. SES VE ALTYAZI SENKRONIZASYONU (SES DOSYASI ÜRETIMI) ---
async def uret_sesler():
    # Eski ses dosyalarını temizle
    for f in ["s_0.mp3", "s_1.mp3"]:
        if os.path.exists(f): os.remove(f)

    ses_klipleri = []
    for i, (isim, metin, _) in enumerate(DİYALOGLAR):
        path = f"s_{i}.mp3"
        await edge_tts.Communicate(metin, KARAKTERLER[isim]["ses"], pitch=KARAKTERLER[isim]["perde"], rate=KARAKTERLER[isim]["hiz"]).save(path)
        ses_klipleri.append(AudioFileClip(path))
    
    return concatenate_audioclips(ses_klipleri)

# --- 3. 3D RENDER VE GÖRSEL MOTOR ---
def project_3d(x, y, z, t):
    cam_x = 200 * math.sin(t * 0.5)
    cam_z = -500
    factor = 600 / (z - cam_z)
    px = (x - cam_x) * factor + 540
    py = y * factor + 960
    return int(px), int(py), factor

def ciz_3d_papi(draw, t, konusuyor=False):
    cx, cy, cz = 0, -200 + 50 * math.sin(t), 100
    # Kollar (Konuşuyorsa daha hızlı hareket)
    hiz_faktor = 2 if konusuyor else 1
    for i in range(8):
        angle = i * (math.pi / 4)
        for d in range(1, 8):
            kx = cx + d * 40 * math.cos(angle + math.sin(t*hiz_faktor + d*0.5))
            ky = cy + d * 40 * math.sin(angle + math.cos(t*hiz_faktor + d*0.5))
            kz = cz + math.sin(t + d) * 50
            px, py, f = project_3d(kx, ky, kz, t)
            draw.ellipse([px-10*f, py-10*f, px+10*f, py+10*f], fill=(255, 100, 80))
    # Kafa
    px, py, f = project_3d(cx, cy, cz, t)
    draw.ellipse([px-60*f, py-80*f, px+60*f, py+40*f], fill=(255, 80, 50), outline="black", width=2)

def generate_background_color(y, t):
    # Derinlik efektli gradyan
    factor = 1 + math.sin(t * 0.2) * 0.1
    return (0, int(y/40*factor), int(y/30*factor))

def make_frame(t):
    img = Image.new("RGB", DIKEI_BOYUT)
    draw = ImageDraw.Draw(img)
    # Gradyan Deniz
    for y in range(0, 1920, 20):
        color = generate_background_color(y, t)
        draw.rectangle([0, y, 1080, y+20], fill=color)

    # 3D Baloncuklar
    for i in range(15):
        bx = math.sin(i) * 700
        by = 1000 - (t * 250 + i * 120) % 2000
        bz = math.cos(i) * 350
        px, py, f = project_3d(bx, by, bz, t)
        if 0 < px < 1080 and 0 < py < 1920:
            draw.ellipse([px, py, px+5*f, py+5*f], outline=(255, 255, 255, 100), width=1)

    # Karakterler (Konuşma takibi: Papi 0-4s arası, Tori 4s+ arası konuşuyor gibi varsayalım)
    papi_konusuyor = True if t < 4.1 else False
    ciz_3d_papi(draw, t, papi_konusuyor)
    
    return np.array(img)

# --- 4. ALTYAZI OLUŞTURMA ---
def create_subtitle_clip(text, duration):
    # Altyazıyı 1080x1920 dikey kadrajın altına yerleştirir.
    subtitle = TextClip(text, fontsize=ALTYAZI_FONT_BOYUTU, color='white', font='Arial-Bold', method='caption', size=(1080, 500))
    subtitle = subtitle.set_position(('center', 1300)).set_duration(duration)
    # Altyazıyı bir CompositeVideoClip içine koyarak dikey dikey kadraja entegre ediyoruz.
    return CompositeVideoClip([subtitle.set_position(('center', 0))], size=DIKEI_BOYUT)

# --- 5. ANA ÇALIŞTIRMA ---
async def main():
    print("🚀 Bot baslatiliyor...")
    final_audio = await uret_sesler()
    sure = final_audio.duration
    
    # Animasyon Klibi
    video = VideoClip(make_frame, duration=sure)
    
    # Altyazı Senkronizasyonu
    subtitles = []
    
    # S_0 (Papi) Altyazısı
    s0_duration = AudioFileClip("s_0.mp3").duration
    subtitles.append(create_subtitle_clip("Tori, bak! Artik uc boyutlu bir dunyadayiz,\nher sey cok daha derin!", s0_duration).set_start(0))
    
    # S_1 (Tori) Altyazısı
    s1_start = s0_duration # İlk ses bittiğinde başlar
    s1_duration = AudioFileClip("s_1.mp3").duration
    subtitles.append(create_subtitle_clip("Inanilmaz Papi! Etrafimizda donen kamera\ngercek bir film gibi hissettiriyor.", s1_duration).set_start(s1_start))

    # Kurgu: Arka plan animasyonu + Karakterler + Altyazı
    subtitles_video = CompositeVideoClip([video] + subtitles)
    final_video = subtitles_video.set_audio(final_audio)

    print("🎬 Render basliyor...")
    final_video.write_videofile("otonom_shorts.mp4", fps=FPS, codec="libx264")
    print("✅ Bitti! Dosya: otonom_shorts.mp4")

if __name__ == "__main__":
    asyncio.run(main())
