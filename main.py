{/* Reason: Bu kod, silinen veya engellenen PNG dosyalarını otonom olarak indirir ve 4K çözünürlükte (3840x2160) senaryoyu canlandırır. */}
import os
import subprocess
import requests

def prepare_assets():
    print(">>> Karakterler otonom olarak hazirlaniyor...")
    # Tori (Kaplumbaga), Papi (Ahtapot) ve Fini (Balik) için yüksek kaliteli görseller
    assets = {
        "tori.png": "https://cdn.pixabay.com/photo/2016/03/31/15/20/animal-1293190_1280.png",
        "papi.png": "https://cdn.pixabay.com/photo/2012/04/13/13/57/octopus-32515_1280.png",
        "fini.png": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzY7B9Y6p7lH9-Pz9j8_Z6J8-R8E5t1-Pz9Q&s"
    }
    for name, url in assets.items():
        try:
            r = requests.get(url, timeout=10)
            with open(name, 'wb') as f: f.write(r.content)
            print(f">>> {name} hazir.")
        except:
            # Yedek plan: Eger internet kesilirse hata vermemesi icin renkli alan yaratir
            os.system(f"ffmpeg -y -f lavfi -i color=c=random:s=300x300:d=1 -vframes 1 {name}")

def build_4k_animation():
    print(">>> 4K Otonom Animasyon Basliyor...")
    prepare_assets()

    # 1. Seslendirme (Karakterlerin tanitimi)
    text = "Selam Papi, Tori ve Fini! İşte 4K çözünürlükteki, otonom dünyamız nihayet hem sesli hem görüntülü hazır!"
    # En stabil yontem
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')

    # 2. 4K RENDER MOTORU (3840x2160)
    # Karakterlere suyun altinda hareket (sine dalgasi) efekti ekler
    ffmpeg_cmd = (
        "ffmpeg -y -f lavfi -i color=c=0x001a33:s=3840x2160:d=10:r=60 " # 4K 60FPS Arka Plan
        "-i tori.png -i papi.png -i fini.png -i voice.mp3 "
        "-filter_complex "
        "[1:v]scale=700:-1[t];"
        "[2:v]scale=600:-1[p];"
        "[3:v]scale=450:-1[f];"
        "[0:v][t]overlay=x='400+120*sin(t)':y='1400+40*cos(t)'[bg1]; " # Tori hareketi
        "[bg1][p]overlay=x='1800+180*cos(t)':y='800+70*sin(t)'[bg2]; "  # Papi hareketi
        "[bg2][f]overlay=x='2800+220*sin(t)':y='1500+90*cos(t)' "      # Fini hareketi
        "-c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -c:a aac -shortest output_4k_final.mp4"
    )

    subprocess.run(ffmpeg_cmd, shell=True)
    print(">>> 4K VIDEO TAMAMLANDI: output_4k_final.mp4")

if __name__ == "__main__":
    build_4k_animation()
