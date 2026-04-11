import os
import asyncio
import math
import subprocess
import sys

# 1. Ortam Yaması (ANTIALIAS Hatası İçin)
try:
    import PIL.Image
    if not hasattr(PIL.Image, 'ANTIALIAS'):
        PIL.Image.ANTIALIAS = getattr(PIL.Image, 'LANCZOS', None)
except:
    pass

from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
import edge_tts

async def main():
    print("🎬 Profesyonel video üretimi akıllı modda başlıyor...")
    
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        print("❌ HATA: assets klasörü bulunamadı!")
        return

    files = os.listdir(assets_dir)
    print(f"📁 Klasördeki dosyalar: {files}")

    # --- AKILLI DOSYA BULUCU ---
    # İsimlerin içinde geçen kelimelere göre dosyaları otomatik seçer
    bg_file = next((f for f in files if "arka" in f.lower() or "back" in f.lower()), None)
    papi_file = next((f for f in files if "papi" in f.lower()), None)
    ahtapot_file = next((f for f in files if "ahtapot" in f.lower() or "tori" in f.lower()), None)

    if not bg_file or not papi_file:
        print(f"❌ KRİTİK HATA: Arka plan veya Papi dosyası bulunamadı!")
        return

    # 2. Seslendirme (Doğal ve Akıcı Ton)
    print("🎙️ Seslendirme oluşturuluyor...")
    text = (
        "Selam dostlar! Ben Kaplumbağa Papi. Bugün denizin derinliklerinde harika bir gün. "
        "Dostum Ahtapot ile birlikte mercanların arasında süzülüyoruz. "
        "Unutmayın, en büyük dalgalarda bile yanınızda bir dostunuz varsa yolculuk hep huzurludur."
    )
    # En doğal Türkçe seslerden biri
    communicate = edge_tts.Communicate(text, "tr-TR-AhmetNeural")
    await communicate.save("final_ses.mp3")
    audio = AudioFileClip("final_ses.mp3")

    # 3. Görsel Kurgu
    print("🖼️ Sahneler birleştiriliyor...")
    
    # Arka Plan
    bg = ImageClip(os.path.join(assets_dir, bg_file)).set_duration(audio.duration).resize(width=1920)
    
    # Papi (Sol alt - Yüzme hareketi)
    papi = ImageClip(os.path.join(assets_dir, papi_file)).set_duration(audio.duration).resize(height=450)
    papi = papi.set_position(lambda t: (300 + 15 * math.sin(t), 600 + 10 * math.cos(t)))

    # Ahtapot (Sağ alt - Süzülme hareketi)
    clips = [bg, papi]
    if ahtapot_file:
        ahtapot = ImageClip(os.path.join(assets_dir, ahtapot_file)).set_duration(audio.duration).resize(height=400)
        ahtapot = ahtapot.set_position(lambda t: (1200, 550 + 25 * math.sin(t * 1.5)))
        clips.append(ahtapot)

    # 4. Final Kayıt
    final_video = CompositeVideoClip(clips).set_audio(audio)
    output_name = "papi_ve_dostu_final.mp4"
    final_video.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")
    
    print(f"✨ BAŞARILI! Video hazır: {output_name}")

if __name__ == "__main__":
    asyncio.run(main())
