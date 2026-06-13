-- ============================================================
-- SEED: Meslek Kategorileri ve Meslekler
-- ============================================================
-- Kaynak: Meslek/web/veritabani_postgresql.sql (özet)

INSERT INTO profession_categories (id, name, slug, sort_order) VALUES
    (1, 'Sağlık ve Tıp', 'saglik-ve-tip', 1),
    (2, 'Mühendislik ve Teknik', 'muhendislik-ve-teknik', 2),
    (3, 'Bilişim ve Teknoloji', 'bilisim-ve-teknoloji', 3),
    (4, 'Eğitim ve Akademi', 'egitim-ve-akademi', 4),
    (5, 'Hukuk ve Adalet', 'hukuk-ve-adalet', 5),
    (6, 'İş ve Finans', 'is-ve-finans', 6),
    (7, 'Sanat, Medya ve Eğlence', 'sanat-medya-ve-eglence', 7),
    (8, 'Sanayi ve Üretim', 'sanayi-ve-uretim', 8),
    (9, 'Tarım ve Hayvancılık', 'tarim-ve-hayvancilik', 9),
    (10, 'Gıda ve İçecek', 'gida-ve-icecek', 10),
    (11, 'Ulaşım ve Lojistik', 'ulasim-ve-lojistik', 11),
    (12, 'Kamu ve Yönetim', 'kamu-ve-yonetim', 12),
    (13, 'Perakende ve Satış', 'perakende-ve-satis', 13),
    (14, 'İnşaat ve Yapı', 'insaat-ve-yapi', 14),
    (15, 'Hizmet ve Bakım', 'hizmet-ve-bakim', 15),
    (16, 'Danışmanlık ve Profesyonel Hizmetler', 'danismanlik-ve-profesyonel-hizmetler', 16);

-- Sağlık (ilk 20 örnek)
INSERT INTO professions (id, category_id, name) VALUES
    (1, 1, 'Aile hekimi'), (2, 1, 'Çocuk doktoru'), (3, 1, 'Göz doktoru'),
    (4, 1, 'Ürolog'), (5, 1, 'Kardiyolog'), (6, 1, 'Jinekolog'),
    (7, 1, 'Nörolog'), (8, 1, 'Endokrinolog'), (9, 1, 'Hematolojist'),
    (10, 1, 'Göğüs hastalıkları uzmanı'), (11, 1, 'Patolog'), (12, 1, 'Radyolog'),
    (13, 1, 'Psikiyatr'), (14, 1, 'Dermatolog'), (15, 1, 'Ortopedist'),
    (16, 1, 'Fizik tedavi uzmanı'), (17, 1, 'Cerrah'), (18, 1, 'Anestezi uzmanı'),
    (19, 1, 'Diş hekimi'), (20, 1, 'Diş teknisyeni');

-- Mühendislik
INSERT INTO professions (id, category_id, name) VALUES
    (60, 2, 'İnşaat mühendisi'), (61, 2, 'Makine mühendisi'),
    (62, 2, 'Elektrik mühendisi'), (63, 2, 'Elektronik mühendisi'),
    (64, 2, 'Bilgisayar mühendisi'), (65, 2, 'Yazılım mühendisi'),
    (66, 2, 'Kimya mühendisi'), (67, 2, 'Gıda mühendisi'),
    (68, 2, 'Çevre mühendisi'), (69, 2, 'Endüstri mühendisi'),
    (70, 2, 'Harita mühendisi'), (71, 2, 'Jeoloji mühendisi'),
    (72, 2, 'Jeofizik mühendisi'), (73, 2, 'Metalurji mühendisi'),
    (74, 2, 'Maden mühendisi'), (75, 2, 'Mimar'),
    (76, 2, 'İç mimar'), (77, 2, 'Peyzaj mimarı');

-- Bilişim
INSERT INTO professions (id, category_id, name) VALUES
    (92, 3, 'Bilgisayar programcısı'), (93, 3, 'Yazılım geliştirici'),
    (94, 3, 'Veri bilimcisi'), (95, 3, 'Veritabanı yöneticisi'),
    (96, 3, 'Sistem yöneticisi'), (97, 3, 'Ağ yöneticisi'),
    (98, 3, 'Siber güvenlik uzmanı'), (99, 3, 'Yapay zeka uzmanı'),
    (100, 3, 'UX tasarımcısı'), (101, 3, 'Web geliştirici'),
    (102, 3, 'Mobil uygulama geliştirici'), (103, 3, 'DevOps mühendisi'),
    (104, 3, 'Bulut mimarı');

-- Eğitim
INSERT INTO professions (id, category_id, name) VALUES
    (112, 4, 'Öğretmen'), (113, 4, 'Akademisyen'),
    (114, 4, 'Profesör'), (115, 4, 'Okutman'),
    (116, 4, 'Araştırmacı'), (117, 4, 'Bilim insanı'),
    (118, 4, 'Okul müdürü'), (119, 4, 'Rehber öğretmen'),
    (120, 4, 'Özel eğitim öğretmeni'), (121, 4, 'Kütüphaneci');

-- Hukuk
INSERT INTO professions (id, category_id, name) VALUES
    (152, 5, 'Avukat'), (153, 5, 'Hakim'), (154, 5, 'Savcı'),
    (155, 5, 'Arabulucu'), (156, 5, 'Noter'), (157, 5, 'Hukuk danışmanı');
