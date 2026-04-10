import os
import google.generativeai as genai

def main():
    print("🚀 YouTube Botu Yeni Nesil Bağlantı İle Başlatıldı!")
    
    # API Anahtarını Ayarla
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: API Anahtarı bulunamadı!")
        return

    try:
        genai.configure(api_key=api_key)
        
        # Model ismini en basit ve garanti haliyle yazıyoruz
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("🤖 Yapay zeka içerik üretiyor...")
        prompt = "YouTube Shorts için 60 saniyelik, çok ilgi çekici bir bilgi videosu senaryosu yaz."
        
        # İçerik Üretme (En güncel komutla)
        response = model.generate_content(prompt)
        
        print("\n--- ÜRETİLEN SENARYO ---\n")
        print(response.text)
        print("\n✅ İşlem başarıyla tamamlandı!")

    except Exception as e:
        print(f"❌ Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
