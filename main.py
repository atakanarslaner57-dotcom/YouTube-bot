import os
import requests
import asyncio
import time
from moviepy.editor import ImageClip, AudioFileClip
import edge_tts

# --- AYARLAR ---
HF_TOKEN = "BURAYA_HF_TOKENINI_YAZ"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
OUTPUT_VIDEO = "otonom_shorts.mp4"

def generate_3d_scene(prompt, filename):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Sunucu meşgulse 3 kez tekrar deneme yapar
    for attempt in range(3):
        print(f"Deneme {attempt + 1}: Görsel oluşturuluyor...")
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return True
        elif response.status_code == 503: # Sunucu yükleniyor hatası
            print("Sunucu hazırlanıyor, 20 saniye bekleniyor...")
            time.sleep(20)
        else:
            print(f"Hata Kodu: {response.status_code}")
            break
    return False

async def make_movie():
    # Sahne Tanımı: Papi, Tori ve Fini bir arada
    scene_prompt = (
        "3D animation masterpiece, Pixar style, vivid colors, cinematic lighting. "
        "A cute purple octopus with big eyes (Papi), a bright turquoise sea turtle (Tori), "
        "and a cheerful orange fish (Fini) swimming together in a 4K underwater kingdom. "
        "Vertical 9:16 aspect ratio."
    )
    
    if generate_3d_scene(scene_prompt, "vivid_scene.png"):
        # Seslendirme
        metin = "Tori, Papi, Fini! İşte hayal ettiğimiz o muhteşem 4K dünyası!"
        await edge_tts.Communicate(metin, "tr-TR-AhmetNeural").save("voice.mp3")
        
        # Videoyu Oluştur
        audio = AudioFileClip("voice.mp3")
        # Görselin varlığını kontrol et
        if os.path.exists("vivid_scene.png"):
            clip = ImageClip("vivid_scene.png").set_duration(audio.duration).set_audio(audio)
            clip.write_videofile(OUTPUT_VIDEO, fps=24, codec="libx264", bitrate="15M")
            print("Video başarıyla oluşturuldu!")
        else:
            print("Görsel dosyası diskte bulunamadı!")
    else:
        print("Görsel üretimi başarısız oldu, video oluşturulamıyor.")

if __name__ == "__main__":
    asyncio.run(make_movie())
