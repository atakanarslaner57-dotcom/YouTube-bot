import os
import subprocess

def build_4k_animation():
    print(">>> 4K Otonom Animasyon Basliyor...")

    # 1. Seslendirme (Karakterlerin tanitimi)
    text = "Selam! Ben Kaplumbaga Tori, yanimda Ahtapot Papi ve Balik Fini var. 4K dunyamiza hos geldiniz!"
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')

    # 2. KARAKTERLERI KODLA YARAT (PNG dosyasi gerektirmez)
    # Tori (Yesil), Papi (Turuncu), Fini (Mavi) karakterlerini temsil eden dinamik objeler
    chars = {
        "tori": "color=c=green:s=300x200",
        "papi": "color=c=orange:s=250x250",
        "fini": "color=c=dodgerblue:s=200x150"
    }
    
    for name, cmd in chars.items():
        os.system(f"ffmpeg -y -f lavfi -i {cmd}:d=1 -vframes 1 {name}.png")

    # 3. 4K RENDER MOTORU (3840x2160)
    # Karakterlere suyun altinda hareket (sine dalgasi) efekti ekler
    ffmpeg_cmd = (
        "ffmpeg -y -f lavfi -i color=c=0x001a33:s=3840x2160:d=10:r=60 " # 4K 60FPS Arka Plan
        "-i tori.png -i papi.png -i fini.png -i voice.mp3 "
        "-filter_complex "
        "[1:v]format=rgba,geom=300x200[t];"
        "[2:v]format=rgba,geom=250x250[p];"
        "[3:v]format=rgba,geom=200x150[f];"
        "[0:v][t]overlay=x='200+50*sin(t)':y='1500+20*cos(t)'[v1]; " # Tori hareketi
        "[v1][p]overlay=x='1800+100*sin(t)':y='800+50*cos(t)'[v2]; "  # Papi hareketi
        "[v2][f]overlay=x='3000+150*cos(t)':y='1600+80*sin(t)' "      # Fini hareketi
        "-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -shortest otonom_4k.mp4"
    )

    subprocess.run(ffmpeg_cmd, shell=True)
    print(">>> 4K VIDEO HAZIR: otonom_4k.mp4")

if __name__ == "__main__":
    build_4k_animation()
