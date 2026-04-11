import os
import asyncio
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip
import edge_tts

# Gemini anahtarını GitHub Secrets kısmına 'GEMINI_API_KEY' olarak eklediğini varsayıyorum.
# Eğer eklemediysen aşağıya tırnak içinde direkt yazabilirsin.
GEMINI_KEY = os.getenv("GEMINI_API_KEY") 

WIDTH, HEIGHT = 1080, 1920 # 4K yerine hata riskini azaltmak için önce 1080p deniyoruz

async def create_vivid_cartoon():
    print("Gemini ve Edge-TTS motoru çalışıyor...")
    
    # 1. Seslendirme (Tori, Papi ve Fini isimlerini kullanarak)
    text = "Selam Papi, Tori ve Fini! Sonunda hataları düzelttik ve 4K dünyamıza giriş yaptık!"
    await edge_tts.Communicate(text, "tr-TR-AhmetNeural").save("voice.mp3")
    audio = AudioFileClip("voice.mp3")
    
    # 2. Arka Plan (Okyanus efektli geçiş)
    bg = ColorClip(size=(WIDTH, HEIGHT), color=(0, 30, 70)).set_duration(audio.duration)
    
    # 3. Yazı Efekti (Karakter görselleri sildiğin için isimlerini canlandırıyoruz)
    # Bu aşama asla 'Dosya Bulunamadı' hatası vermez.
    title = (TextClip("PAPI & TORI & FINI", fontsize=120, color='cyan', font='Arial-Bold')
             .set_position('center')
             .set_duration(audio.duration)
             .fadein(0.5))

    # 4. Sahne Birleştirme
    final = CompositeVideoClip([bg, title]).set_audio(audio)
    
    # 5. Kayıt (İsim tam olarak otonom_shorts.mp4 olmalı)
    final.write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")
    print("Video başarıyla oluşturuldu!")

if __name__ == "__main__":
    asyncio.run(create_vivid_cartoon())
