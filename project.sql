-- ============================================================
-- 0. SPLIT DES TABLES BRUTES (salary_by_country_europe_*)
-- ============================================================

DROP TABLE IF EXISTS wage_nominal_by_country;

CREATE TABLE wage_nominal_by_country AS
SELECT
    TRIM(SUBSTR(c1, 1, INSTR(c1, ';') - 1))              AS country,
    CAST(TRIM(SUBSTR(c1, INSTR(c1, ';') + 1)) AS FLOAT)  AS nominal_wage
FROM salary_by_country_europe_nominal
WHERE c1 IS NOT NULL
  AND INSTR(c1, ';') > 0
  AND LOWER(TRIM(SUBSTR(c1, 1, INSTR(c1, ';') - 1))) <> 'country';


DROP TABLE IF EXISTS wage_ppp_by_country;

CREATE TABLE wage_ppp_by_country AS
SELECT
    TRIM(SUBSTR(c1, 1, INSTR(c1, ';') - 1))              AS country,
    CAST(TRIM(SUBSTR(c1, INSTR(c1, ';') + 1)) AS FLOAT)  AS ppp_wage
FROM salary_by_country_europe_ppp
WHERE c1 IS NOT NULL
  AND INSTR(c1, ';') > 0
  AND LOWER(TRIM(SUBSTR(c1, 1, INSTR(c1, ';') - 1))) <> 'country';


-- ============================================================
-- 1. TABLE DE BASE AVEC NIVEAUX ET LOGS
-- ============================================================

DROP TABLE IF EXISTS wage_level_by_country;

CREATE TABLE wage_level_by_country AS
SELECT
    n.country,
    n.nominal_wage,
    p.ppp_wage,
    ROUND(n.nominal_wage / p.ppp_wage, 4) AS price_level_index,
    LOG(n.nominal_wage)                   AS log_nominal_wage,
    LOG(p.ppp_wage)                       AS log_ppp_wage,
    LOG(n.nominal_wage / p.ppp_wage)      AS log_price_level_index
FROM wage_nominal_by_country n
JOIN wage_ppp_by_country p
  ON n.country = p.country;


-- ============================================================
-- 2. ECARTS VS FRANCE (NIVEAUX + LOGS)
-- ============================================================

DROP TABLE IF EXISTS wage_gap_vs_france;

CREATE TABLE wage_gap_vs_france AS
SELECT
    w.country,
    w.nominal_wage,
    w.ppp_wage,
    w.price_level_index,
    w.log_nominal_wage,
    w.log_ppp_wage,
    w.log_price_level_index,

    -- écarts en niveau
    w.nominal_wage      - f.nominal_wage      AS gap_nominal,
    w.ppp_wage          - f.ppp_wage          AS gap_ppp,
    w.price_level_index - f.price_level_index AS gap_price_level,

    -- écarts en log (≈ écarts relatifs)
    w.log_nominal_wage      - f.log_nominal_wage      AS gap_log_nominal,
    w.log_ppp_wage          - f.log_ppp_wage          AS gap_log_ppp,
    w.log_price_level_index - f.log_price_level_index AS gap_log_price_level
FROM wage_level_by_country w
CROSS JOIN (
    SELECT *
    FROM wage_level_by_country
    WHERE country = 'France'
) f;


-- ============================================================
-- 2bis. INDICATEURS SIMPLES VS FRANCE (COMPTES + RATIOS)
-- ============================================================

-- Comptes au-dessus / en-dessous de la France
DROP TABLE IF EXISTS france_basic_counts;

CREATE TABLE france_basic_counts AS
SELECT
    -- salaires réels
    SUM(
        CASE
            WHEN ppp_wage > (SELECT ppp_wage
                             FROM wage_level_by_country
                             WHERE country = 'France')
            THEN 1 ELSE 0
        END
    ) AS n_higher_real_wage_than_france,
    SUM(
        CASE
            WHEN ppp_wage < (SELECT ppp_wage
                             FROM wage_level_by_country
                             WHERE country = 'France')
            THEN 1 ELSE 0
        END
    ) AS n_lower_real_wage_than_france,

    -- salaires nominaux
    SUM(
        CASE
            WHEN nominal_wage > (SELECT nominal_wage
                                 FROM wage_level_by_country
                                 WHERE country = 'France')
            THEN 1 ELSE 0
        END
    ) AS n_higher_nominal_wage_than_france,
    SUM(
        CASE
            WHEN nominal_wage < (SELECT nominal_wage
                                 FROM wage_level_by_country
                                 WHERE country = 'France')
            THEN 1 ELSE 0
        END
    ) AS n_lower_nominal_wage_than_france,

    -- niveaux de prix
    SUM(
        CASE
            WHEN price_level_index > (SELECT price_level_index
                                      FROM wage_level_by_country
                                      WHERE country = 'France')
            THEN 1 ELSE 0
        END
    ) AS n_higher_price_level_than_france,
    SUM(
        CASE
            WHEN price_level_index < (SELECT price_level_index
                                      FROM wage_level_by_country
                                      WHERE country = 'France')
            THEN 1 ELSE 0
        END
    ) AS n_lower_price_level_than_france
FROM wage_level_by_country
WHERE country <> 'France';


-- Ratios (valeur pays / valeur France), France incluse (ratios = 1)
DROP TABLE IF EXISTS france_ratios;

CREATE TABLE france_ratios AS
SELECT
    w.country,
    w.nominal_wage,
    w.ppp_wage,
    w.price_level_index,
    w.nominal_wage      / f.nominal_wage      AS ratio_nominal_vs_france,
    w.ppp_wage          / f.ppp_wage          AS ratio_ppp_vs_france,
    w.price_level_index / f.price_level_index AS ratio_price_vs_france
FROM wage_level_by_country w
CROSS JOIN (
    SELECT *
    FROM wage_level_by_country
    WHERE country = 'France'
) f;


-- ============================================================
-- 3. DOMINANCE PARETO
-- ============================================================

DROP TABLE IF EXISTS country_dominance_counts;

CREATE TABLE country_dominance_counts AS
SELECT
    ref.country,
    ref.nominal_wage,
    ref.ppp_wage,
    ref.price_level_index,
    ref.log_nominal_wage,
    ref.log_ppp_wage,
    ref.log_price_level_index,
    COUNT(cmp.country) AS dominator_count
FROM wage_level_by_country AS ref
LEFT JOIN wage_level_by_country AS cmp
  ON cmp.country <> ref.country
 AND cmp.ppp_wage          > ref.ppp_wage
 AND cmp.price_level_index < ref.price_level_index
GROUP BY
    ref.country,
    ref.nominal_wage,
    ref.ppp_wage,
    ref.price_level_index,
    ref.log_nominal_wage,
    ref.log_ppp_wage,
    ref.log_price_level_index;


DROP TABLE IF EXISTS pareto_efficient_countries;

CREATE TABLE pareto_efficient_countries AS
SELECT *
FROM country_dominance_counts
WHERE dominator_count = 0
ORDER BY ppp_wage DESC;


DROP TABLE IF EXISTS top10_most_dominated_countries;

CREATE TABLE top10_most_dominated_countries AS
SELECT *
FROM country_dominance_counts
ORDER BY dominator_count DESC
LIMIT 10;


-- ============================================================
-- 4. QUATRE CATEGORIES VS FRANCE (SUR SALAIRE REEL & PRIX)
-- ============================================================
-- A: salaire réel > France & prix > France
-- B: salaire réel > France & prix < France
-- C: salaire réel < France & prix < France
-- D: salaire réel < France & prix > France
-- ============================================================

-- A) salaire réel ↑, prix ↑
DROP TABLE IF EXISTS higher_wage_higher_price_france;

CREATE TABLE higher_wage_higher_price_france AS
SELECT
    country,
    nominal_wage,
    ppp_wage,
    price_level_index,
    gap_nominal,
    gap_ppp,
    gap_price_level,
    gap_log_nominal,
    gap_log_ppp,
    gap_log_price_level
FROM wage_gap_vs_france
WHERE country <> 'France'
  AND gap_ppp > 0
  AND gap_price_level > 0;


-- B) salaire réel ↑, prix ↓
DROP TABLE IF EXISTS higher_wage_lower_price_france;

CREATE TABLE higher_wage_lower_price_france AS
SELECT
    country,
    nominal_wage,
    ppp_wage,
    price_level_index,
    gap_nominal,
    gap_ppp,
    gap_price_level,
    gap_log_nominal,
    gap_log_ppp,
    gap_log_price_level
FROM wage_gap_vs_france
WHERE country <> 'France'
  AND gap_ppp > 0
  AND gap_price_level < 0;


-- C) salaire réel ↓, prix ↓
DROP TABLE IF EXISTS lower_wage_lower_price_france;

CREATE TABLE lower_wage_lower_price_france AS
SELECT
    country,
    nominal_wage,
    ppp_wage,
    price_level_index,
    gap_nominal,
    gap_ppp,
    gap_price_level,
    gap_log_nominal,
    gap_log_ppp,
    gap_log_price_level
FROM wage_gap_vs_france
WHERE country <> 'France'
  AND gap_ppp < 0
  AND gap_price_level < 0;


-- D) salaire réel ↓, prix ↑
DROP TABLE IF EXISTS lower_wage_higher_price_france;

CREATE TABLE lower_wage_higher_price_france AS
SELECT
    country,
    nominal_wage,
    ppp_wage,
    price_level_index,
    gap_nominal,
    gap_ppp,
    gap_price_level,
    gap_log_nominal,
    gap_log_ppp,
    gap_log_price_level
FROM wage_gap_vs_france
WHERE country <> 'France'
  AND gap_ppp < 0
  AND gap_price_level > 0;
