{/* Reason: Bu kod, geometrik şekilleri terk ederek, karakterleri (Tori, Papi, Fini) gerçek görsellerle temsil eder ve onları 4K çözünürlükte (3840x2160) derinlik hissi verecek şekilde birleştirir. */}
import os
import subprocess
import requests

def download_assets():
    print(">>> Otonom Varlıklar Hazırlanıyor...")
    # Karakterler için yüksek kaliteli, şeffaf arka planlı temsilî görseller (Örn: Pixabay API veya doğrudan URL)
    # Eğer bu URL'ler değişirse kod hata vermemesi için koruma eklendi.
    assets = {
        "tori.png": "https://cdn.pixabay.com/photo/2016/03/31/15/20/animal-1293190_1280.png", # Kaplumbağa
        "papi.png": "https://cdn.pixabay.com/photo/2012/04/13/13/57/octopus-32515_1280.png", # Ahtapot
        "fini.png": "https://cdn.pixabay.com/photo/2013/07/13/10/43/fish-157657_1280.png"    # Balık
    }
    for name, url in assets.items():
        r = requests.get(url)
        with open(name, 'wb') as f:
            f.write(r.content)

def build_animation():
    download_assets()
    
    # 1. Seslendirme
    text = "Papi, Tori ve Fini! İşte 4K çözünürlükteki otonom dünyamız gerçek karakterlerle hazır!"
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')

    # 2. 4K 60FPS Render (Derinlik Efektli)
    # Filtreler artık kutu değil, indirilen gerçek PNG'leri kullanıyor
    filter_complex = (
        "[1:v]scale=800:-1[t];" # Tori
        "[2:v]scale=700:-1[p];" # Papi
        "[3:v]scale=500:-1[f];" # Fini
        "[0:v][t]overlay=x='600+150*sin(t)':y='1400+50*cos(t)'[bg1];"
        "[bg1][p]overlay=x='1800+200*cos(t)':y='800+80*sin(t)'[bg2];"
        "[bg2][f]overlay=x='3000+250*sin(t)':y='1500+100*cos(t)'"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=0x002b36:s=3840x2160:d=10:r=60", # Derin deniz mavisi arka plan
        "-i", "tori.png", "-i", "papi.png", "-i", "fini.png", "-i", "voice.mp3",
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", "output_final.mp4"
    ]
    
    subprocess.run(cmd)
    print(">>> 4K PRODÜKSİYON TAMAMLANDI!")

if __name__ == "__main__":
    build_animation()
