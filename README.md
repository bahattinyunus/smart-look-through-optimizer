# 🛡️ Akıllı Look-Through Optimizatörü (SLT-X)

> **Yüksek Riskli Sinyal Ortamları İçin Adaptif Elektronik Harp Zamanlama Optimizasyonu.**

![EH Durumu](https://img.shields.io/badge/Durum-Operasyonel-00f2ff?style=for-the-badge&logo=target)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![UI](https://img.shields.io/badge/Aray%C3%BCz-Glassmorphism-purple?style=for-the-badge&logo=css3)

## 🌌 Genel Bakış

**Akıllı Look-Through Optimizatörü (SLT-X)**, modern Elektronik Harp (EH) sistemlerindeki *Look-Through İkilemi*'ni çözmek için tasarlanmış yeni nesil bir araçtır. Karıştırma (jamming) esnasında, sistemin ortamı örnekleyebilmesi ve hedef parametrelerini güncelleyebilmesi için periyodik olarak yayını durdurması (look-through aşaması) gerekir.

SLT-X, **Adaptif Sezgisel Optimizasyon** kullanarak bu pencerelerin genişliğini ve tekrar aralığını dinamik olarak ayarlar. Böylece maksimum durumsal farkındalık sağlanırken, karıştırma etkinliğinden ödün verilmez.

## 🛠️ Mimari

`mermaid
graph TD
    A[Radar Ortamı] -->|Sinyal Yakalama| B(Adaptif Optimizatör)
    B -->|SNR Hesaplama| C{Karar Mekanizması}
    C -->|Yüksek Tehdit| D[Dar LT Penceresi / Yüksek Frekans]
    C -->|Düşük Tehdit| E[Geniş LT Penceresi / Düşük Frekans]
    D --> F[Karıştırıcı Kontrolcü]
    E --> F
    F -->|Optimal Karıştırma| A
`

## 🚀 Temel Özellikler

- **Adaptif LT Ölçeklendirme:** Tehdit hızı ve Sinyal-Gürültü Oranı'na (SNR) göre izleme pencerelerini otomatik ayarlar.
- **Glassmorphic Konsol:** Optimizasyon metriklerinin ve sinyal spektrogramının izlendiği premium gerçek zamanlı web arayüzü.
- **EH Simülatörü:** Algoritmaları sentetik radar profillerine karşı test etmek için entegre simülasyon motoru.
- **Üst Düzey Performans:** Yüksek yoğunluklu sinyal ortamlarında düşük gecikmeli karar verme için optimize edilmiştir.

## 📂 Proje Yapısı

- core/: Python tabanlı mantık ve simülasyon.
  - optimizer.py: SLT-X algoritmasının kalbi.
  - simulator.py: Sentetik EH ortamı başlatıcısı.
- gui/: Premium dashboard dosyaları.
  - index.html: Ana konsol giriş noktası.
  - styles.css: Glassmorphic tasarım sistemi.
  - pp.js: Gerçek zamanlı görselleştirme mantığı.

## 🚦 Hızlı Başlangıç

1. **Simülasyonu Çalıştır:**
   `ash
   python core/simulator.py
   `
2. **Dashboard'u Başlat:**
   gui/index.html dosyasını herhangi bir modern tarayıcıda açın.

---

*Yasal Uyarı: Bu proje, eğitim ve simülasyon amaçlı bir teknik gösterimdir.*
