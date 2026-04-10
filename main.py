import os
import google.generativeai as genai

def main():
    print("🚀 Bot Başlatıldı...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: API Anahtarı bulunamadı!")
        return

    try:
        genai.configure(api_key=api_key)
        
        # En güncel model ismini en yalın haliyle kullanıyoruz
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("🤖 Yapay zeka içeriği oluşturuyor...")
        
        # Basit bir deneme isteği
        response = model.generate_content("YouTube Shorts için ilginç bir bilgi yaz.")
        
        print("\n✨ ÜRETİLEN İÇERİK:")
        print(response.text)
        print("\n✅ BAŞARILI!")

    except Exception as e:
        print(f"❌ Kritik Hata: {str(e)}")
        print("\n💡 İPUCU: Eğer hala 404 alıyorsan, Google AI Studio'dan yeni bir API KEY almayı dene.")

if __name__ == "__main__":
    main()
