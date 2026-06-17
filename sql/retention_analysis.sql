-- =============================================================
-- retention_analysis.sql
-- A/B Test: Retention Rate Analysis by Experiment Group
-- A/B 测试：按实验组分析留存率
--
-- Table: users
-- Columns used: version, retention_1, retention_7
-- =============================================================


-- -------------------------------------------------------------
-- Query 1: Sample Size by Group
-- 查询 1：各实验组的样本量
-- Verify that control and treatment groups are balanced.
-- 验证控制组和实验组的样本量是否均衡。
-- -------------------------------------------------------------
SELECT
    version                         AS experiment_group,  -- 'gate_30' = control / 控制组, 'gate_40' = treatment / 实验组
    COUNT(*)                        AS total_users,       -- total users assigned to this group / 该组总用户数
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) AS pct_of_total  -- share of all 90,189 users / 占总样本的百分比
FROM users
GROUP BY version
ORDER BY version;


-- -------------------------------------------------------------
-- Query 2: D1 and D7 Retention Rates by Group
-- 查询 2：各实验组的 D1 和 D7 留存率
-- Core metric comparison between control (gate_30) and treatment (gate_40).
-- 控制组（gate_30）与实验组（gate_40）的核心指标对比。
-- -------------------------------------------------------------
SELECT
    version                                                    AS experiment_group,
    COUNT(*)                                                   AS total_users,        -- total users in group / 该组总用户数
    SUM(retention_1)                                           AS retained_day1,      -- users who returned on Day 1 / 第1天回访的用户数
    ROUND(SUM(retention_1) * 100.0 / COUNT(*), 3)             AS d1_retention_pct,   -- D1 retention rate (%) / D1 留存率（%）
    SUM(retention_7)                                           AS retained_day7,      -- users who returned on Day 7 / 第7天回访的用户数（主指标）
    ROUND(SUM(retention_7) * 100.0 / COUNT(*), 3)             AS d7_retention_pct    -- D7 retention rate (%) — PRIMARY METRIC / D7 留存率（%）— 主指标
FROM users
GROUP BY version
ORDER BY version;


-- -------------------------------------------------------------
-- Query 3: Uplift — Treatment vs Control
-- 查询 3：实验组相对控制组的提升幅度（Uplift）
-- Uplift = treatment rate - control rate (positive = treatment better)
-- Uplift = 实验组留存率 - 控制组留存率（正值 = 实验组更好）
-- -------------------------------------------------------------
SELECT
    'D1 Retention'                                             AS metric,
    ROUND(MAX(CASE WHEN version = 'gate_30' THEN d1_pct END), 3) AS control_pct,
    ROUND(MAX(CASE WHEN version = 'gate_40' THEN d1_pct END), 3) AS treatment_pct,
    ROUND(
        MAX(CASE WHEN version = 'gate_40' THEN d1_pct END) -
        MAX(CASE WHEN version = 'gate_30' THEN d1_pct END),
    3)                                                         AS uplift_pp
FROM (
    SELECT version,
           SUM(retention_1) * 100.0 / COUNT(*) AS d1_pct
    FROM users
    GROUP BY version
)

UNION ALL

SELECT
    'D7 Retention (Primary)'                                   AS metric,
    ROUND(MAX(CASE WHEN version = 'gate_30' THEN d7_pct END), 3) AS control_pct,
    ROUND(MAX(CASE WHEN version = 'gate_40' THEN d7_pct END), 3) AS treatment_pct,
    ROUND(
        MAX(CASE WHEN version = 'gate_40' THEN d7_pct END) -
        MAX(CASE WHEN version = 'gate_30' THEN d7_pct END),
    3)                                                         AS uplift_pp
FROM (
    SELECT version,
           SUM(retention_7) * 100.0 / COUNT(*) AS d7_pct
    FROM users
    GROUP BY version
);


-- -------------------------------------------------------------
-- Query 4: Funnel — Retention by Engagement Level and Group
-- 查询 4：按参与深度拆分的留存率漏斗
-- Shows how D7 retention varies across engagement thresholds
-- for each experiment group.
-- 展示不同参与深度阈值下，两组 D7 留存率的差异。
-- -------------------------------------------------------------
-- NULLIF(..., 0) prevents division by zero if a subgroup has no users
-- NULLIF(..., 0) 防止某子组用户数为 0 时出现除以零的错误
SELECT
    version                                                         AS experiment_group,
    -- D7 retention rate among users who played at least once (>0 rounds)
    -- 至少玩过一局的用户中，第7天留存率
    ROUND(SUM(CASE WHEN sum_gamerounds >  0 THEN retention_7 ELSE 0 END) * 100.0
          / NULLIF(SUM(CASE WHEN sum_gamerounds >  0 THEN 1 ELSE 0 END), 0), 2) AS d7_played,
    -- D7 retention rate among engaged users (5+ rounds)
    -- 参与用户（5局以上）中，第7天留存率
    ROUND(SUM(CASE WHEN sum_gamerounds >= 5  THEN retention_7 ELSE 0 END) * 100.0
          / NULLIF(SUM(CASE WHEN sum_gamerounds >= 5  THEN 1 ELSE 0 END), 0), 2) AS d7_engaged_5plus,
    -- D7 retention rate among highly engaged users (30+ rounds, reached gate area)
    -- 深度参与用户（30局以上，到达关卡门槛区域）中，第7天留存率
    ROUND(SUM(CASE WHEN sum_gamerounds >= 30 THEN retention_7 ELSE 0 END) * 100.0
          / NULLIF(SUM(CASE WHEN sum_gamerounds >= 30 THEN 1 ELSE 0 END), 0), 2) AS d7_highly_engaged_30plus
FROM users
GROUP BY version
ORDER BY version;
