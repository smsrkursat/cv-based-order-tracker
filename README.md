# BGG-but

BGG-but, restoranlarda kamera ile yemek tespiti, masa ve garson yönetimi, sipariş takibi ve raporlama sağlayan bir Flask + MongoDB tabanlı demo projedir.

## Özellikler
- **Canlı Kamera:** Web arayüzünden canlı kamera görüntüsü izleme
- **Yemek Tespiti:** Görüntü işleme ile tabaktaki yemekleri otomatik tespit etme (renk tabanlı demo)
- **Sipariş Yönetimi:** Masalara otomatik sipariş ekleme, toplam tutar ve ödeme/temizleme
- **Görüntü Arşivi:** Tüm tespit edilen yemeklerin ve görüntülerin arşivlenmesi
- **Garson Girişi:** Garson seçimi ve yetkilendirme
- **Çoklu Masa Desteği:** Birden fazla masa için ayrı sipariş ve arşiv takibi
- **Raporlama:** Garson ve ürün bazlı satış raporları (API üzerinden)

## Kurulum
1. **Gereksinimler:**
   - Python 3.8+
   - MongoDB (local veya bulut)
   - pip ile: `pip install flask pymongo opencv-python numpy`

2. **MongoDB'yi başlatın:**
   - Localde: `mongod` komutuyla
   - Veya MongoDB Atlas bağlantı adresinizi `database.py` içinde güncelleyin.

3. **Projeyi başlatın:**
   ```bash
   python app.py
   ```

4. **Web arayüzüne erişin:**
   - Tarayıcıdan: [http://localhost:5000](http://localhost:5000)

## Kullanım
- Garson seçip giriş yapın.
- Masa seçin, kamerayı başlatın ve "Yemekleri Tespit Et" butonuna tıklayın.
- Siparişler otomatik eklenir, toplam tutar ve arşiv güncellenir.
- "Siparişi Temizle/Öde" ile masa sıfırlanır ve sipariş arşive kaydedilir.
- Görüntü arşivinde geçmiş tespitler ve fotoğraflar listelenir.

## Geliştirici Notları
- Yemek tespiti gerçek AI modeliyle kolayca entegre edilebilir (şu an renk tabanlı demo).
- Kod modülerdir: `camera.py`, `food_detector.py`, `database.py`, `utils.py`.
- API endpoint'leriyle (örn. `/get_reports`) raporlar alınabilir.

## Katkı ve Lisans
- Demo ve eğitim amaçlıdır. Katkılarınızı bekleriz!
