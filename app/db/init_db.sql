-- ======================================
-- SmartRecruitz Database Initialization
-- ======================================

-- Create table
CREATE TABLE IF NOT EXISTS candidates_staging (
    candidate_id VARCHAR(36) PRIMARY KEY,

    parse_status VARCHAR(50) NOT NULL,

    processing_stage VARCHAR(50) NOT NULL,

    raw_text TEXT,

    confidence_score FLOAT,

    structured_profile JSONB NOT NULL,

    candidate_status VARCHAR(50),

    error_message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================================
-- Indexes
-- ======================================

CREATE INDEX IF NOT EXISTS idx_candidate_status
ON candidates_staging(candidate_status);

CREATE INDEX IF NOT EXISTS idx_created_at
ON candidates_staging(created_at);

CREATE INDEX IF NOT EXISTS idx_confidence_score
ON candidates_staging(confidence_score);

CREATE INDEX IF NOT EXISTS idx_processing_stage
ON candidates_staging(processing_stage);

-- ======================================
-- Trigger Function
-- ======================================

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ======================================
-- Trigger
-- ======================================

DROP TRIGGER IF EXISTS update_candidates_staging_updated_at
ON candidates_staging;

CREATE TRIGGER update_candidates_staging_updated_at
BEFORE UPDATE ON candidates_staging
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
