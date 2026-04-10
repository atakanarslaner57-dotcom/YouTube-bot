import os
import google.generativeai as genai

def main():
    print("🚀 YouTube Botu Zorunlu Modda Başlatıldı!")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: API Anahtarı bulunamadı!")
        return

    try:
        genai.configure(api_key=api_key)
        
        # 404 hatasını aşmak için model ismini tam teknik adıyla yazıyoruz
        # Bu yöntem v1beta hatasını genellikle baypas eder
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        print("🤖 Yapay zeka içerik üretiyor...")
        
        # İçerik üretme istemi
        response = model.generate_content("YouTube Shorts için ilginç bir bilgi videosu senaryosu yaz.")
        
        if response.text:
            print("\n--- ÜRETİLEN SENARYO ---\n")
            print(response.text)
            print("\n✅ BAŞARILI!")
        else:
            print("⚠️ Cevap boş döndü.")

    except Exception as e:
        print(f"❌ Hata Detayı: {str(e)}")

if __name__ == "__main__":
    main()
