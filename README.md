# Araç Sınıflandırma ve Plaka Tanıma Sistemi 🚗🔍

## 🛠️ Kullanılan Teknolojiler

- **Python** – YOLO modeli ve OCR işlemleri için  
- **Arduino IDE** – Buzzer ve kapı kontrolü için  
- **VS Code** – Kodlama ve proje yönetimi ortamı  
- **Flask** – Web arayüzü oluşturmak için  
- **OpenCV & EasyOCR** – Görüntü işleme ve plaka tanıma için  
- **Roboflow** – Görüntü verilerini işaretlemek ve model eğitimi için hazır hale getirmek amacıyla kullanıldı


## 🎯 Proje Amacı

Bu projenin temel amacı, bir aracın türünü (araba veya kamyonet) ve plakasını gerçek zamanlı olarak tespit eden bir sistem geliştirmektir.  
Sistem, bir web kamerası aracılığıyla aracı sınıflandırır ve plakasını okur. Aşağıdaki kurallara göre işlem yapar:

- Eğer araç **kamyonet** ve plaka **sisteme kayıtlıysa**, Arduino üzerinden **kapı açılır**.  
- Eğer araç **araba** ise veya plaka **sisteme kayıtlı değilse**, Arduino üzerindeki **buzzer aktif hale gelir ve öter**.

Bu yapı sayesinde araç tipi ve plaka bilgisine göre kontrollü bir geçiş sistemi simüle edilmektedir.

## 🚀 Proje Adımları

### 1️⃣ Veri Toplama ve Etiketleme

Projenin ilk adımı olarak toplamda 2000 adet araç görseli toplandı.  
- İlk 1000 görselde farklı araç türleri ve bu araçlara ait plakalar yer aldı. Bu görseller, **Roboflow** platformu kullanılarak hem araç hem de plaka olacak şekilde nesne tespiti formatında etiketlendi.  
- İkinci 1000 görsel ise **kamyon, tır ve otobüs** gibi büyük araçlardan oluştu. Bu görseller yalnızca “kamyon” sınıfı altında işaretlendi ve plakaları da yine Roboflow üzerinden etiketlendi.  

Etiketleme işlemi tamamlandıktan sonra veri seti, eğitim (%70), doğrulama (%15) ve test (%15) olarak ayrıldı.  
Son olarak bu veriler **YOLO formatında** dışa aktarılıp, **YOLOv8** model eğitimi için hazırlandı.


### 2️⃣ YOLOv8 Model Eğitimi

Etiketlenmiş veri seti, YOLOv8 algoritması kullanılarak eğitilmiştir. Eğitim işlemi `train_model.py` dosyası üzerinden, **Visual Studio Code** ortamında gerçekleştirilmiştir.  
Model eğitimi sırasında kullanılan veriler ve eğitim sonucu oluşan `best.pt` ağırlık dosyası GitHub'a yüklenememiştir. Bu dosyaların boyutu büyük olduğundan, **Google Drive bağlantısı** aracılığıyla paylaşılmıştır.


### 3️⃣ Arduino Entegrasyonu

Arduino, sistemde fiziksel kontrol birimi olarak görev yapmaktadır. Kapı açma ve buzzer çalıştırma işlemleri Arduino üzerinden gerçekleştirilmiştir.  
İlk olarak `arduino_listener2.py` dosyası kullanılarak Arduino'nun bilgisayara bağlı olup olmadığı test edilmiştir. Bu dosya, temel bağlantı kontrolü sağlamak için kullanılmıştır.

Asıl kontrol mekanizması ise `app2.py` ve `app3.py` dosyaları aracılığıyla yürütülmektedir. Bu dosyalar, tespit edilen araç türüne ve plaka bilgisine göre Arduino'ya uygun komutu gönderir:

- Eğer araç **kamyonet** ve plaka **kayıtlıysa** → Arduino'ya **kapı aç** komutu gider.  
- Eğer araç **araba** ya da plaka **kayıtlı değilse** → Arduino'ya **buzzer çal** komutu gider.



### 4️⃣ Uygulama Akışı ve Gerçek Zamanlı İşlem

Projenin ana uygulama akışı `app2.py` ve `app3.py` dosyalarında gerçekleştirilmektedir.  
Bu dosyalar sayesinde aşağıdaki adımlar tamamlanır:

1. **Webcam üzerinden anlık görüntü alınır**  
2. **YOLOv8 modeli ile araç tespiti yapılır**  
3. **EasyOCR ile plakalar okunur**  
4. Araç tipi ve plaka bilgisi analiz edilir  
5. Duruma göre Arduino'ya **kapı açma** veya **buzzer çalma** komutu gönderilir

📸 Kamera kullanımı için telefon **IP kamera** olarak konumlandırılmıştır. Bu işlem `web.py` dosyasıyla test edilmiştir.  
Görüntü aktarımı için hem bilgisayarın hem de telefonun **aynı Wi-Fi ağına bağlı olması** gerekmektedir. `web.py` dosyası bu amaçla geliştirilmiş bir test betiğidir.

### 🧠 Ana Uygulama Dosyası: `app2.py`

Bu dosya, projenin tüm temel işlevlerini bir araya getiren ana uygulama dosyasıdır. İşlevleri şu şekilde özetlenebilir:

- 📷 **Webcam bağlantısı**: IP üzerinden çalışan telefon kamerasından anlık görüntü alınır.
- 🔍 **Araç ve plaka tespiti**: YOLOv8 modeli ile araç türü (araba/kamyonet) ve plaka konumu tespit edilir.
- 🧠 **OCR (plaka okuma)**: EasyOCR kullanılarak tespit edilen plaka bölgesinden metin okunur.
- 🧾 **Plaka kaydı**: Okunan plakalar tarih/saat bilgisiyle birlikte `.txt` dosyasına ve `.jpg` görsel olarak kaydedilir.
- 🧭 **Karar mekanizması**:
  - Eğer araç **kamyonet** ve plaka **sistemde kayıtlı** ise: Arduino'ya `"KAPI"` komutu gönderilir.
  - Eğer araç **araba** ya da plaka **kayıtlı değilse**: Arduino'ya `"BUZZER"` komutu gönderilir.
- 🌐 **Web arayüzü (Flask)**: `index.html` üzerinden canlı kamera görüntüsü ve tespit bilgileri kullanıcıya sunulur.

📍 Not: Kamera bağlantısının çalışabilmesi için bilgisayar ve IP kamera olarak kullanılan telefonun aynı Wi-Fi ağına bağlı olması gerekmektedir.


### 🧪 Gerçek Test Senaryosu: `app3.py`

`app3.py` dosyası, sistemin gerçek araçla test edilebilmesi için hazırlanmıştır.  
Ancak test sırasında kamyonet bulunamadığı için, sistemin doğru çalıştığını göstermek amacıyla **kayıtlı bir araba ve plakası (34 NDH 928)** manuel olarak eklenmiştir.

Bu dosya üzerinden yapılan testlerde:

- Gerçek zamanlı olarak IP kamera bağlantısı kurulur  
- Araç ve plaka tespiti yapılır  
- Plaka `KAYITLI_PLAKALAR` listesinde varsa ve araç tipi uygunsa Arduino’ya doğru komut gönderilir:
  - 🚗 Kayıtlı araba → `"KAPI"` komutu gönderilir
  - 🚗 Kayıtsız araba → `"BUZZER"` komutu gönderilir

Ayrıca plaka karşılaştırması, harf büyük/küçüklüğü ve boşluklardan etkilenmeyecek şekilde normalize edilerek yapılmıştır.  
Bu sayede sistemin çalışma mantığı, gerçek ortamda başarıyla test edilmiştir.


## 🎥 Proje Tanıtım Videoları

Aşağıdaki videolarda sistemin gerçek araçlarla yapılan testlerini izleyebilirsiniz:

- 🚗 **Araba ile Gerçek Zamanlı Test:**  
  [https://www.youtube.com/watch?v=7t-cNMLsBSo](https://www.youtube.com/watch?v=7t-cNMLsBSo)

- 🚚 **Kamyonet ile Gerçek Zamanlı Test:**  
  [https://www.youtube.com/watch?v=HUh6iXOQYls&t=4s](https://www.youtube.com/watch?v=HUh6iXOQYls&t=4s)


  ## 📁 Dosyalara Erişim (Google Drive)

Boyut kısıtlamalarından dolayı aşağıdaki dosyalar GitHub deposuna yüklenememiştir.  
Bu dosyalara aşağıdaki Google Drive bağlantısı üzerinden erişebilirsiniz:

🔗 [Google Drive – Eğitim Verileri & Model Ağırlıkları](https://drive.google.com/drive/u/0/folders/151BHTIxvO2pjaCyDjF8uPTAG85C1D4DM)

İçerik:
- `best.pt`: Eğitilmiş YOLOv8 model ağırlığı  
- `runs/`: Eğitim çıktı klasörü  
- `dataset/`: Etiketlenmiş veri seti  
- Diğer büyük boyutlu medya ve proje dosyaları




