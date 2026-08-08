ALTER TABLE job_offers
ALTER COLUMN title TYPE VARCHAR(500);

ALTER TABLE job_offers
ALTER COLUMN company_name DROP NOT NULL;

ALTER TABLE job_offers
ALTER COLUMN company_name TYPE VARCHAR(500);

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS uuid VARCHAR(36);

UPDATE job_offers
SET uuid = md5(random()::text || clock_timestamp()::text)
WHERE uuid IS NULL;

ALTER TABLE job_offers
ALTER COLUMN uuid SET NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS ix_job_offers_uuid
ON job_offers (uuid);

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS city VARCHAR(255);

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS region VARCHAR(255);

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS country VARCHAR(255);

UPDATE job_offers
SET country = 'UNKNOWN'
WHERE country IS NULL;

ALTER TABLE job_offers
ALTER COLUMN country SET NOT NULL;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS url_primary TEXT;

UPDATE job_offers
SET url_primary = source_url
WHERE url_primary IS NULL
AND source_url IS NOT NULL;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS description_raw TEXT;

UPDATE job_offers
SET description_raw = description
WHERE description_raw IS NULL;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS description_normalized TEXT;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS language VARCHAR(20);

UPDATE job_offers
SET language = 'UNKNOWN'
WHERE language IS NULL;

ALTER TABLE job_offers
ALTER COLUMN language SET NOT NULL;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS work_mode VARCHAR(50);

UPDATE job_offers
SET work_mode = 'UNKNOWN'
WHERE work_mode IS NULL;

ALTER TABLE job_offers
ALTER COLUMN work_mode SET NOT NULL;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS contract_type VARCHAR(50);

UPDATE job_offers
SET contract_type = 'UNKNOWN'
WHERE contract_type IS NULL;

ALTER TABLE job_offers
ALTER COLUMN contract_type SET NOT NULL;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS seniority VARCHAR(50);

UPDATE job_offers
SET seniority = 'UNKNOWN'
WHERE seniority IS NULL;

ALTER TABLE job_offers
ALTER COLUMN seniority SET NOT NULL;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS salary_min INTEGER;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS salary_max INTEGER;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS salary_currency VARCHAR(10);

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS salary_original_text TEXT;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS skills_extracted JSON;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS skills_normalized JSON;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS quality_level VARCHAR(20);

UPDATE job_offers
SET quality_level = 'PARTIAL'
WHERE quality_level IS NULL;

ALTER TABLE job_offers
ALTER COLUMN quality_level SET NOT NULL;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS status VARCHAR(20);

UPDATE job_offers
SET status = 'ACTIVE'
WHERE status IS NULL;

ALTER TABLE job_offers
ALTER COLUMN status SET NOT NULL;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS archived_at TIMESTAMP;

ALTER TABLE job_offers
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP;

UPDATE job_offers
SET updated_at = created_at
WHERE updated_at IS NULL;

ALTER TABLE job_offers
ALTER COLUMN updated_at SET NOT NULL;

CREATE INDEX IF NOT EXISTS idx_job_offer_deduplication
ON job_offers (title, company_name, city);

CREATE TABLE IF NOT EXISTS job_sources (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL UNIQUE,
    source_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_job_source_name
ON job_sources (name);

CREATE TABLE IF NOT EXISTS job_offer_sources (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) NOT NULL UNIQUE,
    job_offer_id INTEGER NOT NULL REFERENCES job_offers(id),
    job_source_id INTEGER NOT NULL REFERENCES job_sources(id),
    source_job_id VARCHAR(255),
    source_url TEXT NOT NULL,
    first_seen_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_job_offer_source_url UNIQUE (
        job_offer_id,
        job_source_id,
        source_url
    )
);

CREATE INDEX IF NOT EXISTS idx_job_offer_sources_job_offer_id
ON job_offer_sources (job_offer_id);

CREATE INDEX IF NOT EXISTS idx_job_offer_sources_job_source_id
ON job_offer_sources (job_source_id);

CREATE INDEX IF NOT EXISTS idx_job_offer_sources_source_job_id
ON job_offer_sources (source_job_id);