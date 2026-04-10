import os
import google.generativeai as genai

# 1. Ayarlar ve Bağlantılar
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def video_fikri_uret():
    print("🤖 Yapay zeka video konusu düşünüyor...")
    prompt = "YouTube Shorts için çok ilginç, bilgilendirici ve merak uyandırıcı bir konu ve 60 saniyelik bir senaryo yaz."
    cevap = model.generate_content(prompt)
    return cevap.text

def main():
    print("🚀 YouTube Botu Başlatıldı!")
    
    # Video içeriğini üret
    icerik = video_fikri_uret()
    print("\n--- ÜRETİLEN SENARYO ---\n")
    print(icerik)
    
    print("\n✅ İçerik hazırlandı. Bir sonraki aşama: Video montaj ve yükleme.")

if __name__ == "__main__":
    main()
