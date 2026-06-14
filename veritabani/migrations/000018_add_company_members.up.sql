-- ============================================================
-- MIGRATION 000018: Emlak Şirket Üyeleri / Ekip Yönetimi
-- ============================================================
-- Şirket yöneticisi kendi şirketine uzman/danışman/agent ekleyebilir

CREATE TABLE company_members (
    id              SERIAL PRIMARY KEY,
    company_id      INT NOT NULL REFERENCES contractor_companies(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role            VARCHAR(30) NOT NULL DEFAULT 'agent', -- yonetici, uzman, danisman, agent
    title           VARCHAR(100), -- Uzman Emlak Danışmanı, Kıdemli Danışman vb.
    is_active       BOOLEAN NOT NULL DEFAULT true,
    joined_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (company_id, user_id)
);

CREATE INDEX idx_company_members_company ON company_members(company_id);
CREATE INDEX idx_company_members_user ON company_members(user_id);

-- Yetki talep / davet tablosu (şirkete katılma talebi veya davet)
CREATE TABLE company_invitations (
    id              SERIAL PRIMARY KEY,
    company_id      INT NOT NULL REFERENCES contractor_companies(id) ON DELETE CASCADE,
    inviter_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    invitee_id      UUID REFERENCES users(id) ON DELETE CASCADE,
    invitee_email   VARCHAR(200), -- email ile davet (kullanıcı yoksa)
    role            VARCHAR(30) NOT NULL DEFAULT 'agent',
    status          VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, accepted, rejected, cancelled
    message         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_company_invitations_company ON company_invitations(company_id);
CREATE INDEX idx_company_invitations_invitee ON company_invitations(invitee_id);
