# Veritabanı Şeması

## Genel Bakış

```
┌─────────────────────────────────────────────────────────────────┐
│                        SİSTEM YAPISI                            │
├─────────────────────────────────────────────────────────────────┤
│  BİREYSEL HESAP → KURUMSAL HESAP → KAMUSAL HESAP               │
│                                                                 │
│  Bireysel: Kendi adına ürün/video/hizmet satabilir             │
│  Kurumsal: Şirket profili, mağaza, çalışan yönetimi            │
│  Kamusal:  Duyuru, toplu bildirim, resmi rozet                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. KULLANICI VE HESAP YÖNETİMİ

### users (Kullanıcılar)
```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    phone           VARCHAR(20),
    status          VARCHAR(20) DEFAULT 'active',  -- active, suspended, deleted
    email_verified  BOOLEAN DEFAULT FALSE,
    phone_verified  BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### user_profiles (Kullanıcı Profilleri)
```sql
CREATE TABLE user_profiles (
    id              UUID PRIMARY KEY,
    user_id         UUID UNIQUE REFERENCES users(id),
    first_name      VARCHAR(100),
    last_name       VARCHAR(100),
    avatar_url      VARCHAR(500),
    cover_photo_url VARCHAR(500),
    biography       TEXT,
    date_of_birth   DATE,
    gender          VARCHAR(10),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### account_types (Hesap Tipleri)
```sql
CREATE TABLE account_types (
    id              UUID PRIMARY KEY,
    code            VARCHAR(20) UNIQUE NOT NULL,  -- individual, corporate, public
    name            VARCHAR(50) NOT NULL,
    parent_type_id  UUID REFERENCES account_types(id),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Seed: individual(1), corporate(2), public(3)
```

### accounts (Kullanıcı Hesapları)
```sql
CREATE TABLE accounts (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    account_type_id UUID REFERENCES account_types(id),
    display_name    VARCHAR(200),
    slug            VARCHAR(200) UNIQUE,
    status          VARCHAR(20) DEFAULT 'active',
    is_verified     BOOLEAN DEFAULT FALSE,
    settings        JSONB DEFAULT '{}',
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, account_type_id)
);
```

---

## 2. BİREYSEL HESAP MODÜLLERİ

### educations (Eğitimlerim)
```sql
CREATE TABLE educations (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    school_name     VARCHAR(255),
    department      VARCHAR(255),
    degree          VARCHAR(50),  -- high_school, bachelor, master, phd, certificate
    start_date      DATE,
    end_date        DATE,
    gpa             DECIMAL(4,2),
    certificate_url VARCHAR(500),
    is_online       BOOLEAN DEFAULT FALSE,
    platform        VARCHAR(100),  -- udemy, coursera, khan academy
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### careers (Kariyerim)
```sql
CREATE TABLE careers (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    company_name    VARCHAR(255),
    position        VARCHAR(255),
    start_date      DATE,
    end_date        DATE,
    is_current      BOOLEAN DEFAULT FALSE,
    salary_visible  BOOLEAN DEFAULT FALSE,
    salary_amount   DECIMAL(12,2),
    salary_currency VARCHAR(3) DEFAULT 'TRY',
    cv_file_url     VARCHAR(500),
    description     TEXT,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### career_references (Kariyer Referansları)
```sql
CREATE TABLE career_references (
    id              UUID PRIMARY KEY,
    career_id       UUID REFERENCES careers(id),
    full_name       VARCHAR(200),
    position        VARCHAR(200),
    company         VARCHAR(200),
    phone           VARCHAR(20),
    email           VARCHAR(255),
    relationship    VARCHAR(100),
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### contact_information (İletişim Bilgilerim)
```sql
CREATE TABLE contact_information (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    address_line1   VARCHAR(255),
    address_line2   VARCHAR(255),
    city            VARCHAR(100),
    state           VARCHAR(100),
    postal_code     VARCHAR(20),
    country         VARCHAR(100),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### projects (Projelerim)
```sql
CREATE TABLE projects (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    start_date      DATE,
    end_date        DATE,
    status          VARCHAR(20),  -- ongoing, completed, cancelled
    technologies    JSONB DEFAULT '[]',
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### project_media (Proje Medyaları)
```sql
CREATE TABLE project_media (
    id              UUID PRIMARY KEY,
    project_id      UUID REFERENCES projects(id),
    media_type      VARCHAR(20),  -- image, video, link
    url             VARCHAR(500),
    title           VARCHAR(255),
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### training_given (Verdiğim Eğitimler)
```sql
CREATE TABLE training_given (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    start_date      DATE,
    end_date        DATE,
    participant_count INTEGER DEFAULT 0,
    location        VARCHAR(255),
    is_online       BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### social_accounts (Sosyal Medya Hesaplarım)
```sql
CREATE TABLE social_accounts (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    platform        VARCHAR(20),  -- twitter, instagram, linkedin, github, youtube, tiktok
    username        VARCHAR(255),
    url             VARCHAR(500),
    is_verified     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### social_connections (Sosyal Çevrem)
```sql
CREATE TABLE social_connections (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    connected_user_id UUID REFERENCES users(id),
    relationship    VARCHAR(20),  -- friend, family, colleague, other
    status          VARCHAR(20),  -- pending, accepted, rejected, blocked
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, connected_user_id)
);
```

### assets (Varlıklarım)
```sql
CREATE TABLE assets (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    asset_type      VARCHAR(20),  -- real_estate, vehicle, financial, intellectual, other
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    estimated_value DECIMAL(14,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    purchase_date   DATE,
    is_visible      BOOLEAN DEFAULT FALSE,
    document_url    VARCHAR(500),
    metadata        JSONB,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### advisors (Danışmanlarım)
```sql
CREATE TABLE advisors (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    advisor_type    VARCHAR(20),  -- academic, business, legal, financial, other
    full_name       VARCHAR(200),
    specialization  VARCHAR(255),
    company         VARCHAR(255),
    phone           VARCHAR(20),
    email           VARCHAR(255),
    linkedin_url    VARCHAR(500),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### interests (İlgi Alanlarım)
```sql
CREATE TABLE interests (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    category        VARCHAR(20),  -- hobby, interest, skill
    name            VARCHAR(255),
    proficiency     VARCHAR(20),  -- beginner, intermediate, advanced, expert
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### banking_information (Banka Bilgilerim)
```sql
CREATE TABLE banking_information (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    bank_name       VARCHAR(200),
    account_holder  VARCHAR(200),
    iban            VARCHAR(34),
    account_type    VARCHAR(20),  -- checking, savings, business
    is_primary      BOOLEAN DEFAULT FALSE,
    is_verified     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### tax_information (Vergi Bilgilerim)
```sql
CREATE TABLE tax_information (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    tax_number      VARCHAR(50),
    tax_office      VARCHAR(200),
    tax_type        VARCHAR(20),  -- individual, corporate
    is_verified     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### certified_documents (Tescilli Belgelerim)
```sql
CREATE TABLE certified_documents (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    document_type   VARCHAR(20),  -- patent, trademark, certificate, license, other
    title           VARCHAR(255),
    document_number VARCHAR(100),
    issue_date      DATE,
    expiry_date     DATE,
    issuing_authority VARCHAR(255),
    file_url        VARCHAR(500),
    status          VARCHAR(20),  -- active, expired, revoked
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 3. E-TİCARET SİSTEMİ (Bireysel + Kurumsal)

### categories (Kategoriler)
```sql
CREATE TABLE categories (
    id              UUID PRIMARY KEY,
    parent_id       UUID REFERENCES categories(id),
    name            VARCHAR(255),
    slug            VARCHAR(255) UNIQUE,
    icon            VARCHAR(100),
    sort_order      INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### products (Ürünler - Bireysel ve Kurumsal)
```sql
CREATE TABLE products (
    id              UUID PRIMARY KEY,
    seller_id       UUID REFERENCES users(id),
    store_id        UUID REFERENCES stores(id) NULL,  -- kurumsal ise mağaza ID'si
    category_id     UUID REFERENCES categories(id),
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    slug            VARCHAR(255),
    product_type    VARCHAR(20),  -- physical, digital, service
    price           DECIMAL(10,2) NOT NULL,
    compare_price   DECIMAL(10,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    sku             VARCHAR(100),
    stock_quantity  INTEGER,
    is_active       BOOLEAN DEFAULT TRUE,
    is_featured     BOOLEAN DEFAULT FALSE,
    status          VARCHAR(20) DEFAULT 'draft',  -- draft, active, archived
    view_count      INTEGER DEFAULT 0,
    sold_count      INTEGER DEFAULT 0,
    rating_avg      DECIMAL(3,2) DEFAULT 0,
    rating_count    INTEGER DEFAULT 0,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### product_media (Ürün Medyaları)
```sql
CREATE TABLE product_media (
    id              UUID PRIMARY KEY,
    product_id      UUID REFERENCES products(id),
    media_type      VARCHAR(20),  -- image, video
    url             VARCHAR(500),
    alt_text        VARCHAR(255),
    sort_order      INTEGER DEFAULT 0,
    is_primary      BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### digital_products (Dijital Ürünler - Video Eğitimler)
```sql
CREATE TABLE digital_products (
    id              UUID PRIMARY KEY,
    product_id      UUID REFERENCES products(id) UNIQUE,
    content_type    VARCHAR(20),  -- video, ebook, course, webinar
    file_url        VARCHAR(500),
    preview_url     VARCHAR(500),  -- ücretsiz önizleme
    duration_minutes INTEGER,
    chapter_count   INTEGER DEFAULT 0,
    is_downloadable BOOLEAN DEFAULT FALSE,
    access_type     VARCHAR(20),  -- lifetime, subscription, time_limited
    access_days     INTEGER,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### product_chapters (Video Eğitim Bölümleri)
```sql
CREATE TABLE product_chapters (
    id              UUID PRIMARY KEY,
    product_id      UUID REFERENCES digital_products(id),
    title           VARCHAR(255),
    description     TEXT,
    video_url       VARCHAR(500),
    duration_minutes INTEGER,
    sort_order      INTEGER DEFAULT 0,
    is_free         BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### services (Hizmetler - Bireysel)
```sql
CREATE TABLE services (
    id              UUID PRIMARY KEY,
    provider_id     UUID REFERENCES users(id),
    category_id     UUID REFERENCES categories(id),
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    slug            VARCHAR(255),
    price           DECIMAL(10,2),
    price_type      VARCHAR(20),  -- fixed, hourly, custom
    duration_minutes INTEGER,
    location_type   VARCHAR(20),  -- online, onsite, both
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### service_media (Hizmet Medyaları)
```sql
CREATE TABLE service_media (
    id              UUID PRIMARY KEY,
    service_id      UUID REFERENCES services(id),
    media_type      VARCHAR(20),  -- image, video
    url             VARCHAR(500),
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 4. KURUMSAL HESAP MODÜLLERİ

### company_profiles (Şirket Profilleri)
```sql
CREATE TABLE company_profiles (
    id              UUID PRIMARY KEY,
    user_id         UUID UNIQUE REFERENCES users(id),
    company_name    VARCHAR(255),
    logo_url        VARCHAR(500),
    cover_image_url VARCHAR(500),
    description     TEXT,
    sector          VARCHAR(100),
    company_type    VARCHAR(50),  -- llc, joint_stock, sole_proprietorship
    tax_number      VARCHAR(50),
    trade_registry_no VARCHAR(100),
    founded_year    INTEGER,
    employee_count  VARCHAR(20),  -- 1-10, 11-50, 51-200, 201-500, 500+
    website         VARCHAR(500),
    address         TEXT,
    is_verified     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### stores (Mağazalar)
```sql
CREATE TABLE stores (
    id              UUID PRIMARY KEY,
    company_id      UUID REFERENCES company_profiles(id),
    user_id         UUID REFERENCES users(id),  -- bireysel hesap da mağaza açabilir
    name            VARCHAR(255),
    description     TEXT,
    logo_url        VARCHAR(500),
    banner_url      VARCHAR(500),
    slug            VARCHAR(255) UNIQUE,
    is_active       BOOLEAN DEFAULT TRUE,
    commission_rate DECIMAL(5,2) DEFAULT 0.50,
    rating_avg      DECIMAL(3,2) DEFAULT 0,
    rating_count    INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### employees (Çalışanlar)
```sql
CREATE TABLE employees (
    id              UUID PRIMARY KEY,
    company_id      UUID REFERENCES company_profiles(id),
    user_id         UUID REFERENCES users(id),
    position        VARCHAR(255),
    department      VARCHAR(100),
    role            VARCHAR(20),  -- owner, admin, manager, staff, viewer
    hire_date       DATE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(company_id, user_id)
);
```

### employee_permissions (Çalışan Yetkileri)
```sql
CREATE TABLE employee_permissions (
    id              UUID PRIMARY KEY,
    employee_id     UUID REFERENCES employees(id),
    resource        VARCHAR(100),
    action          VARCHAR(20),  -- create, read, update, delete, manage
    granted         BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(employee_id, resource, action)
);
```

### financial_reports (Finansal Raporlar)
```sql
CREATE TABLE financial_reports (
    id              UUID PRIMARY KEY,
    company_id      UUID REFERENCES company_profiles(id),
    report_type     VARCHAR(20),  -- income, expense, sales, tax, custom
    title           VARCHAR(255),
    period_start    DATE,
    period_end      DATE,
    data            JSONB,
    file_url        VARCHAR(500),
    generated_by    UUID REFERENCES users(id),
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 5. KAMUSAL HESAP MODÜLLERİ

### public_announcements (Duyurular)
```sql
CREATE TABLE public_announcements (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    title           VARCHAR(255) NOT NULL,
    content         TEXT NOT NULL,
    priority        VARCHAR(20) DEFAULT 'normal',  -- low, normal, high, urgent
    is_published    BOOLEAN DEFAULT FALSE,
    published_at    TIMESTAMP,
    expires_at      TIMESTAMP,
    target_audience JSONB,
    view_count      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### bulk_notifications (Toplu Bildirimler)
```sql
CREATE TABLE bulk_notifications (
    id              UUID PRIMARY KEY,
    sender_id       UUID REFERENCES users(id),
    title           VARCHAR(255) NOT NULL,
    message         TEXT NOT NULL,
    channel         VARCHAR(20),  -- in_app, email, sms, push
    target_type     VARCHAR(20),  -- all, account_type, segment, custom
    target_filter   JSONB,
    sent_count      INTEGER DEFAULT 0,
    status          VARCHAR(20) DEFAULT 'draft',  -- draft, sending, sent, failed
    scheduled_at    TIMESTAMP,
    sent_at         TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 6. SİPARİŞ VE ÖDEME SİSTEMİ

### orders (Siparişler)
```sql
CREATE TABLE orders (
    id              UUID PRIMARY KEY,
    buyer_id        UUID REFERENCES users(id),
    store_id        UUID REFERENCES stores(id),
    order_number    VARCHAR(50) UNIQUE,
    status          VARCHAR(20),  -- pending, paid, processing, shipped, delivered, cancelled, refunded
    subtotal        DECIMAL(10,2),
    commission_amount DECIMAL(10,2),
    total_amount    DECIMAL(10,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    payment_method  VARCHAR(50),
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### order_items (Sipariş Kalemleri)
```sql
CREATE TABLE order_items (
    id              UUID PRIMARY KEY,
    order_id        UUID REFERENCES orders(id),
    product_id      UUID REFERENCES products(id),
    quantity        INTEGER DEFAULT 1,
    unit_price      DECIMAL(10,2),
    total_price     DECIMAL(10,2),
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### transactions (İşlemler)
```sql
CREATE TABLE transactions (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    order_id        UUID REFERENCES orders(id),
    type            VARCHAR(20),  -- payment, commission, refund, withdrawal, deposit
    amount          DECIMAL(12,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    status          VARCHAR(20),  -- pending, completed, failed, cancelled
    payment_gateway VARCHAR(50),
    gateway_ref     VARCHAR(255),
    description     TEXT,
    metadata        JSONB,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### reviews (Değerlendirmeler)
```sql
CREATE TABLE reviews (
    id              UUID PRIMARY KEY,
    reviewer_id     UUID REFERENCES users(id),
    product_id      UUID REFERENCES products(id),
    store_id        UUID REFERENCES stores(id),
    rating          INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment         TEXT,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 7. ORTAK TABLOLAR

### follows (Takip Sistemi)
```sql
CREATE TABLE follows (
    id              UUID PRIMARY KEY,
    follower_id     UUID REFERENCES users(id),
    following_id    UUID REFERENCES users(id),
    created_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(follower_id, following_id)
);
```

### likes (Beğeniler)
```sql
CREATE TABLE likes (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    content_id      UUID,
    content_type    VARCHAR(20),  -- product, service, post, announcement
    created_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, content_id, content_type)
);
```

### comments (Yorumlar)
```sql
CREATE TABLE comments (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    content_id      UUID,
    content_type    VARCHAR(20),
    parent_id       UUID REFERENCES comments(id),
    body            TEXT,
    status          VARCHAR(20) DEFAULT 'active',
    like_count      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### conversations (Konuşmalar)
```sql
CREATE TABLE conversations (
    id              UUID PRIMARY KEY,
    type            VARCHAR(20) DEFAULT 'direct',  -- direct, group
    name            VARCHAR(200),
    created_by      UUID REFERENCES users(id),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### conversation_members (Konuşma Üyeleri)
```sql
CREATE TABLE conversation_members (
    conversation_id UUID REFERENCES conversations(id),
    user_id         UUID REFERENCES users(id),
    role            VARCHAR(20) DEFAULT 'member',
    joined_at       TIMESTAMP DEFAULT NOW(),
    last_read_at    TIMESTAMP,
    PRIMARY KEY (conversation_id, user_id)
);
```

### messages (Mesajlar)
```sql
CREATE TABLE messages (
    id              UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    sender_id       UUID REFERENCES users(id),
    content         TEXT,
    message_type    VARCHAR(20) DEFAULT 'text',  -- text, image, file, system
    attachment_url  VARCHAR(500),
    is_edited       BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    deleted_at      TIMESTAMP
);
```

### notifications (Bildirimler)
```sql
CREATE TABLE notifications (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    type            VARCHAR(50),
    title           VARCHAR(200),
    message         TEXT,
    data            JSONB,
    is_read         BOOLEAN DEFAULT FALSE,
    read_at         TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### file_uploads (Dosya Yüklemeleri)
```sql
CREATE TABLE file_uploads (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    original_name   VARCHAR(255),
    stored_name     VARCHAR(255) UNIQUE,
    mime_type       VARCHAR(100),
    size_bytes      BIGINT,
    storage_path    VARCHAR(500),
    url             VARCHAR(500),
    uploaded_at     TIMESTAMP DEFAULT NOW()
);
```

### audit_logs (Denetim Kayıtları)
```sql
CREATE TABLE audit_logs (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    action          VARCHAR(100),
    resource_type   VARCHAR(100),
    resource_id     UUID,
    old_values      JSONB,
    new_values      JSONB,
    ip_address      INET,
    user_agent      TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 8. YETKİLENDİRİLMİŞ SATIŞ SİSTEMİ (Komisyonlu Satış)

### listings (İlan Sayfaları)
```sql
-- Gayrimenkul uzmanı, emlakçı, ikinci el satıcıları vb.
-- Kendi ilan sayfalarını oluşturabilir
CREATE TABLE listings (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),  -- İlan sahibi (satıcı)
    store_id        UUID REFERENCES stores(id) NULL,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    slug            VARCHAR(255) UNIQUE,
    cover_image_url VARCHAR(500),
    is_active       BOOLEAN DEFAULT TRUE,
    commission_rate DECIMAL(5,2) DEFAULT 5.00,  -- Varsayılan komisyon oranı
    view_count      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### listing_products (İlan Ürünleri)
```sql
-- İlan sayfasındaki ürünler (araba, ev, arsa vb.)
CREATE TABLE listing_products (
    id              UUID PRIMARY KEY,
    listing_id      UUID REFERENCES listings(id),
    product_id      UUID REFERENCES products(id),
    sort_order      INTEGER DEFAULT 0,
    is_featured     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### product_authorizations (Ürün Satış Yetkileri)
```sql
-- Bir ürünün birden fazla kişi tarafından satılabilmesi için izin sistemi
-- Örnek: Gayrimenkul uzmanı bir evi satacaksa ev sahibinden izin ister
CREATE TABLE product_authorizations (
    id              UUID PRIMARY KEY,
    product_id      UUID REFERENCES products(id),  -- Satılacak ürün
    owner_id        UUID REFERENCES users(id),      -- Ürünün gerçek sahibi
    seller_id       UUID REFERENCES users(id),      -- Satmak isteyen kişi
    status          VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected, revoked
    commission_rate DECIMAL(5,2) DEFAULT 5.00,      -- Anlaşılan komisyon oranı
    commission_type VARCHAR(20) DEFAULT 'percentage', -- percentage, fixed
    commission_amount DECIMAL(10,2),                 -- Sabit komisyon ise tutar
    authorized_at   TIMESTAMP,                       -- Onay tarihi
    expires_at      TIMESTAMP,                       -- Yetki bitiş tarihi
    notes           TEXT,                            -- Ek notlar
    contract_url    VARCHAR(500),                    -- Sözleşme/doküman
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(product_id, seller_id)
);
```

### authorization_requests (Yetki İstekleri)
```sql
-- Satıcıların ürün sahiplerine gönderdiği yetki istekleri
CREATE TABLE authorization_requests (
    id              UUID PRIMARY KEY,
    product_id      UUID REFERENCES products(id),
    requester_id    UUID REFERENCES users(id),      -- İstek gönderen (satıcı)
    owner_id        UUID REFERENCES users(id),      -- İzin istenen kişi (ürün sahibi)
    status          VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected
    message         TEXT,                           -- Satıcının mesajı
    proposed_commission DECIMAL(5,2),               -- Önerilen komisyon oranı
    owner_response  TEXT,                           -- Ürün sahibinin yanıtı
    responded_at    TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(product_id, requester_id)
);
```

### authorized_sales (Onaylı Satışlar)
```sql
-- Tamamlanmış onaylı satışlar
CREATE TABLE authorized_sales (
    id              UUID PRIMARY KEY,
    authorization_id UUID REFERENCES product_authorizations(id),
    order_id        UUID REFERENCES orders(id),
    buyer_id        UUID REFERENCES users(id),
    seller_id       UUID REFERENCES users(id),
    owner_id        UUID REFERENCES users(id),
    product_id      UUID REFERENCES products(id),
    sale_price      DECIMAL(12,2),
    commission_amount DECIMAL(10,2),
    seller_earning  DECIMAL(10,2),
    owner_earning   DECIMAL(10,2),
    status          VARCHAR(20) DEFAULT 'completed',
    sold_at         TIMESTAMP DEFAULT NOW(),
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### commission_settings (Komisyon Ayarları)
```sql
-- Sistem genelinde komisyon ayarları
CREATE TABLE commission_settings (
    id              UUID PRIMARY KEY,
    category_id     UUID REFERENCES categories(id),  -- Kategori bazlı komisyon
    default_rate    DECIMAL(5,2) DEFAULT 5.00,        -- Varsayılan komisyon oranı
    min_rate        DECIMAL(5,2) DEFAULT 1.00,        -- Minimum komisyon
    max_rate        DECIMAL(5,2) DEFAULT 50.00,       -- Maksimum komisyon
    platform_fee    DECIMAL(5,2) DEFAULT 1.00,        -- Platform komisyonu
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### seller_profiles (Satıcı Profilleri)
```sql
-- Satıcıların profilleri ve istatistikleri
CREATE TABLE seller_profiles (
    id              UUID PRIMARY KEY,
    user_id         UUID UNIQUE REFERENCES users(id),
    is_verified     BOOLEAN DEFAULT FALSE,           -- Doğrulanmış satıcı
    total_sales     INTEGER DEFAULT 0,
    total_earning   DECIMAL(14,2) DEFAULT 0,
    commission_owed DECIMAL(14,2) DEFAULT 0,         -- Ödenmemiş komisyon
    rating_avg      DECIMAL(3,2) DEFAULT 0,
    rating_count    INTEGER DEFAULT 0,
    speciality      VARCHAR(100),                    -- Uzmanlık alanı (emlak, araç vb.)
    business_license VARCHAR(100),                   -- İş ruhsatı
    is_realtor      BOOLEAN DEFAULT FALSE,           -- Emlakçı mı?
    is_farmer       BOOLEAN DEFAULT FALSE,           -- Çiftçi mi?
    is_breeder      BOOLEAN DEFAULT FALSE,           -- Hayvan üreticisi mi?
    is_beekeeper    BOOLEAN DEFAULT FALSE,           -- Arıcı mı?
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 9. TARIM, HAYVANCILIK VE ÜRÜN SATIŞ SİSTEMİ

### farm_products (Tarım Ürünleri)
```sql
-- Çiftçilerin tarlada ektiği ürünler
CREATE TABLE farm_products (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),      -- Çiftçi
    product_id      UUID REFERENCES products(id),   -- Satıştaki ürün
    farm_name       VARCHAR(255),                   -- Çiftlik adı
    product_name    VARCHAR(255) NOT NULL,           -- Ürün adı (buğday, pamuk, domates vb.)
    description     TEXT,
    
    -- Tarla Bilgileri
    land_area       DECIMAL(10,2),                   -- Ekili alan (m² veya dönüm)
    land_unit       VARCHAR(10) DEFAULT 'm2',        -- m2, donum, hectare
    land_location   TEXT,                            -- Tarla konumu (il, ilçe, köy)
    latitude        DECIMAL(10,8),                   -- Enlem
    longitude       DECIMAL(11,8),                   -- Boylam
    
    -- Ekim Bilgileri
    planting_date   DATE,                            -- Ekim tarihi
    harvest_date    DATE,                            -- Hasat tahmini
    actual_harvest_date DATE,                        -- Gerçek hasat tarihi
    
    -- Üretim Bilgileri
    total_yield     DECIMAL(10,2),                   -- Toplam üretim miktarı
    yield_unit      VARCHAR(20),                     -- kg, ton, kasa, kutu
    organic         BOOLEAN DEFAULT FALSE,           -- Organik mi?
    certification   VARCHAR(100),                    -- Sertifika (organik, coğrafi işaret vb.)
    
    -- Hasat ve Stok
    harvested       BOOLEAN DEFAULT FALSE,           -- Hasat edildi mi?
    current_stock   DECIMAL(10,2),                   -- Mevcut stok
    stock_unit      VARCHAR(20),
    
    -- Fiyat
    price_per_unit  DECIMAL(10,2),                   -- Birim fiyat
    currency        VARCHAR(3) DEFAULT 'TRY',
    min_order       DECIMAL(10,2),                   -- Minimum sipariş miktarı
    
    -- Görseller
    cover_image     VARCHAR(500),
    
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### farm_product_images (Tarım Ürünü Görselleri)
```sql
CREATE TABLE farm_product_images (
    id              UUID PRIMARY KEY,
    farm_product_id UUID REFERENCES farm_products(id),
    image_url       VARCHAR(500) NOT NULL,
    alt_text        VARCHAR(255),
    sort_order      INTEGER DEFAULT 0,
    is_primary      BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### farm_certifications (Tarım Sertifikaları)
```sql
-- Çiftçinin sertifikaları
CREATE TABLE farm_certifications (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    cert_name       VARCHAR(255) NOT NULL,           -- Organik Tarım, Coğrafi İşaret vb.
    cert_number     VARCHAR(100),                    -- Sertifika numarası
    issuing_authority VARCHAR(255),                  -- Veren kurum
    issue_date      DATE,
    expiry_date     DATE,
    file_url        VARCHAR(500),                    -- Sertifika dosyası
    is_verified     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### livestock_products (Hayvancılık Ürünleri)
```sql
-- Hayvan yetiştiricilerinin ürünleri
CREATE TABLE livestock_products (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),      -- Yetiştirici
    product_id      UUID REFERENCES products(id),
    farm_name       VARCHAR(255),
    
    -- Hayvan Bilgileri
    animal_type     VARCHAR(50) NOT NULL,            -- inek, koyun, keçi, tavuk, balık vb.
    animal_breed    VARCHAR(100),                    -- Cins (Holstein, Merinos vb.)
    animal_count    INTEGER,                         -- Hayvan sayısı
    animal_age_months INTEGER,                       -- Hayvan yaşı (ay)
    gender          VARCHAR(10),                     -- erkek, dişi
    
    -- Üretim Bilgileri (et, süt, yumurta vb.)
    product_type    VARCHAR(50) NOT NULL,            -- et, süt, yumurta, peynir, yoğurt, yağ, bal
    daily_production DECIMAL(10,2),                  -- Günlük üretim
    production_unit VARCHAR(20),                     -- litre, kg, adet
    monthly_capacity DECIMAL(10,2),                  -- Aylık kapasite
    
    -- Fiyat
    price           DECIMAL(10,2),
    price_unit      VARCHAR(20),                     -- litre, kg, adet
    currency        VARCHAR(3) DEFAULT 'TRY',
    min_order       DECIMAL(10,2),
    
    -- Konum ve Koşullar
    location        TEXT,
    is_organic      BOOLEAN DEFAULT FALSE,
    feed_type       VARCHAR(100),                    -- Yem türü (otlama, yemlik vb.)
    
    cover_image     VARCHAR(500),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### livestock_product_images (Hayvancılık Ürünü Görselleri)
```sql
CREATE TABLE livestock_product_images (
    id              UUID PRIMARY KEY,
    livestock_product_id UUID REFERENCES livestock_products(id),
    image_url       VARCHAR(500) NOT NULL,
    alt_text        VARCHAR(255),
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### beekeeping_products (Arıcılık Ürünleri)
```sql
-- Arıcıların ürünleri
CREATE TABLE beekeeping_products (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),      -- Arıcı
    product_id      UUID REFERENCES products(id),
    farm_name       VARCHAR(255),                   -- Arılık adı
    
    -- Arılık Bilgileri
    hive_count      INTEGER,                         -- Kovan sayısı
    location        TEXT,                            -- Arılık konumu
    altitude        INTEGER,                         -- Rakım (metre)
    flowering_area  TEXT,                            -- Çiçeklenme alanı
    
    -- Ürün Bilgisi
    product_type    VARCHAR(50) NOT NULL,            -- bal, polen, arı sütü, propolis, balmumu
    product_name    VARCHAR(255),
    description     TEXT,
    
    -- Bal İçin Özel Bilgiler
    flower_type     VARCHAR(100),                    -- Çiçek türü (keçiboynuzu, çam, ayçiçeği vb.)
    is_raw          BOOLEAN DEFAULT FALSE,           -- Ham bal mı?
    is_organic      BOOLEAN DEFAULT FALSE,
    
    -- Üretim
    annual_production DECIMAL(10,2),                 -- Yıllık üretim
    production_unit VARCHAR(20),                     -- kg, litre
    current_stock   DECIMAL(10,2),
    stock_unit      VARCHAR(20),
    
    -- Fiyat
    price           DECIMAL(10,2),
    price_unit      VARCHAR(20),
    currency        VARCHAR(3) DEFAULT 'TRY',
    min_order       DECIMAL(10,2),
    
    cover_image     VARCHAR(500),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### beekeeping_product_images (Arıcılık Ürünü Görselleri)
```sql
CREATE TABLE beekeeping_product_images (
    id              UUID PRIMARY KEY,
    beekeeping_product_id UUID REFERENCES beekeeping_products(id),
    image_url       VARCHAR(500) NOT NULL,
    alt_text        VARCHAR(255),
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### producer_shops (Üretici Sayfaları / Satış Sayfaları)
```sql
-- Çiftçiler, hayvan yetiştiricileri, arıcılar için satış sayfaları
CREATE TABLE producer_shops (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    shop_name       VARCHAR(255) NOT NULL,
    description     TEXT,
    shop_type       VARCHAR(30) NOT NULL,            -- farm, livestock, beekeeping, mixed
    
    -- Görseller
    logo_url        VARCHAR(500),
    banner_url      VARCHAR(500),
    cover_image     VARCHAR(500),
    
    -- Konum
    location        TEXT,
    city            VARCHAR(100),
    district        VARCHAR(100),
    latitude        DECIMAL(10,8),
    longitude       DECIMAL(11,8),
    
    -- İletişim
    phone           VARCHAR(20),
    whatsapp        VARCHAR(20),
    email           VARCHAR(255),
    
    -- Güvenilirlik
    is_verified     BOOLEAN DEFAULT FALSE,
    rating_avg      DECIMAL(3,2) DEFAULT 0,
    rating_count    INTEGER DEFAULT 0,
    total_sales     INTEGER DEFAULT 0,
    
    -- Ayarlar
    slug            VARCHAR(255) UNIQUE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### producer_shop_products (Üretici Sayfası Ürünleri)
```sql
-- Üretici sayfasındaki ürünlerin listesi
CREATE TABLE producer_shop_products (
    id              UUID PRIMARY KEY,
    shop_id         UUID REFERENCES producer_shops(id),
    product_id      UUID REFERENCES products(id),
    farm_product_id UUID REFERENCES farm_products(id) NULL,
    livestock_product_id UUID REFERENCES livestock_products(id) NULL,
    beekeeping_product_id UUID REFERENCES beekeeping_products(id) NULL,
    sort_order      INTEGER DEFAULT 0,
    is_featured     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### producer_certifications (Üretici Belgeleri)
```sql
-- Üreticinin belgeleri (tarım, hayvancılık, arıcılık için)
CREATE TABLE producer_certifications (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    cert_type       VARCHAR(50),                     -- organic, geographic_indication, quality, other
    cert_name       VARCHAR(255) NOT NULL,
    cert_number     VARCHAR(100),
    issuing_authority VARCHAR(255),
    issue_date      DATE,
    expiry_date     DATE,
    file_url        VARCHAR(500),
    is_verified     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 10. ELEKTRONİK VE İKİNCİ EL PAZARI

### electronics_products (Elektronik Ürünler)
```sql
-- Telefon, tablet, bilgisayar vb. elektronik ürünler
CREATE TABLE electronics_products (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),      -- Satıcı
    product_id      UUID REFERENCES products(id),
    
    -- Ürün Bilgisi
    brand           VARCHAR(100),                    -- Apple, Samsung, Xiaomi vb.
    model           VARCHAR(200),                    -- iPhone 15 Pro Max vb.
    color           VARCHAR(50),
    storage         VARCHAR(20),                     -- 128GB, 256GB vb.
    ram             VARCHAR(20),                     -- 8GB, 12GB vb.
    
    -- Durum
    condition       VARCHAR(20) NOT NULL,            -- new, used, refurbished, open_box
    condition_detail TEXT,                           -- Kullanım durumu açıklaması
    cosmetic_score  INTEGER,                         -- Kozmetik puanı (1-10)
    
    -- Teknik Bilgiler
    screen_size     VARCHAR(20),                     -- 6.7 inç vb.
    battery_health  INTEGER,                         -- Pil sağlık yüzdesi
    imei_number     VARCHAR(20),                     -- IMEI numarası (opsiyonel)
    serial_number   VARCHAR(100),                    -- Seri numarası
    
    -- Garanti
    has_warranty    BOOLEAN DEFAULT FALSE,
    warranty_months INTEGER,
    warranty_provider VARCHAR(100),
    warranty_end_date DATE,
    
    -- Kutu ve Aksesuar
    original_box    BOOLEAN DEFAULT FALSE,
    charger_included BOOLEAN DEFAULT TRUE,
    accessories     JSONB DEFAULT '[]',              -- Kulaklık, kılıf vb.
    
    -- İkinci El İçin
    purchase_date   DATE,                            -- İlk satın alma tarihi
    usage_months    INTEGER,                         -- Kullanım süresi (ay)
    reason_for_sale TEXT,                            -- Satış nedeni
    
    -- Fiyat
    original_price  DECIMAL(12,2),                   -- Orijinal fiyat (sıfır ise)
    current_price   DECIMAL(12,2),                   -- Satış fiyatı
    
    -- Görseller
    cover_image     VARCHAR(500),
    
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### electronics_product_images (Elektronik Ürün Görselleri)
```sql
CREATE TABLE electronics_product_images (
    id                  UUID PRIMARY KEY,
    electronics_product_id UUID REFERENCES electronics_products(id),
    image_url           VARCHAR(500) NOT NULL,
    alt_text            VARCHAR(255),
    sort_order          INTEGER DEFAULT 0,
    is_primary          BOOLEAN DEFAULT FALSE,
    is_detail           BOOLEAN DEFAULT FALSE,      -- Detay görseli mi?
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### electronics_categories (Elektronik Kategorileri)
```sql
-- Elektronik ürün kategorileri
CREATE TABLE electronics_categories (
    id              UUID PRIMARY KEY,
    parent_id       UUID REFERENCES electronics_categories(id),
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE,
    icon            VARCHAR(100),
    sort_order      INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Seed veriler:
-- Telefon, Tablet, Dizüstü Bilgisayar, Masaüstü Bilgisayar
-- Kulaklık, Watch, Kamera, Oyun Konsolu
-- TV, Ses Sistemi, Beyaz Eşya vb.
```

### trade_in_requests (Takas İstekleri)
```sql
-- İkinci el takas sistemi
CREATE TABLE trade_in_requests (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    seller_id       UUID REFERENCES users(id),      -- Satıcı (telefonecu)
    
    -- Takas Edilen Cihaz
    device_brand    VARCHAR(100),
    device_model    VARCHAR(200),
    device_condition VARCHAR(20),                    -- excellent, good, fair, poor
    device_age_months INTEGER,
    device_imei     VARCHAR(20),
    
    -- Alınmak İstenen Cihaz
    target_product_id UUID REFERENCES electronics_products(id),
    
    -- Değerlendirme
    estimated_value DECIMAL(12,2),                   -- Tahmini değer
    final_value     DECIMAL(12,2),                   -- Nihai değer
    status          VARCHAR(20) DEFAULT 'pending',   -- pending, evaluated, approved, completed, rejected
    
    -- Notlar
    user_notes      TEXT,
    seller_notes    TEXT,
    photos          JSONB DEFAULT '[]',              -- Cihaz fotoğrafları
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### warranty_cards (Garanti Kartları)
```sql
-- Satılan ürünlerin garanti bilgileri
CREATE TABLE warranty_cards (
    id              UUID PRIMARY KEY,
    order_id        UUID REFERENCES orders(id),
    product_id      UUID REFERENCES electronics_products(id),
    buyer_id        UUID REFERENCES users(id),
    seller_id       UUID REFERENCES users(id),
    
    warranty_type   VARCHAR(50),                     -- manufacturer, seller, extended
    warranty_months INTEGER,
    start_date      DATE,
    end_date        DATE,
    
    -- Garanti Şartları
    coverage        TEXT,                            -- Neleri kapsıyor
    exclusions      TEXT,                            -- İstisnalar
    
    -- Belge
    card_number     VARCHAR(100),
    file_url        VARCHAR(500),                    -- Garanti belgesi
    
    status          VARCHAR(20) DEFAULT 'active',    -- active, expired, voided
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### device_conditions (Cihaz Durum Geçmişi)
```sql
-- İkinci el cihazların durum geçmişi
CREATE TABLE device_conditions (
    id              UUID PRIMARY KEY,
    electronics_product_id UUID REFERENCES electronics_products(id),
    checked_by      UUID REFERENCES users(id),
    
    -- Kontrol Detayları
    screen_condition VARCHAR(20),                    -- excellent, good, fair, poor, cracked
    body_condition  VARCHAR(20),                     -- excellent, good, fair, poor
    battery_health  INTEGER,                         -- Pil sağlık %
    functionality   JSONB DEFAULT '{}',              -- Fonksiyon testleri
    
    -- Fotoğraflar
    photos          JSONB DEFAULT '[]',
    
    notes           TEXT,
    checked_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 11. SEKTÖR VE MESLEK SİSTEMİ

### sectors (Sektörler)
```sql
-- Tüm sektörlerin listesi
CREATE TABLE sectors (
    id              UUID PRIMARY KEY,
    parent_id       UUID REFERENCES sectors(id),     -- Alt sektörler için
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE,
    icon            VARCHAR(100),
    description     TEXT,
    sort_order      INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ANA SEKTÖRLER:
-- 1. Tarım ve Hayvancılık
-- 2. Gıda ve İçecek
-- 3. Tekstil ve Giyim
-- 4. İmalat ve Üretim
-- 5. İnşaat ve Gayrimenkul
-- 6. Enerji ve Madencilik
-- 7. Ulaştırma ve Lojistik
-- 8. Bilgi Teknolojileri
-- 9. Telekomünikasyon
-- 10. Bankacılık ve Finans
-- 11. Sigortacılık
-- 12. Sağlık
-- 13. Eğitim
-- 14. Hukuk
-- 15. Muhasebe ve Denetim
-- 16. Pazarlama ve Reklam
-- 17. Medya ve Yayın
-- 18. Turizm ve Otelcilik
-- 19. Eğlence ve Sanat
-- 20. Spor
-- 21. Perakende
-- 22. Toptan Ticaret
-- 23. E-Ticaret
-- 24. Otomotiv
-- 25. Beyaz Eşya ve Elektronik
-- 26. Mobilya ve Dekorasyon
-- 27. Kimya ve Plastik
-- 28. Kağıt ve Baskı
-- 29. Ambalaj
-- 30. Çevre ve Geri Dönüşüm
-- 31. Savunma Sanayii
-- 32. Havacılık ve Uzay
-- 33. Denizcilik
-- 34. Su Ürünleri
-- 35. Ormancılık
-- 36. Madencilik
-- 37. Petrol ve Gaz
-- 38. İnşaat Malzemeleri
-- 39. Makine ve Ekipman
-- 40. Metal ve Metal Ürünleri
-- 41. Cam ve Seramik
-- 42. Deri ve Deri Ürünleri
-- 43. Kauçuk ve Plastik
-- 44. Mobilya Üretimi
-- 45. Gıda İşleme
-- 46. İçecek Üretimi
-- 47. Tütün Ürünleri
-- 48. İlaç
-- 49. Tıbbi Cihazlar
-- 50. Biyoteknoloji
```

### professions (Meslekler)
```sql
-- Tüm mesleklerin listesi
CREATE TABLE professions (
    id              UUID PRIMARY KEY,
    sector_id       UUID REFERENCES sectors(id),     -- Hangi sektöre ait
    parent_id       UUID REFERENCES professions(id), -- Alt meslekler için
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE,
    description     TEXT,
    
    -- Hizmet Türü
    service_type    VARCHAR(20),                     -- service, product, both
    is_service      BOOLEAN DEFAULT TRUE,            -- Hizmet veriyor mu?
    is_product      BOOLEAN DEFAULT FALSE,           -- Ürün satıyor mu?
    
    -- Gereksinimler
    requires_license BOOLEAN DEFAULT FALSE,          -- Lisans gerektiriyor mu?
    requires_certification BOOLEAN DEFAULT FALSE,    -- Sertifika gerektiriyor mu?
    education_level VARCHAR(50),                     -- Gereken eğitim seviyesi
    
    -- Konum
    is_mobile       BOOLEAN DEFAULT FALSE,           -- Adrese gelebiliyor mu?
    is_remote       BOOLEAN DEFAULT FALSE,           -- Uzaktan hizmet verebiliyor mu?
    is_office       BOOLEAN DEFAULT FALSE,           -- Kendi dükkanı/ofisi var mı?
    
    icon            VARCHAR(100),
    sort_order      INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- MESLEK ÖRNEKLERİ:
-- TARIM SEKTÖRÜ:
--   Çiftçi, Ziraat Mühendisi, Tarım İşçisi, Sera İşçisi, Sulama Uzmanı
--   Bağcılık Uzmanı, Bahçecilik Uzmanı, Toprak Analiz Uzmanı
  
-- HAYVANCILIK SEKTÖRÜ:
--   Hayvan Yetiştiricisi, Veteriner, Zooteknist, Hayvan Sağlığı Teknisyeni
--   Arıcı, Balıkçı, Kuş Yetiştiricisi
  
-- İNŞAAT SEKTÖRÜ:
--   İnşaat Mühendisi, Mimar, Makine Mühendisi, Elektrik Mühendisi
--   İnşaat İşçisi, Duvar Ustası, Alçı Ustası, Boya Ustası
--   Tesisatçı, Kalebodurcu, Çatı Ustası, Kaynakçı
--   Demirci, Kalıpçı, Seramikçi, Parkeci
  
-- SAĞLIK SEKTÖRÜ:
--   Doktor, Hemşire, Eczacı, Diş Hekimi, Psikolog
--   Fizyoterapist, Diyetisyen, Ebe, Tıbbi Sekreter
  
-- EĞİTİM SEKTÖRÜ:
--   Öğretmen, Akademisyen, Eğitmen, Koç, Mentor
--   Özel Ders Öğretmeni, Online Eğitim Uzmanı
  
-- TEKNOLOJİ SEKTÖRÜ:
--   Yazılımcı, Web Tasarımcı, Grafik Tasarımcı, Veri Analisti
--   Siber Güvenlik Uzmanı, Sistem Yöneticisi, Network Mühendisi
  
-- HUKUK SEKTÖRÜ:
--   Avukat, Hukuk Danışmanı, Arabulucu, Noter
  
-- MUHASEBE SEKTÖRÜ:
--   Muhasebeci, Mali Müşavir, Denetçi, Finans Uzmanı
  
-- OTOMOTİV SEKTÖRÜ:
--   Otomobil Tamircisi, Oto Elektrikçisi, Oto Boyacısı
--   Oto Kaportacı, Oto Lastikçi, Oto Yıkamacı
  
-- ELEKTRONİK SEKTÖRÜ:
--   Elektronik Tamircisi, Telefon Tamircisi, Bilgisayar Tamircisi
--   Klima Tamircisi, Beyaz Eşya Tamircisi
  
-- EV HİZMETLERİ:
--   Temizlikçi, Çilingir, Badana Ustası, Su Tesisatçısı
--   Elektrikçi, Camcı, Marangoz, Beyaz Eşya Servisi
  
-- GÜZELLİK SEKTÖRÜ:
--   Kuaför, Berber, Güzellik Uzmanı, Makyaj Uzmanı
--   Cilt Bakım Uzmanı, Manikürcü, Pedikürcü
  
-- SPOR SEKTÖRÜ:
--   Antrenör, Personal Trainer, Yoga Eğitmeni, Pilates Eğitmeni
  
-- SANAT SEKTÖRÜ:
--   Müzisyen, Fotoğrafçı, Video Çekim Uzmanı, Düğün Fotoğrafçısı
  
-- TURİZM SEKTÖRÜ:
--   Seyahat Acentası, Tur Rehberi, Otel İşletmecisi, Restoran
  
-- LOJİSTİK SEKTÖRÜ:
--   Nakliyatçı, Kurye, Depo İşçisi, Gümrük Müşaviri
  
-- SAVUNMA SANAYİİ:
--   Savunma Mühendisi, Güvenlik Görevlisi, Koruma
  
-- VE DAHA FAZLASI...
```

### profession_skills (Meslek Becerileri)
```sql
-- Her mesleğin gerektirdiği beceriler
CREATE TABLE profession_skills (
    id              UUID PRIMARY KEY,
    profession_id   UUID REFERENCES professions(id),
    skill_name      VARCHAR(255) NOT NULL,
    description     TEXT,
    required_level  VARCHAR(20),                     -- beginner, intermediate, advanced, expert
    is_mandatory    BOOLEAN DEFAULT TRUE,             -- Zorunlu mu?
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### user_professions (Kullanıcı Meslekleri)
```sql
-- Kullanıcıların sahip olduğu meslekler
CREATE TABLE user_professions (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    profession_id   UUID REFERENCES professions(id),
    sector_id       UUID REFERENCES sectors(id),
    
    -- Deneyim
    experience_years INTEGER,                        -- Deneyim yılı
    experience_months INTEGER,                       -- Deneyim ayı
    
    -- Uzmanlık
    expertise_level VARCHAR(20),                     -- beginner, intermediate, advanced, expert
    speciality      TEXT,                            -- Özel uzmanlık alanı
    
    -- Belgeler
    has_license     BOOLEAN DEFAULT FALSE,
    license_number  VARCHAR(100),
    license_expiry  DATE,
    has_certification BOOLEAN DEFAULT FALSE,
    certifications  JSONB DEFAULT '[]',
    
    -- Çalışma Durumu
    is_available    BOOLEAN DEFAULT TRUE,            -- Müsait mi?
    availability    VARCHAR(20),                     -- full_time, part_time, freelance, contract
    hourly_rate     DECIMAL(10,2),                   -- Saatlik ücret
    daily_rate      DECIMAL(10,2),                   -- Günlük ücret
    project_rate    DECIMAL(10,2),                   -- Proje bazlı ücret
    currency        VARCHAR(3) DEFAULT 'TRY',
    
    -- Konum
    service_area    JSONB DEFAULT '[]',              -- Hizmet verdiği bölgeler
    is_mobile       BOOLEAN DEFAULT FALSE,           -- Adrese gelebiliyor mu?
    is_remote       BOOLEAN DEFAULT FALSE,           -- Uzaktan hizmet verebiliyor mu?
    
    -- Durum
    is_primary      BOOLEAN DEFAULT FALSE,           -- Asıl mesleği mi?
    is_verified     BOOLEAN DEFAULT FALSE,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, profession_id)
);
```

### service_listings (Hizmet İlanları)
```sql
-- Kullanıcıların hizmet ilanları
CREATE TABLE service_listings (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    profession_id   UUID REFERENCES professions(id),
    sector_id       UUID REFERENCES sectors(id),
    
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    slug            VARCHAR(255) UNIQUE,
    
    -- Hizmet Detayları
    service_type    VARCHAR(20),                     -- fixed, hourly, daily, project
    price           DECIMAL(10,2),
    price_min       DECIMAL(10,2),                   -- Minimum fiyat
    price_max       DECIMAL(10,2),                   -- Maksimum fiyat
    currency        VARCHAR(3) DEFAULT 'TRY',
    
    -- Konum
    location_type   VARCHAR(20),                     -- online, onsite, both
    address         TEXT,
    city            VARCHAR(100),
    district        VARCHAR(100),
    neighborhood    VARCHAR(100),
    latitude        DECIMAL(10,8),
    longitude       DECIMAL(11,8),
    service_radius  INTEGER DEFAULT 10,              -- Hizmet yarıçapı (km)
    
    -- Çalışma Saatleri
    working_hours   JSONB DEFAULT '{}',              -- Haftalık çalışma saatleri
    is_24_7         BOOLEAN DEFAULT FALSE,
    appointment_required BOOLEAN DEFAULT FALSE,
    
    -- Durum
    is_available    BOOLEAN DEFAULT TRUE,            -- Açık/Kapalı
    is_active       BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE,
    
    -- İstatistikler
    view_count      INTEGER DEFAULT 0,
    contact_count   INTEGER DEFAULT 0,
    booking_count   INTEGER DEFAULT 0,
    rating_avg      DECIMAL(3,2) DEFAULT 0,
    rating_count    INTEGER DEFAULT 0,
    
    -- Görseller
    cover_image     VARCHAR(500),
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### service_listing_images (Hizmet İlanı Görselleri)
```sql
CREATE TABLE service_listing_images (
    id              UUID PRIMARY KEY,
    service_listing_id UUID REFERENCES service_listings(id),
    image_url       VARCHAR(500) NOT NULL,
    alt_text        VARCHAR(255),
    sort_order      INTEGER DEFAULT 0,
    is_primary      BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### service_categories (Hizmet Kategorileri)
```sql
-- Hizmet kategorileri (sektör ve mesleklerden bağımsız)
CREATE TABLE service_categories (
    id              UUID PRIMARY KEY,
    parent_id       UUID REFERENCES service_categories(id),
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE,
    icon            VARCHAR(100),
    sort_order      INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ANA KATEGORİLER:
-- 1. Ev Hizmetleri
--    - Temizlik, Badana, Tesisat, Elektrik, Çilingir, Marangoz
-- 2. İnşaat
--    - Duvar, Alçı, Çatı, Kalebodur, Havuz, Peyzaj
-- 3. Taşımacılık
--    - Nakliyat, Kurye, Lojistik, Depo
-- 4. Eğitim
--    - Özel Ders, Online Kurs, Koçluk, Mentörlük
-- 5. Sağlık
--    - Muayene, Tedavi, Bakım, Fizyoterapi
-- 6. Hukuk
--    - Danışmanlık, Dava, Arabuluculuk, Noter
-- 7. Finans
--    - Muhasebe, Vergi, Yatırım, Sigorta
-- 8. Pazarlama
--    - Dijital Pazarlama, SEO, Sosyal Medya, Reklam
-- 9. Teknoloji
--    - Yazılım, Web, Mobil, Veri, Güvenlik
-- 10. Tasarım
--     - Grafik, Mimar, İç Mekan, Ürün Tasarımı
-- 11. Medya
--     - Fotoğraf, Video, Ses, Yayin
-- 12. Hukuk
--     - Avukatlık, Danışmanlık, Arabuluculuk
-- 13. Otomotiv
--     - Tamir, Bakım, Boya, Kaporta, Yıkama
-- 14. Elektronik
--     - Tamir, Kurulum, Bakım, Servis
-- 15. Güzellik
--     - Kuaför, Berber, Cilt Bakımı, Makyaj
-- 16. Spor
--     - Antrenman, Koçluk, Yoga, Pilates
-- 17. Eğlence
--     - Düğün, Organizasyon, DJ, Müzisyen
-- 18. Turizm
--     - Seyahat, Tur, Otel, Rehberlik
-- 19. Güvenlik
--     - Güvenlik Görevlisi, Koruma, Alarm
-- 20. Çevre
--     - Temizlik, Geri Dönüşüm, Danışmanlık
```

### service_bookings (Hizmet Randevuları)
```sql
-- Hizmet randevu sistemi
CREATE TABLE service_bookings (
    id              UUID PRIMARY KEY,
    service_listing_id UUID REFERENCES service_listings(id),
    provider_id     UUID REFERENCES users(id),       -- Hizmet veren
    client_id       UUID REFERENCES users(id),       -- Hizmet alan
    
    -- Randevu Bilgileri
    booking_date    DATE NOT NULL,
    booking_time    TIME NOT NULL,
    end_time        TIME,
    duration_minutes INTEGER,
    
    -- Hizmet Detayları
    service_description TEXT,
    location        TEXT,
    address         TEXT,
    
    -- Fiyat
    quoted_price    DECIMAL(10,2),
    final_price     DECIMAL(10,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    payment_method  VARCHAR(50),
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'pending',   -- pending, confirmed, in_progress, completed, cancelled
    cancellation_reason TEXT,
    
    -- Değerlendirme
    rating          INTEGER CHECK(rating BETWEEN 1 AND 5),
    review          TEXT,
    reviewed_at     TIMESTAMP,
    
    -- Notlar
    client_notes    TEXT,
    provider_notes  TEXT,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### location_search (Konum Arama)
```sql
-- Yakın çevrede hizmet arama için
CREATE TABLE location_search (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    search_query    VARCHAR(500),
    sector_id       UUID REFERENCES sectors(id),
    profession_id   UUID REFERENCES professions(id),
    category_id     UUID REFERENCES service_categories(id),
    latitude        DECIMAL(10,8),
    longitude       DECIMAL(11,8),
    radius_km       INTEGER DEFAULT 10,
    results_count   INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### favorites (Favoriler)
```sql
-- Kullanıcıların favori hizmet/satıcı listesi
CREATE TABLE favorites (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    service_listing_id UUID REFERENCES service_listings(id),
    seller_id       UUID REFERENCES users(id),
    product_id      UUID REFERENCES products(id),
    created_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, service_listing_id)
);
```

---

## 12. ÇİFT YÖNLÜ HİZMET SİSTEMİ

### dual_roles (Çift Rollü Kullanıcılar)
```sql
-- Bir kullanıcının hem hizmet veren hem hizmet alan olabilmesi
CREATE TABLE dual_roles (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    
    -- Hizmet Veren Rolü
    is_provider     BOOLEAN DEFAULT FALSE,            -- Hizmet veriyor mu?
    provider_status VARCHAR(20) DEFAULT 'inactive',   -- active, inactive, busy
    
    -- Hizmet Alan Rolü
    is_client       BOOLEAN DEFAULT FALSE,            -- Hizmet alıyor mu?
    client_status   VARCHAR(20) DEFAULT 'active',     -- active, inactive
    
    -- Çalışma Durumu
    is_currently_working BOOLEAN DEFAULT FALSE,       -- Şu an çalışıyor mu?
    current_task    TEXT,                             -- Şu an ne yapıyor?
    
    -- İstatistikler (Hizmet Veren)
    total_jobs_done INTEGER DEFAULT 0,                -- Toplam yapılan iş
    total_earned    DECIMAL(14,2) DEFAULT 0,          -- Toplam kazanç
    
    -- İstatistikler (Hizmet Alan)
    total_orders    INTEGER DEFAULT 0,                -- Toplam sipariş
    total_spent     DECIMAL(14,2) DEFAULT 0,          -- Toplam harcama
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id)
);
```

### provider_tasks (Hizmet Veren Görevleri)
```sql
-- Hizmet verenin aktif görevleri
CREATE TABLE provider_tasks (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),        -- Hizmet veren
    booking_id      UUID REFERENCES service_bookings(id),
    
    -- Görev Bilgileri
    task_title      VARCHAR(255),
    task_description TEXT,
    task_type       VARCHAR(20),                      -- service, delivery, installation
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'pending',     -- pending, in_progress, completed, on_hold
    started_at      TIMESTAMP,
    completed_at    TIMESTAMP,
    
    -- Konum
    location        TEXT,
    latitude        DECIMAL(10,8),
    longitude       DECIMAL(11,8),
    
    -- Notlar
    notes           TEXT,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### client_requests (Hizmet Alan İstekleri)
```sql
-- Hizmet alan kişinin gönderdiği istekler
CREATE TABLE client_requests (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),        -- Hizmet alan
    
    -- İstek Bilgileri
    request_type    VARCHAR(30),                      -- service, product, delivery
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    
    -- Kategori
    sector_id       UUID REFERENCES sectors(id),
    profession_id   UUID REFERENCES professions(id),
    category_id     UUID REFERENCES service_categories(id),
    
    -- Fiyat
    budget_min      DECIMAL(10,2),
    budget_max      DECIMAL(10,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    
    -- Konum
    location_type   VARCHAR(20),                      -- online, onsite, both
    address         TEXT,
    city            VARCHAR(100),
    district        VARCHAR(100),
    latitude        DECIMAL(10,8),
    longitude       DECIMAL(11,8),
    
    -- Zaman
    preferred_date  DATE,
    preferred_time  TIME,
    is_urgent       BOOLEAN DEFAULT FALSE,
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'open',        -- open, matched, in_progress, completed, cancelled
    matched_provider_id UUID REFERENCES users(id),    -- Eşleşen hizmet veren
    
    -- Fotoğraflar
    photos          JSONB DEFAULT '[]',
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### provider_offers (Hizmet Veren Teklifleri)
```sql
-- Hizmet verenlerin isteklere verdiği teklifler
CREATE TABLE provider_offers (
    id              UUID PRIMARY KEY,
    request_id      UUID REFERENCES client_requests(id),
    provider_id     UUID REFERENCES users(id),
    
    -- Teklif
    offer_price     DECIMAL(10,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    estimated_duration INTEGER,                        -- Tahmini süre (dakika)
    proposal        TEXT,                             -- Teklif açıklaması
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'pending',     -- pending, accepted, rejected, expired
    
    -- Yanıt
    client_response TEXT,
    responded_at    TIMESTAMP,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### marketplace_orders (Pazar Yeri Siparişleri)
```sql
-- Pazar yerindeki siparişler (hizmet alan → ürün/hizmet satıcısı)
CREATE TABLE marketplace_orders (
    id              UUID PRIMARY KEY,
    buyer_id        UUID REFERENCES users(id),         -- Hizmet alan (alıcı)
    seller_id       UUID REFERENCES users(id),         -- Satıcı
    provider_id     UUID REFERENCES users(id),         -- Hizmet veren (farklı olabilir)
    
    -- Sipariş Türü
    order_type      VARCHAR(30),                       -- product, service, delivery, mixed
    
    -- Ürün/Hizmet
    product_id      UUID REFERENCES products(id),
    service_listing_id UUID REFERENCES service_listings(id),
    service_booking_id UUID REFERENCES service_bookings(id),
    
    -- Miktar ve Fiyat
    quantity        INTEGER DEFAULT 1,
    unit_price      DECIMAL(10,2),
    total_price     DECIMAL(10,2),
    commission      DECIMAL(10,2),
    delivery_fee    DECIMAL(10,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    
    -- Teslimat
    delivery_type   VARCHAR(20),                       -- pickup, delivery, both
    delivery_address TEXT,
    delivery_date   DATE,
    delivery_time   TIME,
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'pending',     -- pending, confirmed, preparing, shipping, delivered, completed
    
    -- Ödeme
    payment_method  VARCHAR(50),
    payment_status  VARCHAR(20) DEFAULT 'pending',     -- pending, paid, refunded
    
    -- Notlar
    buyer_notes     TEXT,
    seller_notes    TEXT,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### marketplace_messages (Pazar Yeri Mesajları)
```sql
-- Hizmet alan ve veren arasındaki mesajlaşma
CREATE TABLE marketplace_messages (
    id              UUID PRIMARY KEY,
    order_id        UUID REFERENCES marketplace_orders(id),
    sender_id       UUID REFERENCES users(id),
    receiver_id     UUID REFERENCES users(id),
    
    message         TEXT NOT NULL,
    message_type    VARCHAR(20) DEFAULT 'text',        -- text, image, file, location
    
    is_read         BOOLEAN DEFAULT FALSE,
    read_at         TIMESTAMP,
    
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### quick_service (Hızlı Hizmet)
```sql
-- Acil/hızlı hizmet istekleri (usta bul, tamirci bul vb.)
CREATE TABLE quick_service (
    id              UUID PRIMARY KEY,
    requester_id    UUID REFERENCES users(id),         -- İstek sahibi
    
    -- İstek
    service_type    VARCHAR(255) NOT NULL,             -- "Alçı ustası", "Su tesisatçısı" vb.
    description     TEXT,
    urgency         VARCHAR(20) DEFAULT 'normal',      -- low, normal, high, urgent
    
    -- Konum
    address         TEXT,
    city            VARCHAR(100),
    district        VARCHAR(100),
    neighborhood    VARCHAR(100),
    latitude        DECIMAL(10,8),
    longitude       DECIMAL(11,8),
    
    -- Fiyat
    budget          DECIMAL(10,2),
    is_negotiable   BOOLEAN DEFAULT TRUE,
    
    -- Fotoğraflar
    photos          JSONB DEFAULT '[]',
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'open',        -- open, matched, in_progress, completed, cancelled
    matched_provider_id UUID REFERENCES users(id),
    
    -- Zaman
    desired_date    DATE,
    desired_time    TIME,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### provider_responses (Hizmet Veren Yanıtları)
```sql
-- Hızlı hizmet isteklerine gelen yanıtlar
CREATE TABLE provider_responses (
    id              UUID PRIMARY KEY,
    quick_service_id UUID REFERENCES quick_service(id),
    provider_id     UUID REFERENCES users(id),
    
    -- Yanıt
    message         TEXT,
    estimated_price DECIMAL(10,2),
    estimated_duration INTEGER,                        -- Dakika cinsinden
    can_come_at     TIMESTAMP,                        -- Ne zaman gelebilir
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'pending',     -- pending, accepted, rejected
    
    -- Değerlendirme
    client_rating   INTEGER,
    client_review   TEXT,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### working_status (Çalışma Durumu)
```sql
-- Hizmet verenlerin anlık çalışma durumu
CREATE TABLE working_status (
    id              UUID PRIMARY KEY,
    user_id         UUID UNIQUE REFERENCES users(id),
    
    is_online       BOOLEAN DEFAULT FALSE,            -- Çevrimiçi mi?
    is_available    BOOLEAN DEFAULT TRUE,             -- Müsait mi?
    is_busy         BOOLEAN DEFAULT FALSE,            -- Meşgul mü?
    
    -- Konum (gerçek zamanlı)
    current_location TEXT,
    latitude        DECIMAL(10,8),
    longitude       DECIMAL(11,8),
    last_location_update TIMESTAMP,
    
    -- Mevcut Görev
    current_task_id UUID REFERENCES provider_tasks(id),
    task_started_at TIMESTAMP,
    estimated_end   TIMESTAMP,
    
    -- Ayarlar
    auto_accept     BOOLEAN DEFAULT FALSE,            -- Otomatik kabul
    max_distance    INTEGER DEFAULT 10,               -- Maksimum mesafe (km)
    
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### review_system (Değerlendirme Sistemi)
```sql
-- Hem hizmet veren hem hizmet alan değerlendirmesi
CREATE TABLE review_system (
    id              UUID PRIMARY KEY,
    
    -- Değerlendirme Yapan
    reviewer_id     UUID REFERENCES users(id),
    reviewer_type   VARCHAR(20),                      -- provider, client
    
    -- Değerlendirilen
    reviewee_id     UUID REFERENCES users(id),
    reviewee_type   VARCHAR(20),                      -- provider, client
    
    -- İlişki
    order_id        UUID REFERENCES marketplace_orders(id),
    booking_id      UUID REFERENCES service_bookings(id),
    
    -- Değerlendirme
    rating          INTEGER CHECK(rating BETWEEN 1 AND 5),
    title           VARCHAR(255),
    comment         TEXT,
    
    -- Kategori Bazlı
    quality_rating  INTEGER CHECK(quality_rating BETWEEN 1 AND 5),
    punctuality_rating INTEGER CHECK(punctuality_rating BETWEEN 1 AND 5),
    communication_rating INTEGER CHECK(communication_rating BETWEEN 1 AND 5),
    value_rating    INTEGER CHECK(value_rating BETWEEN 1 AND 5),
    
    -- Yanıt
    response        TEXT,
    response_date   TIMESTAMP,
    
    -- Fotoğraflar
    photos          JSONB DEFAULT '[]',
    
    is_visible      BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 13. TAKSİCİLİK VE ARAÇ TABANLI HİZMET SİSTEMİ

> Taksi sistemi detaylı tasarımı için → [TAXI-SYSTEM-DESIGN.md](./TAXI-SYSTEM-DESIGN.md)

### vehicle_fleet (Araç Filosu)
```sql
-- Taksi, otobüs, kamyon vb. araçların yönetimi
CREATE TABLE vehicle_fleet (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),        -- Araç sahibi
    company_id      UUID REFERENCES company_profiles(id) NULL, -- Kurumsal ise
    
    -- Araç Bilgileri
    vehicle_type    VARCHAR(30) NOT NULL,             -- taxi, bus, truck, van, motorcycle, cargo
    brand           VARCHAR(100),                     -- Renault, Fiat, Toyota vb.
    model           VARCHAR(100),                     -- Megane, Egea, Corolla vb.
    year            INTEGER,
    color           VARCHAR(50),
    plate_number    VARCHAR(20) UNIQUE,               -- Plaka numarası
    
    -- Teknik Bilgiler
    engine_type     VARCHAR(20),                      -- diesel, gasoline, electric, hybrid
    fuel_type       VARCHAR(20),
    transmission    VARCHAR(20),                      -- manual, automatic
    seating_capacity INTEGER DEFAULT 4,               -- Koltuk kapasitesi
    cargo_capacity_kg DECIMAL(8,2),                   -- Yük kapasitesi (kg)
    cargo_capacity_m3 DECIMAL(8,2),                   -- Yük hacmi (m³)
    
    -- Belge ve Ruhsat
    registration_doc VARCHAR(500),                    -- Ruhsat belgesi
    insurance_doc   VARCHAR(500),                     -- Sigorta belgesi
    insurance_expiry DATE,
    inspection_expiry DATE,                           -- Muayene bitiş
    
    -- Durum
    condition       VARCHAR(20) DEFAULT 'excellent',  -- excellent, good, fair, poor
    is_active       BOOLEAN DEFAULT TRUE,
    is_available    BOOLEAN DEFAULT TRUE,             -- Müsait mi?
    
    -- Konum (GPS)
    current_latitude  DECIMAL(10,8),
    current_longitude DECIMAL(11,8),
    last_location_update TIMESTAMP,
    
    -- Fotoğraflar
    photo_url       VARCHAR(500),
    photos          JSONB DEFAULT '[]',
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### taxi_services (Taksi Hizmetleri)
```sql
-- Taksi hizmeti veren kullanıcılar ve şirketler
CREATE TABLE taxi_services (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),        -- Taksi şoförü
    vehicle_id      UUID REFERENCES vehicle_fleet(id),
    
    -- Taksi Bilgileri
    taxi_number     VARCHAR(50),                      -- Taksi numarası
    taxi_brand      VARCHAR(100),                     -- Taksi markası (Turktaxi vb.)
    is_metered      BOOLEAN DEFAULT TRUE,             -- Taksimetreli mi?
    is_app_based    BOOLEAN DEFAULT TRUE,             -- Uygulama bazlı mı?
    
    -- Hizmet Alanı
    service_areas   JSONB DEFAULT '[]',               -- Hizmet verdiği bölgeler
    city            VARCHAR(100),
    districts       JSONB DEFAULT '[]',               -- İlçe listesi
    
    -- Çalışma Saatleri
    working_hours   JSONB DEFAULT '{}',               -- Haftalık çalışma saatleri
    is_24_7         BOOLEAN DEFAULT FALSE,
    
    -- Fiyatlandırma
    base_fare       DECIMAL(8,2),                     -- Açılış ücreti
    per_km_rate     DECIMAL(8,2),                     -- Km başı ücret
    per_minute_rate DECIMAL(8,2),                     -- Dakika başı ücret
    min_fare        DECIMAL(8,2),                     -- Minimum ücret
    currency        VARCHAR(3) DEFAULT 'TRY',
    
    -- İstatistikler
    total_trips     INTEGER DEFAULT 0,
    total_distance  DECIMAL(12,2) DEFAULT 0,          -- km cinsinden
    total_earnings  DECIMAL(14,2) DEFAULT 0,
    rating_avg      DECIMAL(3,2) DEFAULT 0,
    rating_count    INTEGER DEFAULT 0,
    
    -- Durum
    is_online       BOOLEAN DEFAULT FALSE,            -- Çevrimiçi mi?
    is_available    BOOLEAN DEFAULT TRUE,             -- Müsait mi?
    is_verified     BOOLEAN DEFAULT FALSE,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### taxi_trips (Taksi Yolculukları)
```sql
-- Taksi yolculukları
CREATE TABLE taxi_trips (
    id              UUID PRIMARY KEY,
    taxi_service_id UUID REFERENCES taxi_services(id),
    driver_id       UUID REFERENCES users(id),
    passenger_id    UUID REFERENCES users(id),
    vehicle_id      UUID REFERENCES vehicle_fleet(id),
    
    -- Yolculuk Detayları
    pickup_location TEXT,
    pickup_latitude DECIMAL(10,8),
    pickup_longitude DECIMAL(11,8),
    dropoff_location TEXT,
    dropoff_latitude DECIMAL(10,8),
    dropoff_longitude DECIMAL(11,8),
    
    -- Mesafe ve Süre
    distance_km     DECIMAL(8,2),
    duration_minutes INTEGER,
    
    -- Fiyat
    base_fare       DECIMAL(8,2),
    distance_fare   DECIMAL(8,2),
    time_fare       DECIMAL(8,2),
    total_fare      DECIMAL(8,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    payment_method  VARCHAR(50),
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'requested',  -- requested, accepted, in_progress, completed, cancelled
    requested_at    TIMESTAMP,
    accepted_at     TIMESTAMP,
    started_at      TIMESTAMP,
    completed_at    TIMESTAMP,
    
    -- İptal
    cancellation_reason TEXT,
    cancelled_by    VARCHAR(10),                      -- driver, passenger
    
    -- Değerlendirme
    driver_rating   INTEGER CHECK(driver_rating BETWEEN 1 AND 5),
    passenger_rating INTEGER CHECK(passenger_rating BETWEEN 1 AND 5),
    
    -- Konum Takibi
    route_track     JSONB DEFAULT '[]',               -- Güzergah noktaları
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### delivery_services (Kurye ve Lojistik Hizmetleri)
```sql
-- Kargo, kurye, lojistik hizmetleri
CREATE TABLE delivery_services (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),        -- Kurye/şoför
    vehicle_id      UUID REFERENCES vehicle_fleet(id),
    
    -- Hizmet Türü
    service_type    VARCHAR(30),                      -- courier, cargo, moving, freight
    
    -- Hizmet Alanı
    service_areas   JSONB DEFAULT '[]',
    city            VARCHAR(100),
    intercity       BOOLEAN DEFAULT FALSE,            -- Şehirlerarası mı?
    
    -- Kapasite
    max_weight_kg   DECIMAL(8,2),
    max_volume_m3   DECIMAL(8,2),
    max_packages    INTEGER,
    
    -- Fiyatlandırma
    base_price      DECIMAL(8,2),
    per_km_rate     DECIMAL(8,2),
    per_kg_rate     DECIMAL(8,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    
    -- Durum
    is_online       BOOLEAN DEFAULT FALSE,
    is_available    BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### cargo_orders (Kargo Siparişleri)
```sql
-- Kargo ve lojistik siparişleri
CREATE TABLE cargo_orders (
    id              UUID PRIMARY KEY,
    sender_id       UUID REFERENCES users(id),
    receiver_id     UUID REFERENCES users(id),
    delivery_service_id UUID REFERENCES delivery_services(id),
    driver_id       UUID REFERENCES users(id),
    vehicle_id      UUID REFERENCES vehicle_fleet(id),
    
    -- Kargo Bilgileri
    order_number    VARCHAR(50) UNIQUE,
    description     TEXT,
    
    -- Gönderen
    sender_name     VARCHAR(200),
    sender_phone    VARCHAR(20),
    sender_address  TEXT,
    sender_latitude DECIMAL(10,8),
    sender_longitude DECIMAL(11,8),
    
    -- Alan
    receiver_name   VARCHAR(200),
    receiver_phone  VARCHAR(20),
    receiver_address TEXT,
    receiver_latitude DECIMAL(10,8),
    receiver_longitude DECIMAL(11,8),
    
    -- Kargo Detayları
    weight_kg       DECIMAL(8,2),
    volume_m3       DECIMAL(8,2),
    package_count   INTEGER DEFAULT 1,
    content_type    VARCHAR(50),                      -- documents, fragile, electronics, food, other
    
    -- Fiyat
    base_price      DECIMAL(10,2),
    distance_price  DECIMAL(10,2),
    weight_price    DECIMAL(10,2),
    total_price     DECIMAL(10,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    payment_method  VARCHAR(50),
    
    -- Teslimat
    pickup_date     DATE,
    pickup_time     TIME,
    delivery_date   DATE,
    delivery_time   TIME,
    estimated_delivery TIMESTAMP,
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'pending',     -- pending, picked_up, in_transit, delivered, returned
    
    -- Takip
    tracking_number VARCHAR(50),
    current_location TEXT,
    current_latitude DECIMAL(10,8),
    current_longitude DECIMAL(11,8),
    
    -- Teslim
    delivered_at    TIMESTAMP,
    delivered_to    VARCHAR(200),
    proof_of_delivery VARCHAR(500),                    -- Teslimat fotoğrafı
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### vehicle_bookings (Araç Kiralama)
```sql
-- Araç kiralama hizmeti
CREATE TABLE vehicle_bookings (
    id              UUID PRIMARY KEY,
    vehicle_id      UUID REFERENCES vehicle_fleet(id),
    owner_id        UUID REFERENCES users(id),
    renter_id       UUID REFERENCES users(id),
    
    -- Kiralama Bilgileri
    start_date      TIMESTAMP NOT NULL,
    end_date        TIMESTAMP NOT NULL,
    start_location  TEXT,
    end_location    TEXT,
    
    -- Fiyat
    daily_rate      DECIMAL(10,2),
    total_days      INTEGER,
    total_price     DECIMAL(10,2),
    deposit         DECIMAL(10,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    payment_method  VARCHAR(50),
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'pending',     -- pending, confirmed, active, completed, cancelled
    
    -- Hasar
    condition_start TEXT,                              -- Başlangıç durumu
    condition_end   TEXT,                              -- Bitiş durumu
    has_damage      BOOLEAN DEFAULT FALSE,
    damage_notes    TEXT,
    damage_photos   JSONB DEFAULT '[]',
    
    -- Sözleşme
    contract_url    VARCHAR(500),
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### route_plans (Güzergah Planları)
```sql
-- Taksi ve kargo için güzergah planlama
CREATE TABLE route_plans (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),
    
    -- Güzergah
    origin          TEXT,
    origin_latitude DECIMAL(10,8),
    origin_longitude DECIMAL(11,8),
    destination     TEXT,
    destination_latitude DECIMAL(10,8),
    destination_longitude DECIMAL(11,8),
    
    -- Ara Duraklar
    waypoints       JSONB DEFAULT '[]',
    
    -- Mesafe ve Süre
    total_distance_km DECIMAL(8,2),
    estimated_duration_min INTEGER,
    
    -- Trafik
    traffic_level   VARCHAR(20),                      -- light, moderate, heavy, blocked
    alternative_routes JSONB DEFAULT '[]',
    
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### 13.1 Taksi Sistemine Özel Tablolar

Aşağıdaki tablolar taksi sistemine özeldir. Detaylı tasarım ve alan açıklamaları için → [TAXI-SYSTEM-DESIGN.md §11](./TAXI-SYSTEM-DESIGN.md#11-veritabanı-şeması-yeni-tablolar)

```sql
-- Taksi şoförü belgeleri
CREATE TABLE taxi_driver_documents (
    id                  UUID PRIMARY KEY,
    user_id             UUID REFERENCES users(id) UNIQUE,
    drivers_license_front   VARCHAR(500),
    drivers_license_back    VARCHAR(500),
    drivers_license_number  VARCHAR(50),
    drivers_license_class   VARCHAR(10),
    drivers_license_issue   DATE,
    drivers_license_expiry  DATE,
    drivers_license_status  VARCHAR(20) DEFAULT 'pending',
    psychotechnical_url     VARCHAR(500),
    psychotechnical_date    DATE,
    psychotechnical_expiry  DATE,
    psychotechnical_status  VARCHAR(20) DEFAULT 'pending',
    src_certificate_url     VARCHAR(500),
    src_certificate_number  VARCHAR(50),
    src_certificate_type    VARCHAR(20),
    src_certificate_expiry  DATE,
    src_certificate_status  VARCHAR(20) DEFAULT 'pending',
    criminal_record_url     VARCHAR(500),
    criminal_record_date    DATE,
    criminal_record_expiry  DATE,
    criminal_record_status  VARCHAR(20) DEFAULT 'pending',
    residence_doc_url       VARCHAR(500),
    residence_address       TEXT,
    residence_status        VARCHAR(20) DEFAULT 'pending',
    tax_certificate_url     VARCHAR(500),
    tax_office              VARCHAR(200),
    tax_number              VARCHAR(50),
    tax_status              VARCHAR(20) DEFAULT 'pending',
    verification_status     VARCHAR(20) DEFAULT 'pending',
    verification_note       TEXT,
    verified_by             UUID REFERENCES users(id),
    verified_at             TIMESTAMP,
    created_at              TIMESTAMP DEFAULT NOW(),
    updated_at              TIMESTAMP DEFAULT NOW()
);

-- Ticari araç / taksi plakası
CREATE TABLE taxi_vehicles (
    id                  UUID PRIMARY KEY,
    ownership_type      VARCHAR(30) NOT NULL,
    plate_number        VARCHAR(20) UNIQUE NOT NULL,
    plate_city          VARCHAR(50),
    plate_type          VARCHAR(30) DEFAULT 'taxi',
    brand               VARCHAR(100) NOT NULL,
    model               VARCHAR(200) NOT NULL,
    year                INTEGER NOT NULL,
    color               VARCHAR(50),
    engine_type         VARCHAR(20),
    transmission        VARCHAR(20),
    seating_capacity    INTEGER DEFAULT 4,
    registration_doc    VARCHAR(500),
    registration_number VARCHAR(100),
    insurance_url       VARCHAR(500),
    insurance_type      VARCHAR(50),
    insurance_start     DATE,
    insurance_expiry    DATE,
    insurance_status    VARCHAR(20) DEFAULT 'pending',
    inspection_url      VARCHAR(500),
    inspection_date     DATE,
    inspection_expiry   DATE,
    inspection_status   VARCHAR(20) DEFAULT 'pending',
    taximeter_model     VARCHAR(100),
    taximeter_calibration_date DATE,
    taximeter_calibration_expiry DATE,
    obd_device_id       VARCHAR(100),
    obd_last_ping       TIMESTAMP,
    obd_status          VARCHAR(20) DEFAULT 'offline',
    -- Muayene OCR
    inspection_ocr_data       JSONB,                       -- OCR çıktısı
    inspection_last_checked   TIMESTAMP,                   -- Son kontrol
    inspection_warning_sent   INTEGER DEFAULT 0,           -- Kaç uyarı gönderildi
    -- Güvenlik Kamerası
    has_security_camera BOOLEAN DEFAULT FALSE,       -- İç güvenlik kamerası var mı?
    security_camera_verified_at TIMESTAMP,            -- Son doğrulama tarihi
    camera_warning_sent  BOOLEAN DEFAULT FALSE,       -- Uyarı gönderildi mi?
    photo_url           VARCHAR(500),
    photos              JSONB DEFAULT '[]',
    is_active           BOOLEAN DEFAULT TRUE,
    is_available        BOOLEAN DEFAULT TRUE,
    status              VARCHAR(20) DEFAULT 'active',
    rating_avg          DECIMAL(3,2) DEFAULT 0,
    rating_count        INTEGER DEFAULT 0,
    total_trips         INTEGER DEFAULT 0,
    total_distance_km   DECIMAL(12,2) DEFAULT 0,
    total_earnings      DECIMAL(14,2) DEFAULT 0,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

-- Araç sahipleri ve hisse oranları
CREATE TABLE taxi_vehicle_owners (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    user_id             UUID REFERENCES users(id),
    company_id          UUID REFERENCES company_profiles(id) NULL,
    ownership_percent   DECIMAL(5,2) NOT NULL,
    ownership_type      VARCHAR(30),
    is_primary_owner    BOOLEAN DEFAULT FALSE,
    role                VARCHAR(30) DEFAULT 'owner',
    agreement_url       VARCHAR(500),
    agreement_start     DATE,
    agreement_end       DATE,
    is_active           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW(),
    UNIQUE(vehicle_id, user_id)
);

-- Araç-şoför vardiya atamaları
CREATE TABLE taxi_driver_assignments (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    driver_id           UUID REFERENCES users(id),
    assigner_id         UUID REFERENCES users(id),
    shift_type          VARCHAR(30) NOT NULL,
    shift_start         TIME NOT NULL,
    shift_end           TIME NOT NULL,
    shift_days          JSONB NOT NULL,
    assignment_type     VARCHAR(30) NOT NULL,
    rental_agreement_id UUID REFERENCES taxi_rental_agreements(id) NULL,
    is_active           BOOLEAN DEFAULT TRUE,
    is_current_driver   BOOLEAN DEFAULT FALSE,
    effective_from      DATE NOT NULL,
    effective_until     DATE,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW(),
    UNIQUE(vehicle_id, driver_id, shift_type, shift_start)
);

-- Araç kiralama sözleşmeleri
CREATE TABLE taxi_rental_agreements (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    lessor_id           UUID REFERENCES users(id),
    lessee_id           UUID REFERENCES users(id),
    rental_type         VARCHAR(30) NOT NULL,
    rental_amount       DECIMAL(10,2) NOT NULL,
    rental_currency     VARCHAR(3) DEFAULT 'TRY',
    payment_frequency   VARCHAR(20) DEFAULT 'daily',
    payment_method      VARCHAR(30) DEFAULT 'auto_deduct',
    km_limit            DECIMAL(10,2) NULL,
    km_overage_rate     DECIMAL(8,2) NULL,
    service_area        JSONB DEFAULT '[]',
    work_hours_start    TIME,
    work_hours_end      TIME,
    deposit_amount      DECIMAL(10,2) DEFAULT 0,
    deposit_paid        BOOLEAN DEFAULT FALSE,
    contract_url        VARCHAR(500),
    contract_start      DATE NOT NULL,
    contract_end        DATE,
    auto_renew          BOOLEAN DEFAULT TRUE,
    status              VARCHAR(20) DEFAULT 'active',
    total_paid          DECIMAL(14,2) DEFAULT 0,
    last_payment_date   DATE,
    next_payment_date   DATE,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

-- Şoförün anlık durumu
CREATE TABLE taxi_driver_status (
    id                  UUID PRIMARY KEY,
    user_id             UUID REFERENCES users(id) UNIQUE,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    status              VARCHAR(30) NOT NULL DEFAULT 'offline',
    is_available        BOOLEAN DEFAULT FALSE,
    is_online           BOOLEAN DEFAULT FALSE,
    current_latitude    DECIMAL(10,8),
    current_longitude   DECIMAL(11,8),
    location_updated_at TIMESTAMP,
    current_trip_id     UUID REFERENCES taxi_trips(id) NULL,
    trip_started_at     TIMESTAMP,
    current_shift_id    UUID REFERENCES taxi_driver_assignments(id) NULL,
    shift_started_at    TIMESTAMP,
    shift_end_at        TIMESTAMP,
    today_trips         INTEGER DEFAULT 0,
    today_earnings      DECIMAL(12,2) DEFAULT 0,
    today_distance_km   DECIMAL(10,2) DEFAULT 0,
    app_version         VARCHAR(20),
    device_type         VARCHAR(20),
    battery_level       INTEGER,
    auto_accept         BOOLEAN DEFAULT FALSE,
    max_accept_distance INTEGER DEFAULT 5,
    auto_assign_mode    VARCHAR(20) DEFAULT 'suggest', -- off, auto_accept, suggest, return_station
    last_trip_ended_at  TIMESTAMP,
    reject_count_today  INTEGER DEFAULT 0,
    last_reject_at      TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT NOW()
);

-- Çağrı logları
CREATE TABLE taxi_ride_requests (
    id                  UUID PRIMARY KEY,
    passenger_id        UUID REFERENCES users(id),
    pickup_latitude     DECIMAL(10,8) NOT NULL,
    pickup_longitude    DECIMAL(11,8) NOT NULL,
    pickup_address      TEXT,
    dropoff_latitude    DECIMAL(10,8) NOT NULL,
    dropoff_longitude   DECIMAL(11,8) NOT NULL,
    dropoff_address     TEXT,
    estimated_distance  DECIMAL(8,2),
    estimated_duration  INTEGER,
    estimated_fare_min  DECIMAL(10,2),
    estimated_fare_max  DECIMAL(10,2),
    comfort_preference  VARCHAR(30),                  -- Any, Good, Premium, VIP
    driver_gender_pref  VARCHAR(10),                  -- any, male, female
    vehicle_brand_pref  VARCHAR(100),                 -- opsiyonel marka filtresi
    vehicle_fuel_pref   VARCHAR(20),                  -- any, gasoline, diesel, lpg, electric, hybrid
    route_polyline      TEXT,
    route_instructions  JSONB DEFAULT '[]',
    notified_drivers    JSONB DEFAULT '[]',
    accepted_driver_id  UUID REFERENCES users(id) NULL,
    accepted_at         TIMESTAMP,
    response_time_seconds INTEGER,
    status              VARCHAR(30) DEFAULT 'pending',
    cancel_reason       TEXT,
    cancelled_by        VARCHAR(20),
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

-- Yolculuk
CREATE TABLE taxi_trips (
    id                  UUID PRIMARY KEY,
    request_id          UUID REFERENCES taxi_ride_requests(id),
    passenger_id        UUID REFERENCES users(id),
    driver_id           UUID REFERENCES users(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    pickup_latitude     DECIMAL(10,8),
    pickup_longitude    DECIMAL(11,8),
    pickup_address      TEXT,
    dropoff_latitude    DECIMAL(10,8),
    dropoff_longitude   DECIMAL(11,8),
    dropoff_address     TEXT,
    distance_km         DECIMAL(8,2),
    duration_minutes    INTEGER,
    route_taken         JSONB DEFAULT '[]',
    base_fare           DECIMAL(8,2) DEFAULT 0,
    distance_fare       DECIMAL(8,2) DEFAULT 0,
    time_fare           DECIMAL(8,2) DEFAULT 0,
    surge_multiplier    DECIMAL(3,2) DEFAULT 1.00,
    surge_amount        DECIMAL(8,2) DEFAULT 0,
    extra_fees          JSONB DEFAULT '{}',
    total_fare          DECIMAL(10,2),
    currency            VARCHAR(3) DEFAULT 'TRY',
    payment_method      VARCHAR(50),
    payment_status      VARCHAR(20) DEFAULT 'pending',
    payment_gateway_ref VARCHAR(255),
    payment_held_fare   DECIMAL(10,2),
    commission_rate     DECIMAL(5,2) DEFAULT 5.00,
    commission_amount   DECIMAL(10,2),
    driver_earning      DECIMAL(10,2),
    rental_cost         DECIMAL(10,2) DEFAULT 0,
    requested_at        TIMESTAMP,
    accepted_at         TIMESTAMP,
    driver_arrived_at   TIMESTAMP,
    started_at          TIMESTAMP,
    completed_at        TIMESTAMP,
    status              VARCHAR(30) DEFAULT 'requested',
    cancellation_reason TEXT,
    cancelled_by        VARCHAR(20),
    driver_rated        BOOLEAN DEFAULT FALSE,
    vehicle_rated       BOOLEAN DEFAULT FALSE,
    driver_rating       INTEGER CHECK(driver_rating BETWEEN 1 AND 5),
    vehicle_rating      INTEGER CHECK(vehicle_rating BETWEEN 1 AND 5),
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

-- Çift yönlü puanlama (şoför + araç)
CREATE TABLE taxi_ratings (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id),
    reviewer_id         UUID REFERENCES users(id),
    driver_id           UUID REFERENCES users(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    driving_quality     INTEGER CHECK(driving_quality BETWEEN 1 AND 5),
    punctuality         INTEGER CHECK(punctuality BETWEEN 1 AND 5),
    communication       INTEGER CHECK(communication BETWEEN 1 AND 5),
    safe_driving        INTEGER CHECK(safe_driving BETWEEN 1 AND 5),
    route_knowledge     INTEGER CHECK(route_knowledge BETWEEN 1 AND 5),
    helpfulness         INTEGER CHECK(helpfulness BETWEEN 1 AND 5),
    driver_avg          DECIMAL(3,2),
    vehicle_cleanliness     INTEGER CHECK(vehicle_cleanliness BETWEEN 1 AND 5),
    vehicle_smell           INTEGER CHECK(vehicle_smell BETWEEN 1 AND 5),
    vehicle_comfort         INTEGER CHECK(vehicle_comfort BETWEEN 1 AND 5),
    vehicle_ac              INTEGER CHECK(vehicle_ac BETWEEN 1 AND 5),
    vehicle_condition       INTEGER CHECK(vehicle_condition BETWEEN 1 AND 5),
    vehicle_avg         DECIMAL(3,2),
    combined_score      DECIMAL(3,2),
    comment             TEXT,
    driver_response     TEXT,
    response_date       TIMESTAMP,
    photos              JSONB DEFAULT '[]',
    is_visible          BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT NOW(),
    UNIQUE(trip_id, reviewer_id)
);

-- Kullanıcı cüzdanı
CREATE TABLE user_wallets (
    id                  UUID PRIMARY KEY,
    user_id             UUID REFERENCES users(id) UNIQUE,
    balance             DECIMAL(14,2) DEFAULT 0,
    blocked_balance     DECIMAL(14,2) DEFAULT 0,
    default_payment     VARCHAR(30) DEFAULT 'wallet',
    saved_cards         JSONB DEFAULT '[]',
    daily_limit         DECIMAL(14,2) DEFAULT 1000,
    monthly_limit       DECIMAL(14,2) DEFAULT 10000,
    current_daily_spent DECIMAL(14,2) DEFAULT 0,
    current_monthly_spent DECIMAL(14,2) DEFAULT 0,
    is_active           BOOLEAN DEFAULT TRUE,
    is_frozen           BOOLEAN DEFAULT FALSE,
    frozen_reason       TEXT,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

-- Cüzdan hareketleri
CREATE TABLE wallet_transactions (
    id                  UUID PRIMARY KEY,
    wallet_id           UUID REFERENCES user_wallets(id),
    user_id             UUID REFERENCES users(id),
    transaction_type    VARCHAR(30) NOT NULL,
    related_trip_id     UUID REFERENCES taxi_trips(id) NULL,
    amount              DECIMAL(14,2) NOT NULL,
    fee                 DECIMAL(10,2) DEFAULT 0,
    net_amount          DECIMAL(14,2),
    currency            VARCHAR(3) DEFAULT 'TRY',
    balance_before      DECIMAL(14,2),
    balance_after       DECIMAL(14,2),
    payment_method      VARCHAR(50),
    gateway_reference   VARCHAR(255),
    status              VARCHAR(20) DEFAULT 'pending',
    description         TEXT,
    created_at          TIMESTAMP DEFAULT NOW()
);

-- Çağrı red logları (ceza puanı için)
CREATE TABLE call_rejection_log (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES users(id),
    request_id          UUID REFERENCES taxi_ride_requests(id),
    rejection_type      VARCHAR(30),
    rejection_reason    TEXT,
    calculated_distance DECIMAL(8,2),
    estimated_fare      DECIMAL(10,2),
    is_penalty          BOOLEAN DEFAULT TRUE,
    penalty_points      INTEGER DEFAULT 0,
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### taxi_qr_log (QR Kod Okutma Logları)
```sql
CREATE TABLE taxi_qr_log (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    trip_id             UUID REFERENCES taxi_trips(id),
    customer_id         UUID REFERENCES users(id),
    
    scan_location       VARCHAR(30) NOT NULL,         -- right_door, left_door, interior
    scan_result         BOOLEAN NOT NULL,             -- başarılı mı?
    ip_address          VARCHAR(45),
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_qr_log_vehicle ON taxi_qr_log(vehicle_id);
```

### taxi_planned_routes (Planlanmış Rotalar)
```sql
CREATE TABLE taxi_planned_routes (
    id                  UUID PRIMARY KEY,
    customer_id         UUID NOT NULL REFERENCES users(id),
    plan_date           DATE NOT NULL,
    route_date          DATE NOT NULL,
    status              VARCHAR(20) DEFAULT 'pending',
    
    total_legs          INTEGER NOT NULL CHECK(total_legs BETWEEN 1 AND 5),
    total_fee           DECIMAL(10,2) NOT NULL,
    blocked_fee         DECIMAL(10,2) NOT NULL,
    collected_fee       DECIMAL(10,2),
    
    cancellation_time   TIMESTAMP,
    cancel_reason       VARCHAR(200),
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_planned_routes_customer ON taxi_planned_routes(customer_id);
CREATE INDEX idx_planned_routes_date ON taxi_planned_routes(route_date);

### taxi_route_legs (Rota Bacakları)
```sql
CREATE TABLE taxi_route_legs (
    id                  UUID PRIMARY KEY,
    route_id            UUID NOT NULL REFERENCES taxi_planned_routes(id) ON DELETE CASCADE,
    leg_order           INTEGER NOT NULL CHECK(leg_order BETWEEN 1 AND 5),
    
    pickup_address      TEXT NOT NULL,
    pickup_lat          DECIMAL(10,7),
    pickup_lng          DECIMAL(10,7),
    dropoff_address     TEXT NOT NULL,
    dropoff_lat         DECIMAL(10,7),
    dropoff_lng         DECIMAL(10,7),
    
    scheduled_time      TIMESTAMP NOT NULL,
    actual_start_time   TIMESTAMP,
    actual_end_time     TIMESTAMP,
    
    estimated_distance  DECIMAL(8,2),
    estimated_fee       DECIMAL(10,2),
    actual_distance     DECIMAL(8,2),
    actual_fee          DECIMAL(10,2),
    
    trip_id             UUID REFERENCES taxi_trips(id),
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    leg_status          VARCHAR(20) DEFAULT 'pending',
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_route_legs_route ON taxi_route_legs(route_id);
```

### taxi_waiting_spots (Bekleme Noktaları)
```sql
CREATE TABLE taxi_waiting_spots (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    latitude            DECIMAL(10,7) NOT NULL,
    longitude           DECIMAL(11,7) NOT NULL,
    label               VARCHAR(100),
    
    duration_minutes    INTEGER DEFAULT 30,
    started_at          TIMESTAMP DEFAULT NOW(),
    expires_at          TIMESTAMP,
    auto_cleared        BOOLEAN DEFAULT FALSE,
    
    status              VARCHAR(20) DEFAULT 'active',
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_waiting_spots_active ON taxi_waiting_spots(status, expires_at);
CREATE INDEX idx_waiting_spots_location ON taxi_waiting_spots(latitude, longitude);
```

### taxi_inspection_log (Muayene Otomatik Kontrol Logları)
```sql
CREATE TABLE taxi_inspection_log (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    action              VARCHAR(30) NOT NULL,      -- ocr_read, warning_30d, warning_7d, auto_disabled, renewed
    old_expiry          DATE,
    new_expiry          DATE,
    ocr_confidence      DECIMAL(5,2),              -- OCR güven oranı %0-100
    is_auto             BOOLEAN DEFAULT TRUE,      -- Otomatik mi, manuel mi?
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_inspection_log_vehicle ON taxi_inspection_log(vehicle_id);
```

### taxi_arrival_bookings (Geliş Öncesi Karşılama Rezervasyonu)
```sql
CREATE TABLE taxi_arrival_bookings (
    id                  UUID PRIMARY KEY,
    customer_id         UUID NOT NULL REFERENCES users(id),
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    departure_city      VARCHAR(100) NOT NULL,
    arrival_city        VARCHAR(100) NOT NULL,
    arrival_point       TEXT NOT NULL,
    arrival_point_lat   DECIMAL(10,7),
    arrival_point_lng   DECIMAL(11,7),
    destination_address TEXT,
    destination_lat     DECIMAL(10,7),
    destination_lng     DECIMAL(11,7),
    
    transport_type      VARCHAR(20) NOT NULL,
    transport_code      VARCHAR(30),
    
    estimated_arrival   TIMESTAMP NOT NULL,
    actual_arrival      TIMESTAMP,
    driver_arrival      TIMESTAMP,
    waiting_started_at  TIMESTAMP,
    waiting_ended_at    TIMESTAMP,
    
    trip_fee            DECIMAL(10,2),
    waiting_fee_rate    DECIMAL(10,2),
    waiting_minutes     INTEGER DEFAULT 0,
    total_waiting_fee   DECIMAL(10,2),
    total_fee           DECIMAL(10,2),
    
    status              VARCHAR(30) DEFAULT 'pending',
    cancel_reason       VARCHAR(200),
    cancelled_by        VARCHAR(20),
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_arrival_bookings_customer ON taxi_arrival_bookings(customer_id);
CREATE INDEX idx_arrival_bookings_status ON taxi_arrival_bookings(status);
CREATE INDEX idx_arrival_bookings_arrival ON taxi_arrival_bookings(estimated_arrival);
```

---

## 14. GIDA VE RESTORAN SİSTEMİ

### restaurants (Restoran ve Dükkanlar)
```sql
-- Restoran, kafe, fast-food, büfe, dürümcü vb.
CREATE TABLE restaurants (
    id              UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(id),        -- İşletme sahibi
    company_id      UUID REFERENCES company_profiles(id) NULL,
    store_id        UUID REFERENCES stores(id) NULL,
    
    -- İşletme Bilgileri
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    cuisine_type    VARCHAR(50),                      -- turkish, fastfood, pizza, kebab, burger, healthy
    
    -- Logo ve Görseller
    logo_url        VARCHAR(500),
    cover_url       VARCHAR(500),
    
    -- Konum
    address         TEXT,
    city            VARCHAR(100),
    district        VARCHAR(100),
    neighborhood    VARCHAR(100),
    latitude        DECIMAL(10,8),
    longitude       DECIMAL(11,8),
    
    -- İletişim
    phone           VARCHAR(20),
    whatsapp        VARCHAR(20),
    
    -- Çalışma Saatleri
    working_hours   JSONB DEFAULT '{}',
    is_24_7         BOOLEAN DEFAULT FALSE,
    
    -- Teslimat
    has_delivery    BOOLEAN DEFAULT TRUE,
    has_takeaway    BOOLEAN DEFAULT TRUE,
    has_dine_in     BOOLEAN DEFAULT TRUE,
    min_order_amount DECIMAL(8,2),                    -- Minimum sipariş tutarı
    delivery_fee    DECIMAL(8,2),
    delivery_radius INTEGER DEFAULT 5,                -- Teslimat yarıçapı (km)
    estimated_delivery_min INTEGER DEFAULT 30,        -- Tahmini teslimat süresi
    
    -- Durum
    is_open         BOOLEAN DEFAULT TRUE,
    is_active       BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE,
    
    -- İstatistikler
    rating_avg      DECIMAL(3,2) DEFAULT 0,
    rating_count    INTEGER DEFAULT 0,
    total_orders    INTEGER DEFAULT 0,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### restaurant_menu (Menü)
```sql
-- Restoran menüsü
CREATE TABLE restaurant_menu (
    id              UUID PRIMARY KEY,
    restaurant_id   UUID REFERENCES restaurants(id),
    parent_id       UUID REFERENCES restaurant_menu(id), -- Alt kategoriler için
    
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    icon            VARCHAR(100),
    sort_order      INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    
    created_at      TIMESTAMP DEFAULT NOW()
);

-- MENÜ KATEGORİLERİ (Dürümcü Örneği):
-- 1. Dürüm Çeşitleri
--    - Tavuk Dürüm
--    - Et Dürüm
--    - Kokoreç
--    - Tantuni
--    - Şiş Tavuk
--    - Adana Dürüm
--    - Urfa Dürüm
--    - Döner Dürüm
-- 2. Porsiyonlar
--    - Porsiyon Tavuk
--    - Porsiyon Et
-- 3. Yan Ürünler
--    - Patates Kızartması
--    - Soğan Halkası
--    - Cola
--    - Ayran
--    - Su
-- 4. Special
--    - Özel Sos
--    - Ekstra Peynir
--    - Acı Sos
```

### menu_items (Menü Ürünleri)
```sql
-- Menüdeki ürünler
CREATE TABLE menu_items (
    id              UUID PRIMARY KEY,
    menu_id         UUID REFERENCES restaurant_menu(id),
    restaurant_id   UUID REFERENCES restaurants(id),
    
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    
    -- Fiyat
    price           DECIMAL(10,2) NOT NULL,
    compare_price   DECIMAL(10,2),                    -- İndirimli fiyat
    currency        VARCHAR(3) DEFAULT 'TRY',
    
    -- Malzemeler
    ingredients     JSONB DEFAULT '[]',
    allergens       JSONB DEFAULT '[]',               -- Alerjenler
    is_vegetarian   BOOLEAN DEFAULT FALSE,
    is_vegan        BOOLEAN DEFAULT FALSE,
    is_gluten_free  BOOLEAN DEFAULT FALSE,
    is_spicy        BOOLEAN DEFAULT FALSE,
    spice_level     INTEGER DEFAULT 0,                -- 0-5 arası
    
    -- Porsiyon
    portion_size    VARCHAR(50),                      -- normal, large, small, custom
    calories        INTEGER,
    
    -- Görsel
    image_url       VARCHAR(500),
    
    -- Hazırlık
    preparation_time INTEGER DEFAULT 15,              -- Hazırlık süresi (dakika)
    
    -- Durum
    is_available    BOOLEAN DEFAULT TRUE,
    is_active       BOOLEAN DEFAULT TRUE,
    is_featured     BOOLEAN DEFAULT FALSE,
    
    -- Sipariş İstatistikleri
    order_count     INTEGER DEFAULT 0,
    
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### menu_item_extras (Menü Ürünü Ek Seçenekleri)
```sql
-- Menü ürünlerine eklenen malzemeler
CREATE TABLE menu_item_extras (
    id              UUID PRIMARY KEY,
    menu_item_id    UUID REFERENCES menu_items(id),
    
    name            VARCHAR(255) NOT NULL,
    price           DECIMAL(8,2) DEFAULT 0,
    is_default      BOOLEAN DEFAULT FALSE,
    is_available    BOOLEAN DEFAULT TRUE,
    
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- DÜRÜM ÖRNEĞİ:
-- Tavuk Dürüm → Ek Seçenekler:
--   + Peynir (+5₺)
--   + Acı Sos (+0₺)
--   + Soğan (+0₺)
--   + Domates (+0₺)
--   + Marul (+0₺)
--   + Turşu (+2₺)
--   + Ekstra Tavuk (+15₺)
```

### food_orders (Gıda Siparişleri)
```sql
-- Restoran siparişleri
CREATE TABLE food_orders (
    id              UUID PRIMARY KEY,
    restaurant_id   UUID REFERENCES restaurants(id),
    customer_id     UUID REFERENCES users(id),
    
    -- Sipariş Numarası
    order_number    VARCHAR(50) UNIQUE,
    
    -- Teslimat Türü
    order_type      VARCHAR(20) NOT NULL,             -- delivery, takeaway, dine_in
    
    -- Teslimat Adresi (delivery için)
    delivery_address TEXT,
    delivery_latitude DECIMAL(10,8),
    delivery_longitude DECIMAL(11,8),
    delivery_notes  TEXT,
    
    -- Zaman
    requested_time  TIMESTAMP,                        -- İstenen zaman
    estimated_time  TIMESTAMP,                        -- Tahmini süre
    actual_time     TIMESTAMP,                        -- Gerçek süre
    
    -- Fiyat
    subtotal        DECIMAL(10,2),                    -- Ara toplam
    delivery_fee    DECIMAL(8,2) DEFAULT 0,
    service_fee     DECIMAL(8,2) DEFAULT 0,
    discount        DECIMAL(8,2) DEFAULT 0,
    total_price     DECIMAL(10,2),
    currency        VARCHAR(3) DEFAULT 'TRY',
    
    -- Ödeme
    payment_method  VARCHAR(50),
    payment_status  VARCHAR(20) DEFAULT 'pending',    -- pending, paid, refunded
    
    -- Durum
    status          VARCHAR(20) DEFAULT 'pending',    -- pending, confirmed, preparing, ready, delivering, delivered, completed, cancelled
    cancellation_reason TEXT,
    
    -- Kurye
    driver_id       UUID REFERENCES users(id),
    assigned_at     TIMESTAMP,
    picked_up_at    TIMESTAMP,
    delivered_at    TIMESTAMP,
    
    -- Değerlendirme
    rating          INTEGER CHECK(rating BETWEEN 1 AND 5),
    review          TEXT,
    
    -- Notlar
    customer_notes  TEXT,
    restaurant_notes TEXT,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### food_order_items (Sipariş Kalemleri)
```sql
-- Sipariş kalemleri
CREATE TABLE food_order_items (
    id              UUID PRIMARY KEY,
    order_id        UUID REFERENCES food_orders(id),
    menu_item_id    UUID REFERENCES menu_items(id),
    
    -- Ürün
    item_name       VARCHAR(255),
    quantity        INTEGER DEFAULT 1,
    unit_price      DECIMAL(10,2),
    total_price     DECIMAL(10,2),
    
    -- Ek Seçenekler
    extras          JSONB DEFAULT '[]',               -- [{name: "Peynir", price: 5}, ...]
    
    -- Notlar
    special_request TEXT,                             -- Özel istekler
    
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### food_order_tracking (Sipariş Takibi)
```sql
-- Sipariş takip logları
CREATE TABLE food_order_tracking (
    id              UUID PRIMARY KEY,
    order_id        UUID REFERENCES food_orders(id),
    
    status          VARCHAR(30),                      -- pending, confirmed, preparing, ready, picked_up, delivered
    note            TEXT,
    location        TEXT,
    latitude        DECIMAL(10,8),
    longitude       DECIMAL(11,8),
    
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 15. EN ÖNEMLİ NOKTA: HERKES HEM ALICI HEM SATICI

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   🔑 SİSTEMİN EN ÖNEMLİ ÖZELLİĞİ                               │
│                                                                 │
│   HER KİŞI AYNI ANDA:                                          │
│                                                                 │
│   1. HİZMET VEREN OLABİLİR                                     │
│      ├── Taksi şoförü → Taksicilik yapar                        │
│      ├── Dürümcü → Dürüm satar                                  │
│      ├── Alçı ustası → Alçı işi yapar                           │
│      ├── Çiftçi → Ürün yetiştirir ve satar                       │
│      └── Telefoncu → Telefon satar                               │
│                                                                 │
│   2. HİZMET ALAN OLABİLİR                                      │
│      ├── Taksi şoförü → Marketten ekmek sipariş eder            │
│      ├── Dürümcü → Tamirci çağırır                               │
│      ├── Alçı ustası → Taksicilik kullanır                       │
│      ├── Çiftçi → Gübre sipariş eder                            │
│      └── Telefoncu → Kargo gönderir                              │
│                                                                 │
│   3. ÜRÜN SATABİLİR                                            │
│      ├── Kendi ürettiği ürünleri                                 │
│      ├── Başkasının ürünlerini (onaylı)                         │
│      └── İkinci el ürünlerini                                    │
│                                                                 │
│   4. HİZMET ALABİLİR                                           │
│      ├── Yakın çevresinden usta bulur                           │
│      ├── Restorandan yemek sipariş eder                         │
│      ├── Taksi çağırır                                           │
│      ├── Kargo gönderir                                          │
│      └── Her türlü hizmeti alır                                  │
│                                                                 │
│   SONUÇ: HERKES HER ŞEYİ YAPABİLİR!                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Örnek Senaryolar:

**Senaryo 1: Taksi Şoförü**
```
Taksi şoförü Ahmet:
├── 🚕 HİZMET VERİR: Taksiyle yolcu taşır
├── 🍔 HİZMET ALIR: Dürümcüden dürüm sipariş eder
├── 🔧 HİZMET ALIR: Tamirci çağırır (araba tamiri)
├── 🛒 ÜRÜN ALIR: Marketten su sigara alır
└── 📱 HİZMET ALIR: Telefondan taksi çağırır (başka taksi)
```

**Senaryo 2: Dürümcü**
```
Dürümcü Mehmet:
├── 🌯 HİZMET VERİR: Dürüm satar
├── 🚕 HİZMET ALIR: Malzeme için taksi kullanır
├── 🔧 HİZMET ALIR: Dükkan tamiri için usta çağırır
├── 📦 HİZMET ALIR: Kargo ile malzeme getirtir
└── 🛒 ÜRÜN ALIR: Toptancıdan malzeme satın alır
```

**Senaryo 3: Alçı Ustası**
```
Alçı ustası Ali:
├── 🧱 HİZMET VERİR: Alçı işi yapar
├── 🚕 HİZMET ALIR: İş yerine taksiyle gider
├── 🍔 HİZMET ALIR: Yemek sipariş eder
├── 🛒 ÜRÜN ALIR: Marketten malzeme satın alır
├── 📦 HİZMET ALIR: Malzeme için kargo çağırır
└── 💻 HİZMET ALIR: Telefon tamiri yaptırır
```

**Senaryo 4: Çiftçi**
```
Çiftçi Fatma:
├── 🌾 HİZMET VERİR: Ürün yetiştirir ve satar
├── 🚜 HİZMET ALIR: Traktör tamiri yaptırır
├── 💊 HİZMET ALIR: İlaç sipariş eder
├── 🚕 HİZMET ALIR: Pazarına taksiyle gider
└── 📦 HİZMET ALIR: Ürünlerini kargoyla gönderir
```

**Senaryo 5: Telefoncu**
```
Telefoncu Zeynep:
├── 📱 HİZMET VERİR: Telefon satar (sıfır/ikinci el)
├── 🔧 HİZMET VERİR: Telefon tamir eder
├── 🚕 HİZMET ALIR: Müşteriye telefon götürür
├── 📦 HİZMET ALIR: Yeni telefon sipariş eder
├── 🍔 HİZMET ALIR: Yemek sipariş eder
└── 💇 HİZMET ALIR: Berbere gider
```

---

## SİSTEMİN TEMEL İLKESİ

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   "HERKES HER ŞEYİ YAPABİLİR"                                  │
│                                                                 │
│   Bu platformda:                                               │
│                                                                 │
│   ✅ Herkes hesap açabilir (ücretsiz)                           │
│   ✅ Herkes ürün satabilir (kendi veya başkasının)             │
│   ✅ Herkes hizmet verebilir                                    │
│   ✅ Herkes hizmet alabilir                                     │
│   ✅ Herkes restorandan sipariş verebilir                       │
│   ✅ Herkes taksi çağırabilir                                   │
│   ✅ Herkes kargo gönderebilir                                  │
│   ✅ Herkes usta bulabilir                                      │
│                                                                 │
│   SINIR YOKTUR!                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## YENİ İLİŞKİLER

```
┌──────────────┐
│    users     │
└──────┬───────┘
       │
       ├── seller_profiles (1:1) ← Satıcı profili
       │
       ├── listings (1:N) ← İlan sayfaları
       │   └── listing_products (1:N)
       │
       ├── products (1:N) ← Kendi ürünleri
       │
       ├── product_authorizations (1:N) ← Satış yetkileri (ürün sahibi olarak)
       │
       ├── authorization_requests (1:N) ← Yetki istekleri (satıcı olarak)
       │
       └── authorized_sales (1:N) ← Tamamlanmış satışlar
```

---

## İŞ AKIŞI

### 1. Kendi Ürününü Satma
```
Kullanıcı → Ürün Ekle → İlan Oluştur → Satışa Sun
```

### 2. Başkasının Ürününü Satma (Komisyonlu)
```
Satıcı → Ürün Bul → Yetki İste
     ↓
Ürün Sahibi → İsteği Gör → Onayla/Reddet
     ↓
Onaylanırsa → "Onaylı Satış" Rozeti → Satış Yapılabilir
     ↓
Satış → Komisyon Hesapla → Ödeme Böl
```

### 3. Komisyon Dağılımı
```
Satış Fiyatı: 1000₺
Platform Komisyonu: %1 → 10₺
Satıcı Komisyonu: %5 → 50₺
Ürün Sahibine Kalan: 940₺
```

---

## ÖRNEK SENARYO

### Gayrimenkul Uzmanı
1. Emlakçı "Ahmet" kendi ilan sayfasını oluşturur
2. "Mehmet" adlı müşterinin evini satmak ister
3. Mehmet'in evini products tablosuna ekler
4. Mehmet'e yetki isteği gönderir
5. Mehmet onay verir → "Onaylı Satış" rozeti
6. Ahmet evi ilan sayfasında yayınlar
7. Satış gerçekleşir → Komisyon paylaşılır

### İkinci El Araç Satıcısı
1. Oto galericisi kendi ilan sayfasını açar
2. Müşterilerin araçlarını satar
3. Her araç için araç sahibinden yetki ister
4. Onaylanan araçlar "Onaylı Satış" rozetiyle görünür
5. Satış完成后 komisyon paylaşılır

---

## İlişki Diyagramı

```
┌──────────────┐
│    users     │
└──────┬───────┘
       │
       ├── user_profiles (1:1)
       ├── accounts (1:N)
       │   └── account_types
       │
       ├── educations (1:N)
       ├── careers (1:N)
       │   └── career_references (1:N)
       ├── contact_information (1:1)
       ├── projects (1:N)
       │   └── project_media (1:N)
       ├── training_given (1:N)
       ├── social_accounts (1:N)
       ├── social_connections (N:N)
       ├── assets (1:N)
       ├── advisors (1:N)
       ├── interests (1:N)
       ├── banking_information (1:N)
       ├── tax_information (1:N)
       ├── certified_documents (1:N)
       │
       ├── products (1:N) ← Bireysel veya Mağaza
       │   ├── product_media (1:N)
       │   ├── digital_products (1:1)
       │   │   └── product_chapters (1:N)
       │   └── reviews (1:N)
       │
       ├── services (1:N) ← Bireysel
       │   └── service_media (1:N)
       │
       ├── stores (1:N) ← Kurumsal veya Bireysel
       │
       ├── company_profiles (1:1) ← Kurumsal
       │   ├── employees (1:N)
       │   │   └── employee_permissions (1:N)
       │   └── financial_reports (1:N)
       │
       ├── public_announcements (1:N) ← Kamusal
       ├── bulk_notifications (1:N) ← Kamusal
       │
       ├── orders (1:N) ← Satın Alma
       │   └── order_items (1:N)
       ├── transactions (1:N)
       │
       ├── follows (N:N)
       ├── likes (1:N)
       ├── comments (1:N)
       ├── notifications (1:N)
       └── audit_logs (1:N)
```
