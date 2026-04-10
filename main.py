import os
import subprocess
import sys

# --- GARANTİLİ KÜTÜPHANE YÜKLEME (En üstte kalmalı) ---
def install_dependencies():
    try:
        import edge_tts
        import moviepy
    except ImportError:
        print("🛠️ Eksik kütüphaneler yükleniyor, lütfen bekleyin...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3", "edge-tts", "requests"])
        print("✅ Yükleme tamamlandı!")

install_dependencies()
# -----------------------------------------------------

import asyncio
import edge_tts
import math
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, vfx
# ... (Kodun geri kalanı aynı kalabilir)
