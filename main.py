import os
import asyncio
import requests
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
import edge_tts

# Karakterlerin doğrudan linkleri (GitHub'da silmiş olsan da buradan çekilecek)
#
CHARACTERS = {
    "Papi": "https://images.pngtree.com/png-clipart/20230913/original/pngtree-3d-orange-fish-png-image_20930822.jpg",
    "Tori": "https://png.pngtree.com/png-clipart/20230531/original/pngtree-3d-turtle-turtle-gradient-texture-ui-design-ux-material-png-image_14115622.jpg",
    "Fini": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzY7B9Y6p7lH9-Pz9j8_Z6J8-R8E5t1-Pz9Q&s" # Octopus
}

def download_and_process_assets():
    """Görselleri indirir ve arka planlarını şeffafmış gibi işler."""
    processed_clips = []
    for name, url in CHARACTERS.items():
        resp = requests.get(url)
        with open(f"{name}.jpg", "wb") as f:
            f.write(resp.content)
        
        # Karakteri ekrana yerleştir (Boyutlandırma ve Pozisyon)
        clip = ImageClip(f"{name}.jpg").set_duration(5).resize(width=400)
        processed_clips.append(clip)
    return processed_clips

async def generate_video():
    print("Otonom render motoru başlatıldı...")
    
    # 1. Karakterleri Hazırla
    clips = download_and_process_assets()
    
    # 2. Seslendirme
    text = "Selam Papi, Tori ve Fini! İşte gerçek 3D dünyamız hazır!"
    await edge_tts.Communicate(text, "tr-TR-AhmetNeural").save("voice.mp3")
    audio = AudioFileClip("voice.mp3")
    
    # 3. Sahne Dizilimi (Yan yana koyalım)
    clips[0] = clips[0].set_position(("center", 400))  # Papi
    clips[1] = clips[1].set_position(("left", 1000))  # Tori
    clips[2] = clips[2].set_position(("right", 1000)) # Fini
    
    # Arka plan rengini belirle
    from moviepy.editor import ColorClip
    bg = ColorClip(size=(1080, 1920), color=(0, 50, 100)).set_duration(audio.duration)
    
    # 4. Final Birleştirme
    final_video = CompositeVideoClip([bg] + [c.set_duration(audio.duration) for c in clips])
    final_video.set_audio(audio).write_videofile("otonom_shorts.mp4", fps=24, codec="libx264")
    print("İşlem Tamam: otonom_shorts.mp4 oluşturuldu!")

if __name__ == "__main__":
    asyncio.run(generate_video())
