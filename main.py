import os
import google.generativeai as genai

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # Senin anahtarının desteklediği kesin olan model
    model = genai.GenerativeModel('gemini-flash-latest')
    
    # Botun yeni "Görevi" (Prompt)
    istek = (
        "Sen popüler bir çocuk eğitici YouTube kanalı yazarısın. "
        "Okul öncesi çocuklara hitap eden, 50-60 saniyelik, eğlenceli ve öğretici bir Shorts senaryosu yaz. "
        "Konu: Hayvanlar, uzay veya doğa hakkında çok ilginç bir bilgi olsun. "
        "Format şu olsun: \n"
        "1. Merak uyandıran bir Soruyla başla.\n"
        "2. Basit ve neşeli bir dille açıkla.\n"
        "3. Sonunda çocuklara bir soru sor.\n"
        "4. Ekran için görsel betimlemeler ekle (Örn: Ekranda zıplayan bir tavşan belirir)."
    )

    try:
        print("👶 Çocuklar için harika bir video fikri hazırlanıyor...")
        response = model.generate_content(istek)
        
        print("\n" + "="*40)
        print("📺 YOUTUBE SHORTS SENARYOSU")
        print("="*40 + "\n")
        print(response.text)
        print("\n✅ Senaryo Hazır! Şimdi bunu videoya dönüştürebilirsin.")

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    main()
