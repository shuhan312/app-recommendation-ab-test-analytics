-- ============================================================
-- App Recommendation A/B Test Analytics
-- Table: users
-- Description: One row per user, containing experiment
--              assignment and post-install behaviour metrics.
-- ============================================================

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    userid             INTEGER PRIMARY KEY,
    version            TEXT    NOT NULL,          -- 'gate_30' or 'gate_40'
    treatment          INTEGER NOT NULL,          -- 0 = control, 1 = treatment
    sum_gamerounds     INTEGER NOT NULL,          -- total rounds in first 14 days
    retention_1        INTEGER NOT NULL,          -- 1 if user returned on day 1
    retention_7        INTEGER NOT NULL,          -- 1 if user returned on day 7
    engagement_segment TEXT    NOT NULL           -- non_player / low / medium / high
);
