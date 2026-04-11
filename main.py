import os
import asyncio
import requests
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip
import edge_tts

# --- AYARLAR ---
GEMINI_API_KEY = "BURAYA_GEMINI_API_KEYINI_YAZ" # Elimizdeki anahtar
WIDTH, HEIGHT = 1080, 1920

def create_vivid_background(filename):
    """ImageMagick gerektirmeden profesyonel bir arka plan ve yazı oluşturur."""
    # Okyanus mavisi bir temel oluştur
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 25, 50))
    draw = ImageDraw.Draw(img)
    
    # Basit bir degrade/ışık efekti ekle (geometri değil, estetik için)
    for i in range(HEIGHT):
        r, g, b = 0, min(255, 25 + i // 40), min(255, 50 + i // 20)
        draw.line([(0, i), (WIDTH, i)], fill=(r, g, b))
    
    # Karakter isimlerini yaz (ImageMagick hatasını bu yöntemle aşıyoruz)
    # Not: Yazı tipi olarak sistemde varsayılan olanı kullanır
    try:
        draw.text((WIDTH//2 - 200, HEIGHT//2), "PAPI & TORI & FINI", fill=(255, 255, 255))
    except:
        pass # Yazı tipi yüklenemezse boş geç, video çökmesin
        
    img.save(filename)

async def run_bot():
    print("Otonom süreç başladı...")
    
    # 1. Görseli Oluştur (Lokal ve Güvenli)
    create_vivid_background("scene.png")
    
    # 2. Seslendirme
    text = "Selam Papi, Tori ve Fini! İşte hatalardan arınmış gerçek 4K dünyamız!"
    await edge_tts.Communicate(text, "tr-TR-AhmetNeural").save("voice.mp3")
    
    # 3. Videoyu Birleştir
    audio = AudioFileClip("voice.mp3")
    clip = ImageClip("scene.png").set_duration(audio.duration).set_audio(audio)
    
    # 4. Kaydet
    clip.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264", bitrate="15M")
    print("Video hazır!")

if __name__ == "__main__":
    asyncio.run(run_bot())
