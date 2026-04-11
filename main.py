import os
import subprocess
import requests

def build_video():
    print(">>> ADIM 1: Ses olusturuluyor...")
    text = "Selam Papi, Tori ve Fini! Artik butun hatalari geride biraktik, videonuz hazir!"
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')

    # Karakter linklerini yedekliyoruz
    links = {
        "papi.png": "https://raw.githubusercontent.com/runwayml/stable-diffusion-v1-5/main/docs/overview.png",
        "tori.png": "https://raw.githubusercontent.com/runwayml/stable-diffusion-v1-5/main/docs/overview.png",
        "fini.png": "https://raw.githubusercontent.com/runwayml/stable-diffusion-v1-5/main/docs/overview.png"
    }
    
    # 2. Resimleri indir, inmezse bos dosya olustur (Cokmeyi onlemek icin)
    for filename, url in links.items():
        try:
            r = requests.get(url, timeout=5)
            with open(filename, 'wb') as f: f.write(r.content)
        except:
            # Eger internet hatasi olursa bos bir gorsel yarat (Hata almamak icin kritik)
            os.system(f"ffmpeg -f lavfi -i color=c=red:s=100x100:d=1 -vframes 1 {filename}")

    print(">>> ADIM 3: FFmpeg ile Video 'Civileniyor'...")
    # MoviePy'i tamamen terk ettik, dogrudan sistem motorunu (FFmpeg) kullaniyoruz
    cmd = (
        "ffmpeg -y -f lavfi -i color=c=0x002B36:s=720x1280:d=5 "
        "-i papi.png -i tori.png -i fini.png -i voice.mp3 "
        '-filter_complex "[1:v]scale=300:-1[p];[2:v]scale=300:-1[t];[3:v]scale=300:-1[f];'
        '[0:v][p]overlay=210:300[bg1];[bg1][t]overlay=50:800[bg2];[bg2][f]overlay=370:800" '
        "-c:v libx264 -pix_fmt yuv420p -c:a aac -shortest otonom_shorts.mp4"
    )
    
    subprocess.run(cmd, shell=True)
    print(">>> ISLEM TAMAMLANDI!")

if __name__ == "__main__":
    build_video()
