# AdminForge

AdminForge, **Python** ve **PySide6** kullanılarak geliştirilmiş açık kaynaklı bir **Windows IT yönetim aracıdır**.

Amaç, sistem yöneticilerinin ve IT destek ekiplerinin günlük kullandığı Windows araçlarını tek bir masaüstü uygulamasında bir araya getirmektir.

AdminForge sayesinde birçok sistem işlemi GUI üzerinden hızlı ve pratik şekilde yapılabilir.

---

# Özellikler

AdminForge şu anda aşağıdaki modülleri içermektedir:

## Dashboard

Sistem hakkında temel bilgileri görüntüler:

- Bilgisayar adı
- Kullanıcı adı
- İşletim sistemi
- IP adresi
- CPU bilgisi
- RAM bilgisi
- Windows lisans durumu

---

## Komut Merkezi

Grafik arayüz üzerinden komut çalıştırmayı sağlar.

Desteklenen kabuklar:

- CMD
- PowerShell

Özellikler:

- hızlı komut butonları
- komut çıktısı görüntüleme
- komut logları

---

## Ağ Araçları

Yaygın kullanılan ağ teşhis araçları:

- Ping
- NSLookup
- Traceroute
- IP yapılandırması
- Netstat
- DNS önbelleği temizleme

---

## Disk ve Depolama

Disk yönetimi ve depolama bilgileri:

- mantıksal disk bilgileri
- disk kullanım bilgileri
- DiskPart komutları
- CHKDSK işlemleri

---

## Sistem Onarım

Windows onarım araçları:

- SFC /SCANNOW
- DISM ScanHealth
- DISM RestoreHealth
- GPUpdate
- System Information
- Event Viewer
- Task Manager

---

## Servis Yönetimi

Windows servislerini GUI üzerinden yönetme:

- çalışan servisleri görüntüleme
- duran servisleri görüntüleme
- servis başlatma
- servis durdurma
- servis durumunu kontrol etme

---

## Raporlama

Sistem raporları oluşturulabilir:

- sistem snapshot
- donanım bilgileri
- lisans bilgileri
- log önizleme

Bu raporlar troubleshooting ve dokümantasyon için kullanılabilir.

---

## Ayarlar

Uygulama hakkında temel bilgiler içerir:

- uygulama sürümü
- geliştirici bilgisi
- uygulama imzası

---

# Kullanılan Teknolojiler

AdminForge aşağıdaki teknolojiler ile geliştirilmiştir:

- Python
- PySide6 (Qt for Python)
- psutil
- PyInstaller

---

# Proje Yapısı

