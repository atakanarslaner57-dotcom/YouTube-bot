import asyncio
import math
from moviepy.editor import ColorClip, CompositeVideoClip, AudioFileClip, concatenate_audioclips
import edge_tts

async def ses_ureti():
    # Karakterler ve replikleri (Hicbir ses dosyasina ihtiyac yok, anlik uretilir)
    diyaloglar = [
        ("Papi", "Selam Tori! Artik hicbir resme ihtiyacimiz yok, her seyi biz yaratiyoruz!", "tr-TR-AhmetNeural", "+15Hz"),
        ("Tori", "Haklisin Papi... Gercek guc, kodun icindeki hayal gucudur.", "tr-TR-EmelNeural", "-10Hz"),
        ("Fini", "Ve ben de en hizli baligim! Hadi yuzelim!", "tr-TR-EmelNeural", "+30Hz")
    ]
    
    sesler = []
    for i, (isim, metin, ses, perde) in enumerate(diyaloglar):
        dosya = f"ses_{i}.mp3"
        comm = edge_tts.Communicate(metin, ses, pitch=perde)
        await comm.save(dosya)
        sesler.append(AudioFileClip(dosya))
    
    return concatenate_audioclips(sesler)

async def main():
    print("🎬 Otonom uretim basliyor...")
    audio = await ses_ureti()
    sure = audio.duration

    # SAHNE 1: Derin Deniz Arka Plani (Koyu Mavi)
    bg = ColorClip(size=(1080, 1920), color=(0, 30, 70)).set_duration(sure)

    # TORI: Yesil Kare (Kaplumbaga - Agir ve bilge)
    tori = ColorClip(size=(400, 250), color=(34, 139, 34)).set_duration(sure)
    tori = tori.set_position(lambda t: ('center', 1200 + 15 * math.sin(t)))

    # PAPI: Turuncu Kare (Ahtapot - Enerjik)
    papi = ColorClip(size=(300, 300), color=(255, 69, 0)).set_duration(sure)
    papi = papi.set_position(lambda t: (250 + 40 * math.cos(t*2), 700 + 60 * math.sin(t*3)))

    # FINI: Sari Kare (Balik - Cok hizli)
    fini = ColorClip(size=(120, 80), color=(255, 215, 0)).set_duration(sure)
    fini = fini.set_position(lambda t: (800 + 120 * math.sin(t*5), 900 + 100 * math.cos(t*2)))

    # KURGU
    video = CompositeVideoClip([bg, tori, papi, fini], size=(1080, 1920)).set_audio(audio)
    video.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")
    print("✅ Bitti! Dosya: otonom_shorts.mp4")

if __name__ == "__main__":
    asyncio.run(main())
