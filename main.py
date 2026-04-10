import os
import asyncio
import edge_tts
import math
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, vfx

# 1. ÜCRETSİZ SES ÜRETİCİ (Microsoft Edge TTS)
async def generate_audio(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    return AudioFileClip(filename)

# 2. RESMİ CANLANDIRAN FONKSİYON
def create_scene(bg_resmi, karakter_resmi, ses_dosyasi, scale_factor=0.6):
    duration = ses_dosyasi.duration
    
    # Arka Plan (assets klasöründen alır)
    bg = ImageClip(f"assets/{bg_resmi}").set_duration(duration).resize(width=1920)
    
    # Karakter (assets klasöründen alır)
    char = ImageClip(f"assets/{karakter_resmi}").set_duration(duration).resize(height=500)
    
    # Karakterin Yüzme Hareketi (Yumuşak salınım efekti)
    char = char.set_position(lambda t: (
        "center", 
        400 + 30 * math.sin(t * 3) # Yukarı aşağı hareket
    ))

    return CompositeVideoClip([bg, char]).set_audio(ses_dosyasi)

async def main():
    # Karakter sesleri (Ücretsiz ve doğal)
    # tr-TR-AhmetNeural (Erkek), tr-TR-EmelNeural (Kadın)
    
    print("🎙️ Sesler ve sahneler hazırlanıyor...")
    
    # 1. Sahne: Papi konuşuyor
    s1_ses = await generate_audio("Merhaba arkadaşlar! Ben Papi. Bu mavi derinliklerde keşfedilecek çok şey var!", "tr-TR-AhmetNeural", "papi_ses.mp3")
    sahne1 = create_scene("background.avif", "papi.avif", s1_ses)
    
    # 2. Sahne: Fini konuşuyor
    s2_ses = await generate_audio("Ben de geliyorum Papi! Mercanların arasından geçmek çok eğlenceli!", "tr-TR-EmelNeural", "fini_ses.mp3")
    sahne2 = create_scene("background.avif", "fini.avif", s2_ses)

    # Videoları Birleştir
    from moviepy.editor import concatenate_videoclips
    final_video = concatenate_videoclips([sahne1, sahne2], method="compose")
    
    # Videoyu Kaydet
    print("🎬 Video oluşturuluyor...")
    final_video.write_videofile("ilk_cizgi_filmim.mp4", fps=24, codec="libx264")
    print("✅ BAŞARILI: 'ilk_cizgi_filmim.mp4' hazır!")

if __name__ == "__main__":
    # Gerekli kütüphaneyi yüklemek için: pip install edge-tts moviepy
    asyncio.run(main())
