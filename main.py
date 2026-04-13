import os
import subprocess
import requests

def prepare_assets():
    # Karakterleri (Tori, Papi, Fini) otonom olarak indirir
    assets = {
        "tori.png": "https://cdn.pixabay.com/photo/2016/03/31/15/20/animal-1293190_1280.png",
        "papi.png": "https://cdn.pixabay.com/photo/2012/04/13/13/57/octopus-32515_1280.png",
        "fini.png": "https://cdn.pixabay.com/photo/2013/07/13/10/43/fish-157657_1280.png"
    }
    for name, url in assets.items():
        r = requests.get(url, timeout=15)
        with open(name, 'wb') as f: f.write(r.content)

def start_render():
    prepare_assets()
    # Seslendirme
    text = "Selam! Ben Kaplumbaga Tori, yanimda Ahtapot Papi ve Balik Fini var. 4K animasyon dunyamiza hos geldiniz!"
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')

    # 4K 60FPS Dinamik Render
    # Filtreleri tırnak hatası olmayacak şekilde basitleştirdik
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
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "final_animation_4k.mp4"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    start_render()
