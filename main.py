import os
import asyncio
import requests
import subprocess

# --- AYARLAR ---
OUTPUT_NAME = "otonom_shorts.mp4"
CHAR_LINKS = {
    "papi": "https://images.pngtree.com/png-clipart/20230913/original/pngtree-3d-orange-fish-png-image_20930822.png",
    "tori": "https://png.pngtree.com/png-clipart/20230531/original/pngtree-3d-turtle-turtle-gradient-texture-ui-design-ux-material-png-image_14115622.png",
    "fini": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzY7B9Y6p7lH9-Pz9j8_Z6J8-R8E5t1-Pz9Q&s"
}

async def make_it_work():
    print(">>> 1. Ses oluşturuluyor...")
    text = "Papi, Tori ve Fini! İşte o çok beklediğimiz otonom dünyamız hem sesli hem görüntülü hazır!"
    # Ahmet sesi yerine daha stabil olan emel sesini deneyelim
    await subprocess.run(["edge-tts", "--text", text, "--voice", "tr-TR-EmelNeural", "--write-media", "voice.mp3"])
    
    print(">>> 2. Karakterler indiriliyor...")
    for name, url in CHAR_LINKS.items():
        r = requests.get(url)
        with open(f"{name}.png", "wb") as f:
            f.write(r.content)

    print(">>> 3. FFmpeg ile Render Başlıyor...")
    # Bu komut: Mavi arka plan oluşturur, karakterleri üzerine dizer ve sesi ekler.
    # MoviePy kullanmadığımız için hata alma şansı %0'a yakın.
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=0x002850:s=720x1280:d=5", # 5 saniye mavi ekran
        "-i", "papi.png", "-i", "tori.png", "-i", "fini.png", "-i", "voice.mp3",
        "-filter_complex", 
        "[1:v]scale=400:-1[p];[2:v]scale=350:-1[t];[3:v]scale=350:-1[f];"
        "[0:v][p]overlay=(W-w)/2:200[bg1];"
        "[bg1][t]overlay=50:700[bg2];"
        "[bg2][f]overlay=350:700",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", OUTPUT_NAME
    ]
    
    subprocess.run(ffmpeg_cmd)
    
    if os.path.exists(OUTPUT_NAME):
        print(f">>> BAŞARILI: {OUTPUT_NAME} oluşturuldu!")
    else:
        print(">>> HATA: Video yine oluşmadı.")

if __name__ == "__main__":
    asyncio.run(make_it_work())
