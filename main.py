import os
import asyncio
import math
import numpy as np
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
from rembg import remove
from PIL import Image
import edge_tts

async def main():
    assets_dir = "assets"
    
    def clean_image(name):
        """Arka planı otomatik siler ve şeffaf PNG yapar"""
        files = os.listdir(assets_dir)
        target = next((f for f in files if name in f.lower()), None)
        if target:
            input_path = os.path.join(assets_dir, target)
            output_path = f"cleaned_{name}.png"
            with open(input_path, 'rb') as i:
                input_data = i.read()
                output_data = remove(input_data)
                with open(output_path, 'wb') as o:
                    o.write(output_data)
            return output_path
        return None

    print("🖋️ Görseller temizleniyor...")
    papi_path = clean_image("papi")
    ahtapot_path = clean_image("tori") # tori veya ahtapot
    bg_file = next((f for f in os.listdir(assets_dir) if "arka" in f.lower() or "back" in f.lower()), None)

    # Seslendirme (Doğal Ses)
    print("🎙️ Ses hazırlanıyor...")
    text = "Selam dostlar! Ben Kaplumbağa Papi. Sonunda o teknik sorunları aştık. Yanımda dostum Ahtapot ile denizin en derin, en mavi yerindeyiz. Dostluk, zorlukları beraber aşmaktır!"
    communicate = edge_tts.Communicate(text, "tr-TR-AhmetNeural")
    await communicate.save("ses.mp3")
    audio = AudioFileClip("ses.mp3")

    # Kurgu
    bg = ImageClip(os.path.join(assets_dir, bg_file)).set_duration(40).resize(width=1920)
    
    papi = ImageClip(papi_path).set_duration(40).resize(height=450)
    papi = papi.set_position(lambda t: (300 + 20 * math.sin(t), 650 + 10 * math.cos(t)))

    katmanlar = [bg, papi]

    if ahtapot_path:
        ahtapot = ImageClip(ahtapot_path).set_duration(40).resize(height=400)
        ahtapot = ahtapot.set_position(lambda t: (1200, 550 + 25 * math.sin(t * 1.5)))
        katmanlar.append(ahtapot)

    final = CompositeVideoClip(katmanlar).set_audio(audio)
    final.write_videofile("ilk_cizgi_filmim.mp4", fps=24)
    print("✨ İşlem Tamam! Arka planlar silindi, ses eklendi.")

if __name__ == "__main__":
    asyncio.run(main())
