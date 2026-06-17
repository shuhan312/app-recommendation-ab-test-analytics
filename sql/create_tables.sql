-- ============================================================
-- App Recommendation A/B Test Analytics
-- Table: users
-- Description: One row per user, containing experiment
--              assignment and post-install behaviour metrics.
-- 每一行代表一名用户，包含实验分组信息和安装后的行为指标。
-- ============================================================

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    userid             INTEGER PRIMARY KEY,
    version            TEXT    NOT NULL,  -- 'gate_30' (control / 控制组) or 'gate_40' (treatment / 实验组)
    treatment          INTEGER NOT NULL,  -- 0 = control / 控制组, 1 = treatment / 实验组
    sum_gamerounds     INTEGER NOT NULL,  -- total game rounds played in first 14 days / 安装后前14天的总游戏局数
    retention_1        INTEGER NOT NULL,  -- 1 if user returned on Day 1, else 0 / 用户是否在第1天回访（1=是，0=否）
    retention_7        INTEGER NOT NULL,  -- 1 if user returned on Day 7, else 0 / 用户是否在第7天回访（1=是，0=否）（主指标）
    engagement_segment TEXT    NOT NULL   -- non_player(0局) / low(1-4局) / medium(5-29局) / high(30+局)
);
