# Albion Recruit Bot ⚔️

Albion Online için geliştirilmiş, klan (guild) alımları veya düzenli sohbet (chat) duyuruları yapmak amacıyla kullanılabilecek, kullanıcı dostu arayüze sahip otomatik mesaj gönderme (Auto-Typer) botudur. 

Modern ve karanlık temalı arayüzü sayesinde birden fazla mesajı farklı zaman aralıklarıyla sıraya koyabilir, istediğiniz zaman başlatıp durdurabilirsiniz.

## Özellikler ✨

* **Çoklu Zamanlayıcı (Timer) Desteği:** Birden fazla farklı mesajı, farklı süre (dakika/saniye) aralıklarıyla aynı anda çalıştırabilirsiniz.
* **Modern Arayüz (GUI):** `customtkinter` kullanılarak hazırlanmış şık, karanlık tema tabanlı arayüz.
* **Kısayol Tuşları (Hotkeys):**
  * `F9`: Botu Başlat/Durdur
  * `F10`: Tüm işlemleri acil durdur
* **Otomatik Kayıt:** Eklediğiniz mesajlar ve süreler çıkışta veya manuel olarak `timers.json` dosyasına kaydedilir, bir sonraki açılışta tekrar yüklenir.
* **Bağımsız Kontrol:** Eklediğiniz her mesaj satırını ayrı ayrı açıp kapatabilirsiniz (Toggle).
* **Güvenli Gönderim:** Mesajı yazarken oyundaki chat ekranını açmak için `Enter`'a basar, mesajı insan hızında yazar ve tekrar `Enter`'a basıp gönderir.

## Gereksinimler 🛠️

Projeyi kaynak kodundan çalıştırmak için sisteminizde **Python 3.8+** yüklü olmalıdır. Ayrıca aşağıdaki kütüphanelerin kurulması gerekmektedir:

```bash
pip install customtkinter pyautogui keyboard
```

*(Not: Eğer `requirements.txt` dosyanız varsa `pip install -r requirements.txt` komutuyla da kurulum yapabilirsiniz.)*

## Nasıl Kullanılır? 🚀

1. Botu açın (Kaynaktan `python bot.py` ile veya `.exe` dosyasını çalıştırarak).
2. **"Timer Ekle"** butonuna basarak yeni bir duyuru satırı oluşturun.
3. Gönderilecek mesajı, dakika ve saniye aralıklarını belirleyin.
4. Oyuna (Albion Online) geçin ve oyun penceresinin aktif (odaklanmış) olduğundan emin olun.
5. Bot arayüzünden **"Başlat"** butonuna basın veya klavyenizden **`F9`** tuşuna basın.
6. Bot belirlediğiniz süreler doldukça otomatik olarak chat'e girip mesajı yazacaktır.

## Ekran Görüntüsü 📸
*(Buraya daha sonra projenin bir ekran görüntüsünü ekleyebilirsiniz)*

## Önemli Uyarı ⚠️

* Bot çalışırken mouse ve klavyenize müdahale eder (`pyautogui` ve `keyboard` kütüphaneleri kullanılarak). Bu nedenle bot yazım işlemi gerçekleştirirken klavyeyi veya fareyi kullanmamaya özen gösterin.
* 3. parti yazılımların oyunlarda kullanımı kurallara aykırı olabilir. Ban riski tamamen kullanıcının kendi sorumluluğundadır.

## Geliştirici

Bu proje, açık kaynak olarak paylaşılmıştır. Dilediğiniz gibi geliştirebilir ve kendi ihtiyaçlarınıza göre düzenleyebilirsiniz.
