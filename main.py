import os
from google import genai

def main():
    print("🚀 YouTube Botu En Yeni SDK ile Başlatıldı!")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: API Anahtarı eksik!")
        return

    try:
        # En yeni bağlantı yöntemi
        client = genai.Client(api_key=api_key)
        
        print("🤖 Yapay zeka içerik üretiyor...")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="YouTube Shorts için 60 saniyelik harika bir bilgi videosu senaryosu yaz."
        )
        
        print("\n--- ÜRETİLEN SENARYO ---\n")
        print(response.text)
        print("\n✅ Başarıyla tamamlandı!")

    except Exception as e:
        print(f"❌ Hata: {str(e)}")

if __name__ == "__main__":
    main()
