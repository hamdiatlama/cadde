-- ============================================================
-- DOMAIN: MESLEKLER (Professions)
-- ============================================================

-- Meslek kategorileri
CREATE TABLE profession_categories (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    slug            VARCHAR(200) UNIQUE NOT NULL,
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Meslekler
CREATE TABLE professions (
    id              SERIAL PRIMARY KEY,
    category_id     SMALLINT NOT NULL REFERENCES profession_categories(id) ON DELETE CASCADE,
    name            VARCHAR(200) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_professions_category ON professions(category_id);
CREATE INDEX idx_professions_name ON professions(name);

-- Hiyerarşik meslek yapısı (Sağlık gibi alt-dallanmalar için)
CREATE TABLE profession_hierarchy (
    id              SERIAL PRIMARY KEY,
    parent_id       INT REFERENCES profession_hierarchy(id) ON DELETE CASCADE,
    profession_id   INT NOT NULL REFERENCES professions(id) ON DELETE CASCADE,
    level           SMALLINT NOT NULL DEFAULT 0,
    path            LTREE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_prof_hierarchy_parent ON profession_hierarchy(parent_id);
CREATE INDEX idx_prof_hierarchy_path ON profession_hierarchy USING GIST(path);
