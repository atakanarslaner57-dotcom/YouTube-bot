import os
import requests
import subprocess

def build_video():
    print(">>> Islem basliyor...")
    
    # 1. Seslendirme (En stabil yontem)
    text = "Selam Papi, Tori ve Fini! Sonunda butun sistem hatalarini giderdik, animasyonumuz hazir!"
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')

    # 2. Karakterleri Indir
    # Linkler direkt PNG dosyalarina gider
    links = {
        "papi.png": "https://images.pngtree.com/png-clipart/20230913/original/pngtree-3d-orange-fish-png-image_20930822.png",
        "tori.png": "https://png.pngtree.com/png-clipart/20230531/original/pngtree-3d-turtle-turtle-gradient-texture-ui-design-ux-material-png-image_14115622.png",
        "fini.png": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzY7B9Y6p7lH9-Pz9j8_Z6J8-R8E5t1-Pz9Q&s"
    }
    
    for filename, url in links.items():
        print(f">>> {filename} indiriliyor...")
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)

    # 3. FFmpeg ile Render (MoviePy kullanmadan, dogrudan sistem komutu)
    # Bu komut arka plani olusturur ve karakterleri uzerine dizer
    cmd = (
        "ffmpeg -y -f lavfi -i color=c=0x003366:s=720x1280:d=5 "
        "-i papi.png -i tori.png -i fini.png -i voice.mp3 "
        '-filter_complex "[1:v]scale=350:-1[p];[2:v]scale=350:-1[t];[3:v]scale=350:-1[f];'
        '[0:v][p]overlay=(W-w)/2:250[bg1];[bg1][t]overlay=50:800[bg2];[bg2][f]overlay=320:800" '
        "-c:v libx264 -pix_fmt yuv420p -c:a aac -shortest otonom_shorts.mp4"
    )
    
    subprocess.run(cmd, shell=True)
    print(">>> BAŞARILI: otonom_shorts.mp4 olusturuldu.")

if __name__ == "__main__":
    build_video()
