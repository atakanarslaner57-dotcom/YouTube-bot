import os
import subprocess

def create_4k_production():
    print(">>> 4K Prodüksiyon Hattı Aktif...")

    # 1. Seslendirme (Kristal Netlikte)
    text = "Papi, Tori ve Fini! İşte 4K çözünürlükte, otonom dünyamız nihayet hazır!"
    os.system(f'edge-tts --text "{text}" --voice tr-TR-EmelNeural --write-media voice.mp3')

    # 2. Karakterleri 4K Kalitesinde Kodla Yarat (PNG gerektirmez)
    # Tori (Yeşil), Papi (Turuncu), Fini (Mavi)
    os.system("ffmpeg -y -f lavfi -i color=c=0x228B22:s=600x400:d=1 -vframes 1 tori.png")
    os.system("ffmpeg -y -f lavfi -i color=c=0xFF4500:s=500x500:d=1 -vframes 1 papi.png")
    os.system("ffmpeg -y -f lavfi -i color=c=0x1E90FF:s=400x300:d=1 -vframes 1 fini.png")

    # 3. 4K 60FPS Render Komutu (YouTube Yatay Format)
    # Karakterlere suyun altında yüzme (dalgalanma) hareketi verir
    cmd = (
        "ffmpeg -y -f lavfi -i color=c=0x000033:s=3840x2160:d=10:r=60 " # 4K 60fps Arka Plan
        "-i tori.png -i papi.png -i fini.png -i voice.mp3 "
        "-filter_complex "
        "[1:v]format=rgba,scale=600:-1[t];"
        "[2:v]format=rgba,scale=500:-1[p];"
        "[3:v]format=rgba,scale=400:-1[f];"
        "[0:v][t]overlay=x='500+100*sin(t)':y='1500+30*cos(t)'[bg1]; " # Tori Hareketi
        "[bg1][p]overlay=x='1800+150*cos(t)':y='800+60*sin(t)'[bg2]; " # Papi Hareketi
        "[bg2][f]overlay=x='3000+200*sin(t)':y='1600+100*cos(t)' "     # Fini Hareketi
        "-c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -c:a aac -shortest output_4k_final.mp4"
    )

    subprocess.run(cmd, shell=True)
    print(">>> 4K VIDEO TAMAMLANDI: output_4k_final.mp4")

if __name__ == "__main__":
    create_4k_production()
