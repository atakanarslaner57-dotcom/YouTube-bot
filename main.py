import os
import requests
import asyncio
from moviepy.editor import ImageClip, AudioFileClip
import edge_tts

# --- AYARLAR ---
# Buraya Hugging Face'den aldığın hf_... kodunu yapıştır
HF_TOKEN = "BURAYA_HF_TOKENINI_YAZ"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate_3d_scene(prompt, filename):
    """Yapay zekaya bağlanıp 4K, 3D çizgi film karesi üretir."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"guidance_scale": 7.5}}
    
    print(f"Sahne çiziliyor: {prompt[:30]}...")
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        return True
    return False

async def make_pro_cartoon():
    # 1. Sahne Tasarımı (Prompt)
    # Burada botun ne çizeceğini 'Pixar style', '4K', '3D render' gibi kelimelerle zorluyoruz.
    scene_prompt = (
        "High-end 3D animation style, Pixar inspired, underwater ocean depth, "
        "a cute purple octopus with big eyes, a colorful sea turtle, and a bright orange fish "
        "swimming together. Cinematic lighting, bubbles, 4K, vivid colors, vertical 9:16."
    )
    
    # 2. Görsel Üretimi
    if not generate_3d_scene(scene_prompt, "vivid_scene.png"):
        print("Hata: Anahtar yanlış veya sunucu meşgul!")
        return

    # 3. Seslendirme (Daha vurgulu)
    text = "Tori, Papi, Fini! İşte hayal ettiğimiz o muhteşem 4K dünyası!"
    await edge_tts.Communicate(text, "tr-TR-AhmetNeural").save("pro_voice.mp3")

    # 4. Videoyu Birleştir
    audio = AudioFileClip("pro_voice.mp3")
    video = ImageClip("vivid_scene.png").set_duration(audio.duration).set_audio(audio)
    
    # 5. Yüksek Kalite Kayıt
    video.write_videofile("otonom_shorts.mp4", fps=24, bitrate="15M")
    print("İşlem Başarılı! otonom_shorts.mp4 oluşturuldu.")

if __name__ == "__main__":
    asyncio.run(make_pro_cartoon())
