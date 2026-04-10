import os
import google.generativeai as genai

def main():
    print("🚀 YouTube Botu Kesin Çözüm Modunda Başlatıldı!")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: API Anahtarı bulunamadı!")
        return

    try:
        genai.configure(api_key=api_key)
        
        # 404 hatasını çözmek için 'models/' ekini kaldırıp en saf ismi deniyoruz
        # Bazı kütüphane versiyonları sadece bunu kabul eder
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("🤖 Yapay zeka içerik üretiyor...")
        
        # En basit içerik üretme komutu
        response = model.generate_content("YouTube Shorts için 1 dakikalık ilginç bir bilgi senaryosu yaz.")
        
        print("\n--- ÜRETİLEN SENARYO ---\n")
        print(response.text)
        print("\n✅ BAŞARILI! Senaryo yukarıdadır.")

    except Exception as e:
        # Eğer yine hata verirse, model ismini 'gemini-pro' olarak deneyelim (Alternatif)
        print(f"⚠️ Bir sorun çıktı, yedek model deneniyor...")
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("YouTube Shorts senaryosu yaz.")
            print(response.text)
            print("\n✅ Yedek model ile başarıldı!")
        except Exception as e2:
            print(f"❌ Kritik Hata: {str(e2)}")

if __name__ == "__main__":
    main()
