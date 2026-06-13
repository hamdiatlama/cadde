-- ============================================================
-- SEED: Araç Kategorileri, Segmentler, Kasa Tipleri, Markalar
-- ============================================================
-- Kaynak: Vasıta/ klasöründeki tüm kategoriler

-- Segmentler
INSERT INTO vehicle_segments (code, name, description) VALUES
    ('A', 'Mini', 'Mini sınıf şehir araçları'),
    ('B', 'Küçük', 'Küçük sınıf binek araçlar'),
    ('C', 'Kompakt', 'Kompakt sınıf aile araçları'),
    ('D', 'Orta', 'Orta sınıf araçlar'),
    ('E', 'Üst Orta', 'Üst orta sınıf araçlar'),
    ('F', 'Lüks', 'Lüks sınıf araçlar'),
    ('J', 'SUV', 'SUV ve crossover araçlar'),
    ('S', 'Spor', 'Spor otomobiller'),
    ('M', 'MPV', 'Çok amaçlı araçlar'),
    ('P', 'Pick-up', 'Kamyonet/pick-up araçlar'),
    ('V', 'Van', 'Van/minibüs araçlar'),
    ('T', 'Ticari', 'Ticari araçlar'),
    ('R', 'Traktör', 'Traktör ve tarım araçları'),
    ('O', 'Ağır Ticari', 'Ağır ticari/kamyon araçlar');

-- Kasa tipleri
INSERT INTO body_types (id, name, slug) VALUES
    (1, 'Sedan', 'sedan'),
    (2, 'Hatchback', 'hatchback'),
    (3, 'Station Wagon', 'station-wagon'),
    (4, 'Coupe', 'coupe'),
    (5, 'Cabrio', 'cabrio'),
    (6, 'SUV', 'suv'),
    (7, 'MPV', 'mpv'),
    (8, 'Pick-up', 'pick-up'),
    (9, 'Van', 'van'),
    (10, 'Fastback', 'fastback'),
    (11, 'Minibüs', 'minibus'),
    (12, 'Kamyon', 'kamyon'),
    (13, 'Traktör', 'traktor'),
    (14, 'Romork/Treyler', 'romork-treyler'),
    (15, 'Motorsiklet', 'motorsiklet');

-- Araç kategorileri (Vasıta klasöründeki 23 kategorinin ana başlıkları)
INSERT INTO vehicle_categories (id, name, slug, sort_order) VALUES
    (1, 'Otomobil', 'otomobil', 1),
    (2, 'SUV & Crossover', 'suv-crossover', 2),
    (3, 'Ticari Hafif', 'ticari-hafif', 3),
    (4, 'Ticari Ağır', 'ticari-agir', 4),
    (5, 'Traktör & Tarım', 'traktor-tarim', 5),
    (6, 'Segment Bazlı', 'segment-bazli', 6),
    (7, 'Özel Amaçlı', 'ozel-amacli', 7),
    (8, 'Römork & Treyler', 'romork-treyler', 8),
    (9, 'Motorsiklet', 'motorsiklet', 9);

-- Örnek markalar (Otomobil kategorisinden)
INSERT INTO vehicle_brands (id, name, slug, country) VALUES
    (1, 'Audi', 'audi', 'Almanya'),
    (2, 'BMW', 'bmw', 'Almanya'),
    (3, 'Mercedes-Benz', 'mercedes-benz', 'Almanya'),
    (4, 'Volkswagen', 'volkswagen', 'Almanya'),
    (5, 'Toyota', 'toyota', 'Japonya'),
    (6, 'Honda', 'honda', 'Japonya'),
    (7, 'Hyundai', 'hyundai', 'Güney Kore'),
    (8, 'Ford', 'ford', 'ABD'),
    (9, 'Renault', 'renault', 'Fransa'),
    (10, 'Fiat', 'fiat', 'İtalya'),
    (11, 'Opel', 'opel', 'Almanya'),
    (12, 'Peugeot', 'peugeot', 'Fransa'),
    (13, 'Nissan', 'nissan', 'Japonya'),
    (14, 'Skoda', 'skoda', 'Çekya'),
    (15, 'Kia', 'kia', 'Güney Kore'),
    (16, 'Volvo', 'volvo', 'İsveç'),
    (17, 'Tesla', 'tesla', 'ABD'),
    (18, 'Togg', 'togg', 'Türkiye'),
    (19, 'Dacia', 'dacia', 'Romanya'),
    (20, 'Seat', 'seat', 'İspanya');

-- Örnek modeller (Audi)
INSERT INTO vehicle_models (id, brand_id, name, segment_code, production_start) VALUES
    (1, 1, 'A3', 'C', 1996), (2, 1, 'A4', 'D', 1994),
    (3, 1, 'A6', 'E', 1994), (4, 1, 'A8', 'F', 1994),
    (5, 1, 'Q5', 'J', 2008), (6, 1, 'Q7', 'J', 2006),
    (7, 1, 'Q8', 'J', 2018), (8, 1, 'TT', 'S', 1998),
    (9, 1, 'e-tron', 'J', 2019);

-- Model-kasa tipi ilişkileri
INSERT INTO vehicle_model_body_types (model_id, body_type_id) VALUES
    (1, 1), (1, 2), (1, 3), (2, 1), (2, 3),
    (3, 1), (3, 3), (4, 1), (5, 6), (6, 6),
    (7, 6), (8, 4), (9, 6);

-- Model-kategori ilişkisi
INSERT INTO vehicle_category_models (category_id, model_id) VALUES
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 8),
    (2, 5), (2, 6), (2, 7), (2, 9);
