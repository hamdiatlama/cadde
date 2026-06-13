-- ============================================================
-- 🏥 Sağlık ve Tıp - Meslek Veritabanı
-- ============================================================

-- Veritabanı oluşturma
CREATE DATABASE IF NOT EXISTS SaglikVeTip_Meslekleri;
USE SaglikVeTip_Meslekleri;

-- ============================================================
-- 1. ANA DALLAR TABLOSU
-- ============================================================
CREATE TABLE ana_dallar (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ad VARCHAR(100) NOT NULL,
    aciklama TEXT,
    sira INT NOT NULL
);

-- ============================================================
-- 2. ALT DALLAR TABLOSU
-- ============================================================
CREATE TABLE alt_dallar (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ana_dal_id INT NOT NULL,
    ad VARCHAR(100) NOT NULL,
    aciklama TEXT,
    FOREIGN KEY (ana_dal_id) REFERENCES ana_dallar(id) ON DELETE CASCADE
);

-- ============================================================
-- 3. MESLEKLER TABLOSU (Ana tablo)
-- ============================================================
CREATE TABLE meslekler (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ad VARCHAR(100) NOT NULL,
    alt_dal_id INT NOT NULL,
    tanim TEXT,
    egitim_seviyesi VARCHAR(50),
    calisma_alani TEXT,
    FOREIGN KEY (alt_dal_id) REFERENCES alt_dallar(id) ON DELETE CASCADE
);

-- ============================================================
-- 4. MESLEK UZMANLIK ALANLARI TABLOSU (isteğe bağlı detay)
-- ============================================================
CREATE TABLE uzmanlik_alanlari (
    id INT PRIMARY KEY AUTO_INCREMENT,
    meslek_id INT NOT NULL,
    alan_adi VARCHAR(100) NOT NULL,
    FOREIGN KEY (meslek_id) REFERENCES meslekler(id) ON DELETE CASCADE
);

-- ============================================================
-- ANA DALLAR VERİ GİRİŞİ
-- ============================================================
INSERT INTO ana_dallar (id, ad, aciklama, sira) VALUES
(1, 'Tıp Doktorları (Uzmanlık Dalları)', 'Tıp fakültesi mezunu, belirli bir alanda uzmanlaşmış hekimler', 1),
(2, 'Cerrahi Tıp', 'Cerrahi müdahale gerektiren hastalıklarla ilgilenen tıp dalları', 2),
(3, 'Diş Hekimliği', 'Ağız, diş ve çene sağlığı ile ilgilenen sağlık dalı', 3),
(4, 'Veterinerlik', 'Hayvan sağlığı ve hastalıkları ile ilgilenen sağlık dalı', 4),
(5, 'Hemşirelik ve Ebelik', 'Hasta bakımı ve doğum süreci ile ilgilenen sağlık profesyonelleri', 5),
(6, 'Acil Sağlık Hizmetleri', 'Acil durumlarda hastane öncesi ve acil müdahale hizmetleri', 6),
(7, 'Tanı ve Tedavi Destek', 'Teşhis ve tedaviye yardımcı teknik sağlık hizmetleri', 7),
(8, 'Rehabilitasyon ve Terapi', 'Fiziksel, dil, işitme ve fonksiyonel rehabilitasyon hizmetleri', 8),
(9, 'Beslenme ve Diyetetik', 'Beslenme bilimi ve diyet tedavisi hizmetleri', 9),
(10, 'Görme Sağlığı', 'Görme kusurlarının değerlendirilmesi ve düzeltilmesi hizmetleri', 10),
(11, 'Ruh Sağlığı', 'Psikolojik ve ruhsal sağlık hizmetleri', 11),
(12, 'Eczacılık', 'İlaç hazırlama, danışmanlık ve takip hizmetleri', 12),
(13, 'Mühendislik ve Teknik Destek', 'Tıbbi cihaz ve sistem mühendisliği hizmetleri', 13),
(14, 'Sağlık Yönetimi', 'Sağlık kurumlarının idari ve operasyonel yönetim hizmetleri', 14);

-- ============================================================
-- ALT DALLAR VERİ GİRİŞİ
-- ============================================================
INSERT INTO alt_dallar (id, ana_dal_id, ad, aciklama) VALUES
-- Tıp Doktorları (ana_dal_id: 1)
(1, 1, 'Dahili Tıp', 'İç hastalıklar ve organ sistemleri ile ilgilenen uzmanlık dalları'),
(2, 1, 'Tanısal Tıp', 'Hastalıkların teşhisine yönelik laboratuvar ve görüntüleme dalları'),
(3, 1, 'Cerrahi Olmayan Klinik Dallar', 'Cerrahi müdahale gerektirmeyen klinik uzmanlık dalları'),

-- Cerrahi Tıp (ana_dal_id: 2)
(4, 2, 'Genel Cerrahi', 'Cerrahi operasyonları gerçekleştiren uzmanlık dalı'),
(5, 2, 'Anesteziyoloji', 'Ameliyat sırasında anestezi ve yaşamsal fonksiyon takibi'),

-- Diş Hekimliği (ana_dal_id: 3)
(6, 3, 'Klinik Diş Hekimliği', 'Ağız ve diş sağlığı teşhis ve tedavi hizmetleri'),
(7, 3, 'Diş Protez ve Teknik', 'Diş protez ve aparey üretim hizmetleri'),

-- Veterinerlik (ana_dal_id: 4)
(8, 4, 'Veteriner Hekimlik', 'Hayvan hastalıkları teşhis ve tedavi hizmetleri'),
(9, 4, 'Veteriner Sağlık', 'Veteriner hekime yardımcı teknik hizmetler'),

-- Hemşirelik ve Ebelik (ana_dal_id: 5)
(10, 5, 'Hemşirelik', 'Hasta bakım ve tedavi uygulama hizmetleri'),
(11, 5, 'Ebelik', 'Gebelik, doğum ve lohusalık bakım hizmetleri'),

-- Acil Sağlık (ana_dal_id: 6)
(12, 6, 'Acil Tıp Hizmetleri', 'Hastane öncesi ve acil durum müdahale hizmetleri'),

-- Tanı ve Tedavi Destek (ana_dal_id: 7)
(13, 7, 'Anestezi Teknikerliği', 'Anestezi cihaz ve ekipman hazırlık hizmetleri'),
(14, 7, 'Radyoloji', 'Tıbbi görüntüleme cihaz kullanım hizmetleri'),
(15, 7, 'Laboratuvar', 'Tıbbi laboratuvar test ve analiz hizmetleri'),

-- Rehabilitasyon ve Terapi (ana_dal_id: 8)
(16, 8, 'Dil ve Konuşma Terapisi', 'Konuşma, dil, ses ve yutma bozuklukları tedavisi'),
(17, 8, 'Fizik Tedavi', 'Hareket ve fonksiyon bozuklukları rehabilitasyonu'),
(18, 8, 'Ergoterapi', 'Günlük yaşam aktivitelerinde bağımsızlık terapisi'),
(19, 8, 'Odyoloji', 'İşitme ve denge bozuklukları rehabilitasyonu'),

-- Beslenme (ana_dal_id: 9)
(20, 9, 'Beslenme ve Diyet', 'Beslenme programı ve diyet tedavisi hizmetleri'),

-- Görme Sağlığı (ana_dal_id: 10)
(21, 10, 'Optometri', 'Görme kusuru değerlendirme ve düzeltme hizmetleri'),

-- Ruh Sağlığı (ana_dal_id: 11)
(22, 11, 'Psikoloji ve Danışmanlık', 'Psikolojik test, terapi ve danışmanlık hizmetleri'),

-- Tıp Doktorları - yeni alt dallar (ana_dal_id: 1)
(23, 1, 'Halk Sağlığı', 'Toplum sağlığını koruma ve geliştirme çalışmaları'),
(24, 1, 'Acil Tıp', 'Acil durumlarda kritik hasta müdahalesi'),

-- Cerrahi Tıp - yeni alt dallar (ana_dal_id: 2)
(25, 2, 'Beyin ve Sinir Cerrahisi', 'Beyin, omurilik ve sinir sistemi cerrahisi'),
(26, 2, 'Kalp ve Damar Cerrahisi', 'Kalp, damar ve göğüs cerrahisi'),
(27, 2, 'Plastik Cerrahi', 'Estetik ve rekonstrüktif cerrahi'),
(28, 2, 'Çocuk Cerrahisi', 'Çocuk hastalıkları cerrahisi'),
(29, 2, 'Perfüzyon', 'Kalp-akciğer makinesi kullanımı ve açık kalp ameliyatı desteği'),

-- Eczacılık (ana_dal_id: 12)
(30, 12, 'Eczacılık Hizmetleri', 'İlaç hazırlama ve danışmanlık hizmetleri'),

-- Mühendislik (ana_dal_id: 13)
(31, 13, 'Biyomedikal Mühendislik', 'Tıbbi cihaz tasarım, bakım ve onarım hizmetleri'),

-- Tanı ve Tedavi Destek - yeni alt dal (ana_dal_id: 7)
(32, 7, 'Ameliyathane Teknikerliği', 'Ameliyathane hazırlık ve sterilizasyon hizmetleri'),

-- Rehabilitasyon - yeni alt dal (ana_dal_id: 8)
(33, 8, 'Podoloji', 'Ayak sağlığı ve bakım hizmetleri'),

-- Sağlık Yönetimi (ana_dal_id: 14)
(34, 14, 'Sağlık Yönetimi ve Sekreterlik', 'Sağlık kurumu idari ve dokümantasyon hizmetleri');

-- ============================================================
-- MESLEKLER VERİ GİRİŞİ
-- ============================================================
INSERT INTO meslekler (id, ad, alt_dal_id, tanim, egitim_seviyesi, calisma_alani) VALUES
-- Dahili Tıp
(1, 'Aile hekimi', 1, 'Birinci basamak sağlık hizmeti sunan, koruyucu hekimlik yapan doktor', 'Tıp Fakültesi + Uzmanlık', 'Aile Sağlığı Merkezi, Hastane'),
(2, 'Çocuk doktoru', 1, 'Bebek, çocuk ve ergenlerin sağlık sorunlarıyla ilgilenen uzman hekim', 'Tıp Fakültesi + Pediatri Uzmanlığı', 'Hastane, Poliklinik'),
(3, 'Göz doktoru', 1, 'Göz ve görme sistemi hastalıklarının teşhis ve tedavisini yapan uzman hekim', 'Tıp Fakültesi + Göz Hastalıkları Uzmanlığı', 'Hastane, Göz Merkezi'),
(4, 'Ürolog', 1, 'İdrar yolları ve erkek üreme sistemi hastalıklarıyla ilgilenen cerrahi uzman', 'Tıp Fakültesi + Üroloji Uzmanlığı', 'Hastane, Poliklinik'),
(5, 'Kardiyolog', 1, 'Kalp ve damar sistemi hastalıklarının teşhis ve tedavisini yapan uzman hekim', 'Tıp Fakültesi + Kardiyoloji Uzmanlığı', 'Hastane, Kardiyoloji Merkezi'),
(6, 'Jinekolog', 1, 'Kadın üreme sistemi hastalıklarıyla ilgilenen uzman hekim', 'Tıp Fakültesi + Kadın Hastalıkları Uzmanlığı', 'Hastane, Poliklinik'),
(7, 'Nörolog', 1, 'Sinir sistemi hastalıklarının teşhis ve tedavisini yapan uzman hekim', 'Tıp Fakültesi + Nöroloji Uzmanlığı', 'Hastane, Poliklinik'),
(8, 'Endokrinolog', 1, 'Hormon ve metabolizma hastalıklarıyla ilgilenen uzman hekim', 'Tıp Fakültesi + Endokrinoloji Uzmanlığı', 'Hastane, Poliklinik'),
(9, 'Hematolojist', 1, 'Kan ve kan hücreleri hastalıklarıyla ilgilenen uzman hekim', 'Tıp Fakültesi + Hematoloji Uzmanlığı', 'Hastane, Poliklinik'),
(10, 'Göğüs hastalıkları uzmanı', 1, 'Solunum sistemi hastalıklarının teşhis ve tedavisini yapan uzman hekim', 'Tıp Fakültesi + Göğüs Hastalıkları Uzmanlığı', 'Hastane, Poliklinik'),

-- Tanısal Tıp
(11, 'Patolog', 2, 'Hastalıkların doku ve hücre düzeyinde tanısını koyan laboratuvar uzmanı', 'Tıp Fakültesi + Patoloji Uzmanlığı', 'Hastane, Laboratuvar'),
(12, 'Radyolog', 2, 'Görüntüleme yöntemleriyle (MR, BT, USG vb.) hastalıkları teşhis eden uzman hekim', 'Tıp Fakültesi + Radyoloji Uzmanlığı', 'Hastane, Radyoloji Merkezi'),

-- Cerrahi Olmayan Klinik Dallar
(13, 'Psikiyatr', 3, 'Ruhsal hastalıkların teşhis ve tedavisini yapan, ilaç ve terapi uygulayan hekim', 'Tıp Fakültesi + Psikiyatri Uzmanlığı', 'Hastane, Poliklinik, Özel Muayenehane'),
(14, 'Dermatolog', 3, 'Deri ve cilt hastalıklarının teşhis ve tedavisini yapan uzman hekim', 'Tıp Fakültesi + Dermatoloji Uzmanlığı', 'Hastane, Poliklinik'),
(15, 'Ortopedist', 3, 'Kas-iskelet sistemi hastalıklarının teşhis ve tedavisini yapan cerrahi uzman', 'Tıp Fakültesi + Ortopedi Uzmanlığı', 'Hastane, Poliklinik'),
(16, 'Fizik tedavi uzmanı', 3, 'Fiziksel tıp ve rehabilitasyon uygulamalarını yöneten uzman hekim', 'Tıp Fakültesi + Fizik Tedavi Uzmanlığı', 'Hastane, Rehabilitasyon Merkezi'),

-- Cerrahi Tıp
(17, 'Cerrah', 4, 'Cerrahi operasyonları gerçekleştiren uzman hekim', 'Tıp Fakültesi + Genel Cerrahi Uzmanlığı', 'Hastane, Ameliyathane'),
(18, 'Anestezi uzmanı', 5, 'Ameliyat sırasında anestezi uygulaması yapan ve hastanın yaşamsal fonksiyonlarını izleyen hekim', 'Tıp Fakültesi + Anesteziyoloji Uzmanlığı', 'Hastane, Ameliyathane'),

-- Diş Hekimliği
(19, 'Diş hekimi', 6, 'Ağız, diş ve çene sağlığı hastalıklarının teşhis ve tedavisini yapan diş hekimi', 'Diş Hekimliği Fakültesi', 'Diş Polikliniği, Hastane'),
(20, 'Diş teknisyeni', 7, 'Diş protezleri ve ortodontik apareyleri üreten teknik personel', 'Diş Teknisyenliği Ön Lisans', 'Diş Laboratuvarı'),

-- Veterinerlik
(21, 'Veteriner hekim', 8, 'Hayvan sağlığı ve hastalıklarının teşhis, tedavi ve korunmasıyla ilgilenen hekim', 'Veteriner Fakültesi', 'Veteriner Kliniği, Hayvan Hastanesi'),
(22, 'Veteriner sağlık teknisyeni', 9, 'Veteriner hekime yardımcı olan teknik sağlık personeli', 'Veteriner Sağlık Ön Lisans', 'Veteriner Kliniği, Hayvan Hastanesi'),

-- Hemşirelik ve Ebelik
(23, 'Hemşire', 10, 'Hasta bakımı, tedavi uygulaması ve sağlık takibi yapan sağlık profesyoneli', 'Hemşirelik Lisans', 'Hastane, Sağlık Ocağı, Poliklinik'),
(24, 'Ebe', 11, 'Gebelik, doğum ve lohusalık dönemlerinde bakım hizmeti sunan sağlık profesyoneli', 'Ebelik Lisans', 'Hastane, Doğum Merkezi'),

-- Acil Sağlık
(25, 'Acil tıp teknisyeni', 12, 'Ambulans içinde temel yaşam desteği sağlayan acil sağlık çalışanı', 'ATT Ön Lisans', 'Ambulans, Acil Servis'),
(26, 'Paramedik', 12, 'Acil durumlarda ileri yaşam desteği sağlayan, hastane öncesi acil bakım uzmanı', 'Paramedik Ön Lisans', 'Ambulans, Acil Servis, AFAD'),

-- Tanı Destek
(27, 'Anestezi teknikeri', 13, 'Anestezi uzmanına yardımcı olan, anestezi cihazlarını hazırlayan teknik sağlık personeli', 'Anestezi Ön Lisans', 'Hastane, Ameliyathane'),
(28, 'Radyoloji teknisyeni', 14, 'Röntgen, MR, BT gibi görüntüleme cihazlarını kullanan teknik personel', 'Radyoloji Ön Lisans', 'Hastane, Radyoloji Merkezi'),
(29, 'Laborant', 15, 'Tıbbi laboratuvar testlerini yapan ve analiz sonuçlarını hazırlayan teknik personel', 'Laborant Ön Lisans', 'Hastane, Tıp Laboratuvarı'),

-- Rehabilitasyon
(30, 'Dil ve Konuşma Terapisti', 16, 'Konuşma, dil, ses ve yutma bozukluklarının değerlendirme ve tedavisini yapan terapist', 'DKT Lisans', 'Hastane, Rehabilitasyon Merkezi, Özel Klinik'),
(31, 'Fizyoterapist', 17, 'Hareket ve fonksiyon bozukluklarında egzersiz, manuel terapi ve fiziksel ajanlarla tedavi uygulayan terapist', 'Fizyoterapi Lisans', 'Hastane, Rehabilitasyon Merkezi, Özel Klinik'),
(32, 'Ergoterapist', 18, 'Günlük yaşam aktivitelerinde bağımsızlığı artırmaya yönelik terapi uygulayan uzman', 'Ergoterapi Lisans', 'Hastane, Rehabilitasyon Merkezi, Özel Klinik'),
(33, 'Odyolog', 19, 'İşitme ve denge bozukluklarının değerlendirme ve rehabilitasyonunu yapan uzman', 'Odyoloji Lisans', 'Hastane, İşitme Merkezi'),

-- Beslenme
(34, 'Diyetisyen', 20, 'Beslenme programları hazırlayan, hastalıklara özel diyet tedavisi uygulayan beslenme uzmanı', 'Beslenme ve Diyetetik Lisans', 'Hastane, Özel Klinik, Spor Merkezi'),

-- Görme Sağlığı
(35, 'Optometrist', 21, 'Görme kusurlarını değerlendiren, gözlük ve kontakt lens reçetesi hazırlayan göz sağlığı uzmanı', 'Optometri Lisans', 'Optik Mağaza, Göz Merkezi'),

-- Ruh Sağlığı
(36, 'Psikolog', 22, 'Ruhsal ve davranışsal sorunlarda psikolojik test ve terapi uygulayan ruh sağlığı uzmanı', 'Psikoloji Lisans/Yüksek Lisans', 'Hastane, Özel Klinik, Okul, Şirket'),
(37, 'Psikolojik danışman', 22, 'Bireysel ve grup danışmanlığı ile psikososyal destek sağlayan ruh sağlığı profesyoneli', 'PD Lisans/Yüksek Lisans', 'Okul, Üniversite, Özel Klinik'),

-- Dahili Tıp - yeni
(38, 'İç Hastalıkları Uzmanı', 1, 'Yetişkin iç hastalıklarının teşhis ve tedavisini yapan uzman hekim', 'Tıp Fakültesi + İç Hastalıkları Uzmanlığı', 'Hastane, Poliklinik'),
(39, 'Enfeksiyon Hastalıkları Uzmanı', 1, 'Enfeksiyon hastalıklarının teşhis ve tedavisini yapan uzman hekim', 'Tıp Fakültesi + Enfeksiyon Hastalıkları Uzmanlığı', 'Hastane, Poliklinik'),
(40, 'Onkolog', 1, 'Kanser hastalıklarının teşhis ve tedavisini yapan uzman hekim', 'Tıp Fakültesi + Onkoloji Uzmanlığı', 'Hastane, Onkoloji Merkezi'),
(41, 'Spor Hekimi', 1, 'Spor yaralanmaları ve egzersiz fizyolojisi ile ilgilenen uzman hekim', 'Tıp Fakültesi + Spor Hekimliği Uzmanlığı', 'Hastane, Spor Merkezi'),

-- Tanısal Tıp - yeni
(42, 'Nükleer Tıp Uzmanı', 2, 'Radyoaktif maddelerle tanı ve tedavi uygulayan uzman hekim', 'Tıp Fakültesi + Nükleer Tıp Uzmanlığı', 'Hastane, Nükleer Tıp Merkezi'),
(43, 'Adli Tıp Uzmanı', 2, 'Adli olaylarda tıbbi delil ve otopsi incelemesi yapan uzman hekim', 'Tıp Fakültesi + Adli Tıp Uzmanlığı', 'Adli Tıp Kurumu, Hastane'),
(44, 'Genetik Uzmanı', 2, 'Genetik hastalıkların tanı ve danışmanlığını yapan uzman hekim', 'Tıp Fakültesi + Genetik Uzmanlığı', 'Hastane, Genetik Tanı Merkezi'),

-- Halk Sağlığı
(45, 'Halk Sağlığı Uzmanı', 23, 'Toplum sağlığını koruma ve geliştirmeye yönelik çalışmalar yürüten uzman hekim', 'Tıp Fakültesi + Halk Sağlığı Uzmanlığı', 'Sağlık Müdürlüğü, ASM, Üniversite'),

-- Acil Tıp
(46, 'Acil Tıp Uzmanı', 24, 'Acil serviste kritik hastalara müdahale eden uzman hekim', 'Tıp Fakültesi + Acil Tıp Uzmanlığı', 'Hastane Acil Servis'),

-- Cerrahi alt dallar
(47, 'Beyin Cerrahı', 25, 'Beyin, omurilik ve sinir sistemi ameliyatlarını gerçekleştiren cerrahi uzman', 'Tıp Fakültesi + Nöroşirürji Uzmanlığı', 'Hastane, Ameliyathane'),
(48, 'Kalp ve Damar Cerrahı', 26, 'Kalp, damar ve göğüs cerrahisi operasyonlarını yapan cerrahi uzman', 'Tıp Fakültesi + Kalp ve Damar Cerrahisi Uzmanlığı', 'Hastane, Ameliyathane'),
(49, 'Plastik Cerrah', 27, 'Estetik ve rekonstrüktif cerrahi operasyonları gerçekleştiren cerrahi uzman', 'Tıp Fakültesi + Plastik Cerrahi Uzmanlığı', 'Hastane, Özel Klinik'),
(50, 'Çocuk Cerrahı', 28, 'Bebek ve çocuklarda cerrahi operasyonları yapan cerrahi uzman', 'Tıp Fakültesi + Çocuk Cerrahisi Uzmanlığı', 'Hastane, Ameliyathane'),

-- Perfüzyon
(51, 'Perfüzyonist', 29, 'Kalp-akciğer makinesini kullanarak açık kalp ameliyatlarında yaşamsal fonksiyonları sürdüren sağlık teknisyeni', 'Perfüzyon Lisans/Yüksek Lisans', 'Hastane, Ameliyathane'),

-- Eczacılık
(52, 'Eczacı', 30, 'İlaç hazırlama, danışmanlık ve takibini yapan ilaç uzmanı', 'Eczacılık Fakültesi', 'Eczane, Hastane, İlaç Firması'),
(53, 'Eczane Teknisyeni', 30, 'Eczacıya yardımcı olan, ilaç hazırlama ve sunumunda görevli teknik personel', 'Eczane Hizmetleri Ön Lisans', 'Eczane, Hastane'),

-- Biyomedikal
(54, 'Biyomedikal Mühendisi', 31, 'Tıbbi cihazların tasarım, bakım ve onarımını yapan mühendis', 'Biyomedikal Mühendisliği Lisans', 'Hastane, Medikal Firma, Ar-Ge'),

-- Ameliyathane
(55, 'Ameliyathane Teknikeri', 32, 'Ameliyathane hazırlığı, sterilizasyon ve cerrahi alet yönetiminden sorumlu teknik personel', 'Ameliyathane Hizmetleri Ön Lisans', 'Hastane, Ameliyathane'),

-- Podoloji
(56, 'Podolog', 33, 'Ayak sağlığı, ayak bakımı ve ayak hastalıklarının tedavisinde uzmanlaşmış sağlık profesyoneli', 'Podoloji Lisans', 'Hastane, Özel Klinik, Diyabet Merkezi'),

-- Sağlık Yönetimi
(57, 'Sağlık Yöneticisi', 34, 'Sağlık kurumlarının idari ve operasyonel yönetimini sağlayan yönetici', 'Sağlık Yönetimi Lisans/Yüksek Lisans', 'Hastane, Sağlık Kurumu, Bakanlık'),
(58, 'Tıbbi Sekreter', 34, 'Hasta kayıt, randevu, dosyalama ve tıbbi dokümantasyon işlemlerini yürüten personel', 'Tıbbi Sekreterlik Ön Lisans', 'Hastane, Poliklinik, Sağlık Merkezi'),

-- Evde Bakım
(59, 'Evde Bakım Hemşiresi', 10, 'Ev ortamında hasta bakımı, takibi ve rehabilitasyon hizmeti sunan hemşire', 'Hemşirelik Lisans', 'Evde Bakım Merkezi, Hastane, Özel Kurum');

-- ============================================================
-- ÖRNEK SORGULAR
-- ============================================================

-- Tüm meslekleri ana dallarıyla listele
SELECT 
    a.ad AS ana_dal,
    m.ad AS meslek,
    m.egitim_seviyesi,
    m.calisma_alani
FROM meslekler m
JOIN alt_dallar ad ON m.alt_dal_id = ad.id
JOIN ana_dallar a ON ad.ana_dal_id = a.id
ORDER BY a.sira, m.id;

-- Bir ana dala göre meslekleri getir (örnek: Tıp Doktorları)
SELECT m.ad, m.tanim, m.egitim_seviyesi
FROM meslekler m
JOIN alt_dallar ad ON m.alt_dal_id = ad.id
JOIN ana_dallar a ON ad.ana_dal_id = a.id
WHERE a.id = 1;

-- Eğitim seviyesine göre meslekler
SELECT egitim_seviyesi, COUNT(*) AS meslek_sayisi
FROM meslekler
GROUP BY egitim_seviyesi
ORDER BY meslek_sayisi DESC;
