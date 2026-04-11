import os
import requests
import asyncio
from moviepy.editor import ImageClip, AudioFileClip
import edge_tts

# --- AYARLAR ---
HF_TOKEN = "BURAYA_HF_TOKENINI_YAZ" # Kendi anahtarını tırnak içine yapıştır
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

def get_vivid_scene(prompt, output_file):
    """Hugging Face üzerinden 4K 3D sahne indirir."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        return True
    else:
        print(f"Hugging Face Hatası: {response.status_code}")
        return False

async def start_engine():
    # 1. Sahne Tasarımı (Senin istediğin 3D karakterler)
    #
    prompt = (
        "3D render, Pixar style, high quality animation, underwater kingdom. "
        "A cute purple octopus with big eyes, a turquoise sea turtle with shell patterns, "
        "and a bright orange 3D fish. Cinematic lighting, bubbles, 4K, vertical 9:16."
    )
    
    print("Yapay zeka sahneyi hayal ediyor...")
    if get_vivid_scene(prompt, "temp_scene.jpg"):
        # 2. Seslendirme
        text = "Tori, Papi, Fini! İşte hayal ettiğimiz o muhteşem 4K dünyası!"
        await edge_tts.Communicate(text, "tr-TR-AhmetNeural").save("temp_voice.mp3")
        
        # 3. Video Montaj
        audio = AudioFileClip("temp_voice.mp3")
        video = ImageClip("temp_scene.jpg").set_duration(audio.duration).set_audio(audio)
        
        # 4. Kayıt (İsim hatası olmaması için)
        video.write_videofile("otonom_shorts.mp4", fps=24, bitrate="15M")
        print("İşlem Başarılı!")
    else:
        print("Görsel oluşturulamadığı için video iptal edildi.")

if __name__ == "__main__":
    asyncio.run(start_engine())
