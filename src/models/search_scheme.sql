-- DROP MATERIALIZED VIEW biodatabase_search;
-- DROP MATERIALIZED VIEW bioentry_search;
-- DROP MATERIALIZED VIEW taxon_search;

-- Biodatabase materialized view

CREATE MATERIALIZED VIEW biodatabase_search AS
    SELECT biodatabase_id,
        to_tsvector('english',
            name
            || ' ' || coalesce(authority, '')
            || ' ' || coalesce(description, '')
        ) as document
    FROM biodatabase;
CREATE INDEX idx_fts_biodatabase ON biodatabase_search USING gin(document);

-- Taxon materialized view

CREATE MATERIALIZED VIEW taxon_search AS
    SELECT taxon_id,
        to_tsvector('english', string_agg(name, ' ')) as document
    FROM taxon_name
    GROUP BY taxon_id;
CREATE INDEX idx_fts_taxon ON taxon_search USING gin(document);

-- Bioentry materialized view

CREATE MATERIALIZED VIEW bioentry_search AS
    SELECT bioentry.bioentry_id, bioentry.biodatabase_id, bioentry.taxon_id,
        to_tsvector('english',
            bioentry.name
            || ' ' || bioentry.accession
            || ' ' || coalesce(bioentry.identifier, '')
            || ' ' || coalesce(bioentry.division, '')
            || ' ' || coalesce(bioentry.description , '')
            || ' ' || bioentry.version
            || ' ' || biodatabase.name
            || ' ' || coalesce(biodatabase.authority, '')
            || ' ' || coalesce(biodatabase.description, '')
            || ' ' || coalesce(string_agg(taxon_name.name, ' '), '')
        ) as document
    FROM bioentry
    JOIN biodatabase ON biodatabase.biodatabase_id = bioentry.biodatabase_id
    LEFT JOIN taxon_name ON taxon_name.taxon_id = bioentry.taxon_id
    GROUP BY bioentry.bioentry_id, biodatabase.biodatabase_id;
CREATE INDEX idx_fts_bioentry ON bioentry_search USING gin(document);

-- Update

-- REFRESH MATERIALIZED VIEW biodatabase_search;
-- REFRESH MATERIALIZED VIEW bioentry_search;
-- REFRESH MATERIALIZED VIEW taxon_search;
