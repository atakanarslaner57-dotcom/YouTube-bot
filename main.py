import os
import google.generativeai as genai

# Yapay Zeka Ayarları
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # En güncel ve hızlı model olan 1.5-flash kullanıyoruz
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    def video_fikri_uret():
        print("🤖 Yapay zeka video konusu düşünüyor...")
        prompt = "YouTube Shorts için çok ilginç, bilgilendirici ve 60 saniyelik bir senaryo yaz. Başlık ve sahneler net olsun."
        cevap = model.generate_content(prompt)
        return cevap.text

    def main():
        print("🚀 YouTube Botu Başlatıldı!")
        
        # Anahtar kontrolü
        if not os.getenv("GEMINI_API_KEY"):
            print("❌ HATA: API Anahtarı bulunamadı!")
            return

        # İçerik üretme
        icerik = video_fikri_uret()
        print("\n--- ÜRETİLEN SENARYO ---\n")
        print(icerik)
        print("\n✅ İçerik başarıyla hazırlandı!")

    if __name__ == "__main__":
        main()

except Exception as e:
    print(f"❌ Bir hata oluştu: {e}")
