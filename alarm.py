import time
import threading
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Bulunan ilanları tutacağımız liste
bulunan_ilanlar = []

# --- 30 SANİYEDE BİR ÇALIŞAN ARKA PLAN BOTU ---
def sahibinden_bot_dongusu():
    print("🤖 Sahibinden tarama botu arka planda başlatıldı (30 saniyede bir tarıyor)...")
    while True:
        try:
            # BURAYA KENDİ BOT KODLARINI (istek atma, ilan bulma mantığını) EKLEYEBİLİRSİN
            # Örnek test ilanı ekleyelim ki arayüzde görebilelim:
            ornek_ilan = {
                "baslik": f"Örnek İlan - {int(time.time())}",
                "fiyat": "1.500.000 TL",
                "link": "https://www.sahibinden.com"
            }
            
            # Eğer ilan daha önce eklenmediyse listeye en başa ekle
            if not any(i['baslik'] == ornek_ilan['baslik'] for i in bulunan_ilanlar):
                bulunan_ilanlar.insert(0, ornek_ilan)
                print(f"✨ Yeni ilan yakalandı: {ornek_ilan['baslik']}")
                
        except Exception as e:
            print(f"Tarama sırasında hata oluştu: {e}")
            
        # 30 saniye bekleme döngüsü
        time.sleep(30)

# --- WEB ARAYÜZÜ ROUTE'LARI ---
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Alarm Sepeti - Canlı Takip</title>
        <style>
            body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }
            h1 { color: #38bdf8; }
            .ilan-kart { background: #1e293b; padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 4px solid #38bdf8; }
            a { color: #38bdf8; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>🛒 Alarm Sepeti - Sahibinden Canlı Takip</h1>
        <p>Bot her 30 saniyede bir arka planda tarama yapıyor...</p>
        <div id="ilan-listesi">Yükleniyor...</div>

        <script>
            async function ilanlariCek() {
                try {
                    let response = await fetch('/api/ilanlar');
                    let ilanlar = await response.json();
                    let listeDiv = document.getElementById('ilan-listesi');
                    
                    if (ilanlar.length === 0) {
                        listeDiv.innerHTML = '<p>Henüz ilan bulunamadı, taranıyor...</p>';
                        return;
                    }

                    let html = '';
                    ilanlar.forEach(ilan => {
                        html += `<div class="ilan-kart">
                            <h3>${ilan.baslik}</h3>
                            <p><b>Fiyat:</b> ${ilan.fiyat}</p>
                            <a href="${ilan.link}" target="_blank">İlanı Sahibinden'de Aç ➔</a>
                        </div>`;
                    });
                    listeDiv.innerHTML = html;
                } catch (err) {
                    console.error('İlanlar alınamadı:', err);
                }
            }

            // Sayfa açıldığında ve her 5 saniyede bir arayüzü güncelle
            ilanlariCek();
            setInterval(ilanlariCek, 5000);
        </script>
    </body>
    </html>
    """

@app.route('/api/ilanlar', methods=['GET'])
def ilanlari_getir():
    return jsonify(bulunan_ilanlar)

if __name__ == '__main__':
    # Arka planda botu çalıştıracak thread'i başlatıyoruz
    bot_thread = threading.Thread(target=sahibinden_bot_dongusu, daemon=True)
    bot_thread.start()

    print("🚀 Web sunucusu http://127.0.0.1:5000 adresinde başlatılıyor...")
    app.run(port=5000, debug=False)