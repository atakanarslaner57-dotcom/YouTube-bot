import asyncio
import math
from moviepy.editor import ColorClip, CompositeVideoClip, AudioFileClip, TextClip, concatenate_audioclips
import edge_tts

async def uret_sesler():
    # Karakterler ve replikleri
    diyaloglar = [
        ("Papi", "Selam Tori! YouTube dünyasına dikey bir giriş yaptık, harika görünüyoruz!", "tr-TR-AhmetNeural", "+15Hz"),
        ("Tori", "Acele etme Papi... Derin suların huzuru, her ekrana sığar.", "tr-TR-EmelNeural", "-10Hz"),
        ("Fini", "Hey, ben de buradayım! Hadi mercanların arasına kaçalım!", "tr-TR-EmelNeural", "+25Hz")
    ]
    
    ses_dosyalari = []
    for i, (isim, metin, ses, perde) in enumerate(diyaloglar):
        dosya = f"ses_{i}.mp3"
        comm = edge_tts.Communicate(metin, ses, pitch=perde)
        await comm.save(dosya)
        ses_dosyalari.append(AudioFileClip(dosya))
    
    return concatenate_audioclips(ses_dosyalari)

def karakter_yap(renk, boy, isim):
    # Basit bir renk bloğunu karakterimiz olarak tanımlıyoruz
    return ColorClip(size=(boy, boy), color=renk).set_duration(10)

async def main():
    print("🚀 Animasyon motoru baslatiliyor...")
    final_audio = await uret_sesler()
    sure = final_audio.duration

    # Arka Plan: Koyu Lacivert Deniz (1080x1920)
    bg = ColorClip(size=(1080, 1920), color=(0, 20, 50)).set_duration(sure)

    # Karakterler (Görsel yüklemeden otonom tasarım)
    # Tori: Yesil (Bilge Kaplumbaga)
    tori = ColorClip(size=(450, 300), color=(40, 150, 40)).set_duration(sure)
    tori = tori.set_position(lambda t: ('center', 1100 + 20 * math.sin(t)))

    # Papi: Turuncu (Enerjik Ahtapot)
    papi = ColorClip(size=(350, 350), color=(255, 120, 0)).set_duration(sure)
    papi = papi.set_position(lambda t: (300 + 50 * math.cos(t*2), 600 + 40 * math.sin(t*3)))

    # Fini: Sari (Neseli Balik)
    fini = ColorClip(size=(150, 100), color=(255, 255, 0)).set_duration(sure)
    fini = fini.set_position(lambda t: (800 + 100 * math.sin(t*4), 800 + 150 * math.cos(t*2)))

    # Kurgu ve Kayit
    video = CompositeVideoClip([bg, tori, papi, fini], size=(1080, 1920)).set_audio(final_audio)
    video.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")
    print("✅ Video basariyla kaydedildi: otonom_shorts.mp4")

if __name__ == "__main__":
    asyncio.run(main())
