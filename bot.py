import requests
from bs4 import BeautifulSoup
import time

# Yerel Flask sunucumuzun adresi
sunucu_url = "http://127.0.0.1:5000"

def ilan_gonder(baslik, fiyat, link):
    try:
        veri = {"title": baslik, "price": fiyat, "url": link}
        response = requests.post(f"{sunucu_url}/api/alarm-ekle", json=veri)
        if response.status_code == 200:
            print("[BİLDİRİM] İlan sisteme başarıyla aktarıldı!")
    except Exception as e:
        print(f"[HATA] İlan gönderilemedi: {e}")

def alarmlari_getir():
    try:
        response = requests.get(f"{sunucu_url}/api/alarmlar")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"[HATA] Alarmlar çekilemedi: {e}")
    return []

def ilan_taramasi_baslat():
    print("Alarm Sepeti Botu aktif alarmları kontrol ediyor...")
    alarmlar = alarmlari_getir()
    
    if not alarmlar:
        print("Aktif alarm bulunamadı, bekleniyor...")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9",
        "Referer": "https://www.sahibinden.com/"
    }

    for alarm in alarmlar:
        kelime = alarm.get("kelime", "arac")
        print(f"[{kelime}] için Sahibinden taranıyor...")
        
        url = f"https://www.sahibinden.com/kelime-ile-arama?query={kelime.replace(' ', '+')}"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                ilanlar = soup.find_all('tr', class_='searchResultsItem')
                
                if ilanlar:
                    for ilan in ilanlar[:3]:
                        baslik = ilan.find('a', class_='classifiedTitle').text.strip()
                        fiyat = ilan.find('td', class_='searchResultsPriceValue').text.strip()
                        link = "https://www.sahibinden.com" + ilan.find('a', class_='classifiedTitle')['href']
                        
                        print(f"[İLAN BULUNDU] {baslik} - Fiyat: {fiyat}")
                        ilan_gonder(baslik, fiyat, link)
                else:
                    print("Bu arama için ilan listesi seçilemedi (Bot koruması aktif olabilir).")
            else:
                print(f"[HATA] Sahibinden erişim kodu: {response.status_code}")
        except Exception as e:
            print(f"[HATA] Tarama hatası: {e}")

if __name__ == "__main__":
    while True:
        ilan_taramasi_baslat()
        print("Yeni tarama döngüsü için 30 saniye bekleniyor...\n")
        time.sleep(30)