import asyncio
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from moviepy.editor import VideoClip, AudioFileClip
import edge_tts

# 4K Çözünürlük Ayarları
WIDTH, HEIGHT = 2160, 3840 

def create_vivid_character(draw, x, y, size, color, character_type):
    """Karakterlere 3D doku ve derinlik katan render fonksiyonu."""
    # 1. Ana Gövde ve Gölgelendirme (Depth)
    for i in range(size, 0, -2):
        alpha_color = tuple(list(color) + [255])
        draw.ellipse([x-i, y-i, x+i, y+i], fill=alpha_color)
    
    # 2. Canlı Gözler (Örneklerdeki gibi büyük ve parlak)
    eye_size = size // 3
    draw.ellipse([x-eye_size*2, y-eye_size, x-eye_size, y], fill="white") # Sol Göz
    draw.ellipse([x+eye_size, y-eye_size, x+eye_size*2, y], fill="white") # Sağ Göz

def make_frame(t):
    """Her kareyi 4K kalitesinde baştan inşa eder."""
    # Okyanus Derinliği (Gradient Arka Plan)
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 15, 40))
    draw = ImageDraw.Draw(img)
    
    # Işık Huzmeleri (God Rays) - Profesyonel Dokunuş
    ray_pos = int(t * 100) % WIDTH
    draw.polygon([(ray_pos, 0), (ray_pos+400, 0), (ray_pos+200, HEIGHT)], fill=(0, 40, 80))

    # Karakterler (Papi, Tori, Fini)
    # Papi (Ahtapot) - Yumuşak Mor
    create_vivid_character(draw, WIDTH//2, HEIGHT//2 + int(np.sin(t*2)*50), 120, (180, 100, 255), "octopus")
    
    # Fini (Balık) - Canlı Turuncu
    create_vivid_character(draw, WIDTH//2 + 300, HEIGHT//2 + 200, 80, (255, 140, 0), "fish")

    return np.array(img)

async def generate_video():
    # Seslendirme (Ultra HD ses kalitesi)
    communicate = edge_tts.Communicate("Tori, Papi, bakın! İşte gerçek 4K kalitesi!", "tr-TR-AhmetNeural")
    await communicate.save("voice.mp3")
    
    # Video Oluşturma
    clip = VideoClip(make_frame, duration=5).set_audio(AudioFileClip("voice.mp3"))
    clip.write_videofile("otonom_4k_vivid.mp4", fps=30, codec="libx264", bitrate="10M")

if __name__ == "__main__":
    asyncio.run(generate_video())
