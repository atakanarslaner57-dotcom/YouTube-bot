import os
import asyncio
import requests
import subprocess

# --- AYARLAR ---
OUTPUT_NAME = "otonom_shorts.mp4"
# Senin daha önce belirttiğin karakterlerin güvenli linkleri
CHAR_LINKS = {
    "papi": "https://images.pngtree.com/png-clipart/20230913/original/pngtree-3d-orange-fish-png-image_20930822.png",
    "tori": "https://png.pngtree.com/png-clipart/20230531/original/pngtree-3d-turtle-turtle-gradient-texture-ui-design-ux-material-png-image_14115622.png",
    "fini": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzY7B9Y6p7lH9-Pz9j8_Z6J8-R8E5t1-Pz9Q&s"
}

async def build_now():
    print(">>> ADIM 1: Ses Dosyası Oluşturuluyor...")
    # Edge-TTS'i doğrudan sistem komutuyla çağırıyoruz (En güvenli yol)
    text = "Papi, Tori ve Fini! İşte otonom dünyamız nihayet sesli ve görüntülü olarak hazır!"
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')
    
    if not os.path.exists("voice.mp3"):
        print(">>> HATA: Ses dosyası oluşturulamadı!")
        return

    print(">>> ADIM 2: Karakterler İndiriliyor...")
    valid_assets = []
    for name, url in CHAR_LINKS.items():
        try:
            r = requests.get(url, timeout=15)
            with open(f"{name}.png", "wb") as f:
                f.write(r.content)
            valid_assets.append(f"{name}.png")
            print(f">>> {name} başarıyla indi.")
        except:
            print(f">>> {name} indirilemedi.")

    print(">>> ADIM 3: FFmpeg ile Render Başlıyor...")
    # Karmaşık filtreleri basitleştirdik ki 'Exit Code 1' almayalım
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=0x003366:s=720x1280:d=5", # Mavi arka plan
        "-i", "papi.png", "-i", "tori.png", "-i", "fini.png", "-i", "voice.mp3",
        "-filter_complex", 
        "[1:v]scale=300:-1[p];[2:v]scale=300:-1[t];[3:v]scale=300:-1[f];"
        "[0:v][p]overlay=210:200[bg1];"
        "[bg1][t]overlay=50:700[bg2];"
        "[bg2][f]overlay=370:700",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-map", "0:v", "-map", "4:a", "-shortest", OUTPUT_NAME
    ]
    
    subprocess.run(cmd)

    if os.path.exists(OUTPUT_NAME):
        print(f">>> BAŞARILI! Video diskte: {os.path.abspath(OUTPUT_NAME)}")
    else:
        print(">>> KRİTİK HATA: Video oluşturulamadı.")

if __name__ == "__main__":
    asyncio.run(build_now())
