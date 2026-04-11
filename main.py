import os
import asyncio
import math
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
import edge_tts

async def main():
    print("🚀 Video üretim süreci başlatıldı...")
    
    # Assets klasöründeki dosyaları tara
    assets_dir = "assets"
    files = os.listdir(assets_dir)
    print(f"📁 Klasördeki dosyalar: {files}")

    # Dosya isimlerindeki hataları (çift uzantı veya boşluk) otomatik bulalım
    # 'arka plan.jpg.png' gibi dosyaları eşleştirmek için:
    bg_file = next((f for f in files if "arka" in f.lower() or "background" in f.lower()), None)
    papi_file = next((f for f in files if "papi" in f.lower()), None)

    if not bg_file or not papi_file:
        print(f"❌ HATA: Gerekli dosyalar bulunamadı!")
        return

    # Ses üretimi
    print("🎙️ Ses dosyası hazırlanıyor...")
    text = "Selam! Ben Kaplumbağa Papi. Sonunda teknik sorunları çözdük ve denizin altındayız!"
    communicate = edge_tts.Communicate(text, "tr-TR-AhmetNeural")
    await communicate.save("s1.mp3")
    audio = AudioFileClip("s1.mp3")

    # Görsel katmanlar
    bg_path = os.path.join(assets_dir, bg_file)
    papi_path = os.path.join(assets_dir, papi_file)

    print(f"🖼️ İşlenen dosyalar: BG={bg_file}, Karakter={papi_file}")

    bg = ImageClip(bg_path).set_duration(audio.duration).resize(width=1920)
    papi = ImageClip(papi_path).set_duration(audio.duration).resize(height=550)
    
    # Karakteri ekrana yerleştir ve hareket ver
    papi = papi.set_position(lambda t: ("center", 450 + 30 * math.sin(t * 3)))

    # Birleştir ve kaydet
    final = CompositeVideoClip([bg, papi]).set_audio(audio)
    final.write_videofile("ilk_cizgi_filmim.mp4", fps=24, codec="libx264")
    
    print("✅ BAŞARILI! Video 'Summary' kısmında seni bekliyor.")

if __name__ == "__main__":
    asyncio.run(main())
