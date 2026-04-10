import os
import google.generativeai as genai

def main():
    # API anahtarını GitHub'dan çek
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    print("🚀 Sistem test ediliyor...")
    
    try:
        # Mevcut modelleri listele (Hatanın nedenini burada göreceğiz)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Kullanabildiğin model: {m.name}")
        
        # En garanti model ile deneme yap
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Merhaba, çalışıyor musun?")
        print("\n🤖 Bot Cevabı:", response.text)
        
    except Exception as e:
        print(f"❌ Hata hala devam ediyor: {e}")

if __name__ == "__main__":
    main()
