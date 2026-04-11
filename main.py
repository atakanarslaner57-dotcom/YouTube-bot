import os
import asyncio
import requests
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, ColorClip
import edge_tts

# Karakter Linkleri (Doğrudan PNG/JPG adresleri)
CHARACTERS = {
    "Papi": "https://png.pngtree.com/png-clipart/20230913/original/pngtree-3d-orange-fish-png-image_20930822.png",
    "Tori": "https://png.pngtree.com/png-clipart/20230531/original/pngtree-3d-turtle-turtle-gradient-texture-ui-design-ux-material-png-image_14115622.png",
    "Fini": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzY7B9Y6p7lH9-Pz9j8_Z6J8-R8E5t1-Pz9Q&s"
}

def get_assets():
    clips = []
    for name, url in CHARACTERS.items():
        try:
            r = requests.get(url, timeout=10)
            with open(f"{name}.png", "wb") as f:
                f.write(r.content)
            
            # Karakteri oluştur ve ekrandaki yerini ayarla
            c = ImageClip(f"{name}.png").set_duration(5).resize(width=500)
            clips.append(c)
        except Exception as e:
            print(f"{name} yüklenemedi: {e}")
    return clips

async def build_video():
    print("Sistem kontrol ediliyor...")
    
    # 1. Seslendirme (Hata payı bırakmamak için basit tutuldu)
    text = "Selam Papi, Tori ve Fini! İşte o çok beklediğimiz animasyon dünyası burada."
    await edge_tts.Communicate(text, "tr-TR-AhmetNeural").save("voice.mp3")
    audio = AudioFileClip("voice.mp3")
    
    # 2. Karakterleri İndir ve Hazırla
    assets = get_assets()
    if not assets:
        print("Hata: Hiçbir karakter yüklenemedi!")
        return

    # 3. Arka Plan (Derin Okyanus Mavisi)
    bg = ColorClip(size=(1080, 1920), color=(0, 40, 80)).set_duration(audio.duration)

    # 4. Karakter Pozisyonları (Önceki videodaki boşluk hatasını giderir)
    # Papi (Merkez), Tori (Sol), Fini (Sağ)
    papi = assets[0].set_position(("center", 400)).set_duration(audio.duration)
    tori = assets[1].set_position((100, 1000)).set_duration(audio.duration)
    fini = assets[2].set_position((600, 1000)).set_duration(audio.duration)

    # 5. Sahne Birleştirme
    final = CompositeVideoClip([bg, papi, tori, fini]).set_audio(audio)
    
    # 6. Render (En güvenli ayarlar)
    final.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("Video Hazır!")

if __name__ == "__main__":
    asyncio.run(build_video())
