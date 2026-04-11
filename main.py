import asyncio
import math
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import VideoClip, AudioFileClip, concatenate_audioclips
import edge_tts

# --- Karakter Çizim Motoru ---
# Bot, her karede karakterleri bu fonksiyonla yeniden çizer.
def ciz_karakter(draw, isim, x, y, size, t):
    
    if isim == "Tori": # Kaplumbağa
        y_salinim = 15 * math.sin(t * 2)
        # Ayaklar (Elipsler)
        for pos in [(x-80, y+100), (x+80, y+100), (x-80, y+200), (x+80, y+200)]:
            draw.ellipse([pos[0], pos[1]+y_salinim, pos[0]+50, pos[1]+30+y_salinim], fill=(50, 100, 50))
        # Gövde/Kabuk (Büyük Yeşil Elips)
        draw.ellipse([x-150, y+50+y_salinim, x+150, y+250+y_salinim], fill=(34, 139, 34), outline="black", width=5)
        
    elif isim == "Papi": # Ahtapot
        x_k = x + 40 * math.cos(t*2)
        y_k = y + 60 * math.sin(t*3)
        # Kollar (İnce Uzun Elipsler/Çizgiler)
        for i in range(8):
            angle = t*5 + (i * math.pi / 4)
            kx, ky = x_k + 120 * math.cos(angle), y_k + 120 * math.sin(angle)
            draw.line([x_k+75, y_k+75, kx+75, ky+75], fill=(255, 69, 0), width=15)
        # Kafa (Turuncu Daire)
        draw.ellipse([x_k, y_k, x_k+150, y_k+150], fill=(255, 69, 0), outline="black", width=5)
        
    elif isim == "Fini": # Balık
        x_f = x + 120 * math.sin(t*5)
        y_f = y + 100 * math.cos(t*2)
        # Kuyruk (Mavi Üçgen)
        draw.polygon([(x_f+80, y_f+20), (x_f+120, y_f), (x_f+120, y_f+40)], fill=(0, 191, 255))
        # Gövde (Sarı Elips)
        draw.ellipse([x_f, y_f, x_f+100, y_f+60], fill=(255, 215, 0), outline="black", width=3)

# --- Video Kare Oluşturma Fonksiyonu ---
def make_frame(t):
    # 1. Arka Plan: Koyu Lacivert Deniz (1080x1920)
    # Tuval (Image) oluşturuluyor
    img = Image.new("RGB", (1080, 1920), (0, 20, 50))
    draw = ImageDraw.Draw(img)

    # 2. Mercanlar (Basit Şekillerle Arka Plan Canlandırması)
    for i in range(3):
        h = 150 + 40 * math.sin(t + i*2)
        draw.chord([300*i, 1920-h, 300*i+200, 1920], 0, 180, fill=(150, 50, 100))

    # 3. Karakterleri Çiz (Pozisyonları matematikle belirleniyor)
    ciz_karakter(draw, "Tori", 540, 1100, 450, t) # Kaplumbağa (Ortada)
    ciz_karakter(draw, "Papi", 200, 600, 350, t)  # Ahtapot (Solda)
    ciz_karakter(draw, "Fini", 800, 800, 150, t)  # Balık (Sağda)

    # PIL Image'ı MoviePy'ın anlayacağı NumPy dizisine çeviriyoruz
    return np.array(img)

# --- Ses Üretme Motoru ---
async def uret_sesler():
    # Karakterler ve replikleri
    diyaloglar = [
        ("Papi", "Tori! Tori! Bak, hicbir resme ihtiyacimiz yok, her seyi biz yaratiyoruz!", "tr-TR-AhmetNeural", "+15Hz"),
        ("Tori", "Haklisin Papi... Gercek guc, kodun icindeki hayal gucudur.", "tr-TR-EmelNeural", "-10Hz"),
        ("Fini", "Hey, ben de buradayım! Hadi yuzelim!", "tr-TR-EmelNeural", "+25Hz")
    ]
    
    ses_dosyalari = []
    for i, (isim, metin, ses, perde) in enumerate(diyaloglar):
        dosya = f"ses_{i}.mp3"
        comm = edge_tts.Communicate(metin, ses, pitch=perde)
        await comm.save(dosya)
        ses_dosyalari.append(AudioFileClip(dosya))
    
    return concatenate_audioclips(ses_dosyalari)

# --- Ana Çalıştırma ---
async def main():
    print("🚀 Tam otonom animasyon motoru baslatiliyor...")
    final_audio = await uret_sesler()
    
    # Video klibi oluşturma (make_frame fonksiyonunu kullanır)
    video = VideoClip(make_frame, duration=final_audio.duration)
    
    # Kurgu ve Kayit
    final_video = video.set_audio(final_audio)
    final_video.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")
    print("✅ Video basariyla kaydedildi: otonom_shorts.mp4")

if __name__ == "__main__":
    asyncio.run(main())
