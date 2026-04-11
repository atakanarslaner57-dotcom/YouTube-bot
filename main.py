import asyncio
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import VideoClip, AudioFileClip
import edge_tts
import os

# --- AYARLAR (Hata riskini sıfırlamak için) ---
OUTPUT_NAME = "otonom_shorts.mp4"
WIDTH, HEIGHT = 2160, 3840 # 4K Dikey

def make_frame(t):
    # Derin okyanus mavisi arka plan
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 10, 40))
    draw = ImageDraw.Draw(img)
    
    # Işık huzmeleri (God Rays)
    for i in range(3):
        x_pos = (t * 200 + i * 800) % WIDTH
        draw.polygon([(x_pos, 0), (x_pos + 400, 0), (x_pos - 200, HEIGHT)], fill=(0, 30, 70))

    # Papi (Ahtapot) - 3D Görünümlü Render
    px, py = WIDTH // 2, HEIGHT // 2 + int(np.sin(t * 3) * 60)
    # Vantuzlu Kollar (Basit çizgiden kurtulduk)
    for i in range(8):
        ang = i * (np.pi / 4) + np.sin(t * 2) * 0.3
        kx, ky = px + 300 * np.cos(ang), py + 300 * np.sin(ang)
        draw.line([px, py, kx, ky], fill=(200, 80, 60), width=40)
    
    # Kafa ve Büyük Gözler
    draw.ellipse([px-150, py-180, px+150, py+100], fill=(255, 100, 80), outline="white", width=5)
    draw.ellipse([px-60, py-60, px-10, py-10], fill="white")
    draw.ellipse([px+10, py-60, px+60, py-10], fill="white")

    return np.array(img)

async def run_bot():
    # 1. Ses Dosyasını Oluştur
    metin = "Tori, Papi! İşte gerçek 4K kalitesi ve canlı renkler!"
    communicate = edge_tts.Communicate(metin, "tr-TR-AhmetNeural")
    await communicate.save("temp_voice.mp3")
    
    # 2. Videoyu Oluştur ve Sesi Göm
    audio = AudioFileClip("temp_voice.mp3")
    video = VideoClip(make_frame, duration=audio.duration).set_audio(audio)
    
    # 3. Dosyayı Kaydet (Kritik nokta burası)
    video.write_videofile(OUTPUT_NAME, fps=30, codec="libx264", bitrate="15M")
    
    # Temizlik
    audio.close()
    if os.path.exists("temp_voice.mp3"): os.remove("temp_voice.mp3")

if __name__ == "__main__":
    asyncio.run(run_bot())
