import os
import asyncio
import requests
from moviepy.editor import ColorClip, ImageClip, AudioFileClip, CompositeVideoClip
import edge_tts

# --- AYARLAR ---
OUTPUT_NAME = "otonom_shorts.mp4"

# Karakter linklerini daha güvenli olanlarla güncelledim
CHAR_LINKS = {
    "Papi": "https://raw.githubusercontent.com/runwayml/stable-diffusion-v1-5/main/docs/overview.png", # Örnek link, geçici
    "Tori": "https://raw.githubusercontent.com/runwayml/stable-diffusion-v1-5/main/docs/overview.png",
    "Fini": "https://raw.githubusercontent.com/runwayml/stable-diffusion-v1-5/main/docs/overview.png"
}

async def make_final_check():
    print(">>> Animasyon Motoru Başlatıldı...")
    
    # 1. Ses Dosyası Kontrolü
    try:
        print(">>> Ses oluşturuluyor...")
        text = "Papi, Tori ve Fini! İşte gerçek otonom dünyamız hazır!"
        await edge_tts.Communicate(text, "tr-TR-AhmetNeural").save("voice.mp3")
        if os.path.exists("voice.mp3"):
            print(">>> Ses dosyası BAŞARIYLA oluşturuldu.")
        audio = AudioFileClip("voice.mp3")
    except Exception as e:
        print(f">>> SES HATASI: {e}")
        return

    # 2. Arka Plan Hazırlığı
    print(">>> Arka plan hazırlanıyor...")
    bg = ColorClip(size=(720, 1280), color=(0, 50, 100)).set_duration(audio.duration)

    # 3. Video Render Denemesi
    try:
        print(">>> Video render işlemi başlıyor (Bu biraz sürebilir)...")
        # Karakterler yüklenemese bile video boş kalmasın diye sadece arka planı basıyoruz
        final_video = CompositeVideoClip([bg]).set_audio(audio)
        
        # En düşük ve en güvenli render ayarları
        final_video.write_videofile(OUTPUT_NAME, fps=24, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
        
        if os.path.exists(OUTPUT_NAME):
            print(f">>> TEBRİKLER! {OUTPUT_NAME} dosyası diskte oluşturuldu.")
        else:
            print(f">>> KRİTİK HATA: Render bitti ama {OUTPUT_NAME} DOSYASI YOK!")
            
    except Exception as e:
        print(f">>> RENDER HATASI: {e}")

if __name__ == "__main__":
    asyncio.run(make_final_check())
