import os
import requests
import subprocess

def download_file(url, filename):
    try:
        r = requests.get(url, timeout=15)
        with open(filename, 'wb') as f:
            f.write(r.content)
        return True
    except:
        return False

def build_video():
    # 1. Seslendirme (edge-tts)
    text = "Selam Papi, Tori ve Fini! Sonunda butun hatalari giderdik!"
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')

    # 2. Karakterleri Indir
    links = {
        "papi.png": "https://images.pngtree.com/png-clipart/20230913/original/pngtree-3d-orange-fish-png-image_20930822.png",
        "tori.png": "https://png.pngtree.com/png-clipart/20230531/original/pngtree-3d-turtle-turtle-gradient-texture-ui-design-ux-material-png-image_14115622.png",
        "fini.png": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzY7B9Y6p7lH9-Pz9j8_Z6J8-R8E5t1-Pz9Q&s"
    }
    
    for filename, url in links.items():
        download_file(url, filename)

    # 3. FFmpeg Render (En sade ve hatasız komut)
    cmd = (
        "ffmpeg -y -f lavfi -i color=c=0x003366:s=720x1280:d=5 "
        "-i papi.png -i tori.png -i fini.png -i voice.mp3 "
        '-filter_complex "[1:v]scale=300:-1[p];[2:v]scale=300:-1[t];[3:v]scale=300:-1[f];'
        '[0:v][p]overlay=210:200[bg1];[bg1][t]overlay=50:700[bg2];[bg2][f]overlay=370:700" '
        "-c:v libx264 -pix_fmt yuv420p -c:a aac -shortest otonom_shorts.mp4"
    )
    
    subprocess.run(cmd, shell=True)
    print("Islem tamamlandi.")

if __name__ == "__main__":
    build_video()
