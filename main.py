import os

def kontrol():
    print("--- OTOMASYON SİSTEMİ BAŞLATILIYOR ---")
    anahtarlar = {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "YOUTUBE_CLIENT_ID": os.getenv("YOUTUBE_CLIENT_ID"),
        "YOUTUBE_CLIENT_SECRET": os.getenv("YOUTUBE_CLIENT_SECRET")
    }
    
    for isim, deger in anahtarlar.items():
        if deger:
            print(f"✅ {isim}: Bağlantı Başarılı!")
        else:
            print(f"❌ {isim}: EKSİK! Lütfen Settings > Secrets kısmını kontrol et.")

if __name__ == "__main__":
    kontrol()
