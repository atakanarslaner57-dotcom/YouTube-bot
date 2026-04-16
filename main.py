# Stable Diffusion Forge / Automatic1111 Arayüzünü Başlatma Kodu
!pip install -q torch torchvision torchaudio
!git clone https://github.com/lllyasviel/stable-diffusion-webui-forge # Forge reposunu çeker
%cd stable-diffusion-webui-forge

# Gerekli model ve upscaler'ları indirmek için (Opsiyonel ama önerilir)
!wget -O models/Stable-diffusion/model.safetensors https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors

# Arayüzü dış dünyaya açan komut
!python launch.py --share --xformers --enable-insecure-extension-access
