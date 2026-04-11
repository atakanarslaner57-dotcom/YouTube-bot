{/* Reason: Bu kod, silinen PNG dosyalarını aramak yerine onları otonom olarak indirir ve 4K çözünürlükte (3840x2160) senaryoyu canlandırır. */}
import os
import subprocess
import requests

def prepare_assets():
    print(">>> Karakterler otonom olarak hazirlaniyor...")
    # Tori (Kaplumbaga), Papi (Ahtapot) ve Fini (Balik) için yüksek kaliteli görseller
    assets = {
        "tori.png": "https://cdn.pixabay.com/photo/2016/03/31/15/20/animal-1293190_1280.png",
        "papi.png": "https://cdn.pixabay.com/photo/2012/04/13/13/57/octopus-32515_1280.png",
        "fini.png": "https://cdn.pixabay.com/photo/2013/07/13/10/43/fish-157657_1280.png"
    }
    for name, url in assets.items():
        try:
            r = requests.get(url, timeout=10)
            with open(name, 'wb') as f: f.write(r.content)
            print(f">>> {name} hazir.")
        except:
            # Yedek plan: Eger internet kesilirse hata vermemesi icin renkli alan yaratir
            os.system(f"ffmpeg -y -f lavfi -i color=c=random:s=300x300:d=1 -vframes 1 {name}")

def start_render():
    prepare_assets()
    
    # 1. Seslendirme
    text = "Selam! Ben Kaplumbaga Tori, yanimda Ahtapot Papi ve Balik Fini var. 4K animasyon dunyamiza hos geldiniz!"
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')

    # 2. 4K 60FPS Dinamik Render
    # Karakterler ekranda yüzer gibi (sine dalgasi) hareket eder
    filter_complex = (
        "[1:v]scale=700:-1[t];"
        "[2:v]scale=600:-1[p];"
        "[3:v]scale=450:-1[f];"
        "[0:v][t]overlay=x='400+120*sin(t)':y='1400+40*cos(t)'[bg1];"
        "[bg1][p]overlay=x='1800+180*cos(t)':y='800+70*sin(t)'[bg2];"
        "[bg2][f]overlay=x='2800+220*sin(t)':y='1500+90*cos(t)'"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=0x001a33:s=3840x2160:d=10:r=60", # 4K Arka Plan
        "-i", "tori.png", "-i", "papi.png", "-i", "fini.png", "-i", "voice.mp3",
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a aac", "-shortest", "final_animation_4k.mp4"
    ]
    
    subprocess.run(cmd)
    print(">>> RENDER TAMAMLANDI!")

if __name__ == "__main__":
    start_render()
