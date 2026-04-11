import os
import asyncio
import requests
import subprocess

# --- AYARLAR ---
# Gemini anahtarını buraya tırnak içinde yapıştırabilirsin
GEMINI_API_KEY = "BURAYA_GEMINI_API_KEYINI_YAZ" 

CHAR_LINKS = {
    "papi": "https://images.pngtree.com/png-clipart/20230913/original/pngtree-3d-orange-fish-png-image_20930822.png",
    "tori": "https://png.pngtree.com/png-clipart/20230531/original/pngtree-3d-turtle-turtle-gradient-texture-ui-design-ux-material-png-image_14115622.png",
    "fini": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzY7B9Y6p7lH9-Pz9j8_Z6J8-R8E5t1-Pz9Q&s"
}

async def build_ultimate_video():
    print(">>> 1. Ses oluşturuluyor...")
    # Seslendirme için en stabil ses: Emel
    text = "Papi, Tori ve Fini! İşte gerçek otonom dünyamız hem sesli hem görüntülü hazır!"
    # edge-tts CLI kullanarak doğrudan ses dosyasını yazdırıyoruz
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')
    
    print(">>> 2. Karakterler indiriliyor...")
    for name, url in CHAR_LINKS.items():
        try:
            r = requests.get(url, timeout=10)
            with open(f"{name}.png", "wb") as f:
                f.write(r.content)
        except:
            print(f">>> {name} indirilemedi, varsayılan kullanılacak.")

    print(">>> 3. FFmpeg ile Render Başlıyor...")
    # Bu komut: Arka planı oluşturur, resimleri üst üste koyar ve sesi ekler.
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=0x002850:s=720x1280:d=5", # Mavi arka plan
        "-i", "papi.png", "-i", "tori.png", "-i", "fini.png", "-i", "voice.mp3",
        "-filter_complex", 
        "[1:v]scale=400:-1[p];[2:v]scale=350:-1[t];[3:v]scale=350:-1[f];"
        "[0:v][p]overlay=(W-w)/2:200[bg1];"
        "[bg1][t]overlay=50:700[bg2];"
        "[bg2][f]overlay=350:700",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "otonom_shorts.mp4"
    ]
    
    subprocess.run(ffmpeg_cmd)
    
    if os.path.exists("otonom_shorts.mp4"):
        print(">>> BAŞARILI: otonom_shorts.mp4 oluşturuldu!")
    else:
        print(">>> HATA: Video oluşturulamadı.")

if __name__ == "__main__":
    asyncio.run(build_ultimate_video())
