import os
import google.generativeai as genai

def main():
    print("🚀 YouTube Botu Senin Modellerinle Başlatıldı!")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ HATA: API Anahtarı bulunamadı!")
        return

    try:
        genai.configure(api_key=api_key)
        
        # Senin listende gördüğüm ve çalıştığı kesin olan model ismi:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        print("🤖 Yapay zeka fikir üretiyor...")
        
        response = model.generate_content("YouTube Shorts için 60 saniyelik çok ilginç bir bilgi videosu senaryosu yaz.")
        
        print("\n" + "="*40)
        print("✨ İŞTE SENARYON ✨")
        print("="*40 + "\n")
        print(response.text)
        print("\n" + "="*40)
        print("✅ BAŞARIYLA TAMAMLANDI!")

    except Exception as e:
        print(f"❌ Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
