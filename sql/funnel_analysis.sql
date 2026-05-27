-- ============================================================
-- Funnel Analysis
-- 漏斗分析
--
-- Compares control (gate_30) vs treatment (gate_40) at each
-- engagement stage, from install through to 7-day retention.
-- 对比 control（gate_30）和 treatment（gate_40）在每个参与阶段的表现，
-- 从安装游戏一直到 7 日留存。
--
-- Note: Because the dataset is user-level (not event-level),
-- the funnel is constructed using game-round thresholds as
-- proxies for engagement depth.
-- 注意：由于数据集是用户级别数据（而非事件级别），
-- 漏斗使用游戏轮数阈值来代替真实用户行为路径。
--
-- Funnel stages defined / 漏斗阶段定义：
--   installed      → all users（所有用户，基准线）
--   played         → sum_gamerounds > 0  （至少玩过一局）
--   engaged        → sum_gamerounds >= 5  （玩了足够多，看到了基本内容）
--   highly_engaged → sum_gamerounds >= 30 （到达关卡门槛附近）
--   retained_day1  → 第1天回来（短期留存）
--   retained_day7  → 第7天回来（长期粘性，主指标）
-- ============================================================


-- ── Query 1: Overall funnel (both groups combined) ─────────
-- 整体漏斗（两组合并）
-- Purpose: Understand the overall drop-off pattern across all users
-- 目的：了解所有用户在漏斗中的整体流失情况
-- Each row = one funnel stage
-- 每一行 = 漏斗中的一个阶段

SELECT
    'installed'      AS funnel_step,   -- Stage name (label only) / 阶段名称（仅作标签）
    1                AS step_order,    -- Used for sorting stages in correct order / 用于按正确顺序排列阶段
    COUNT(*)         AS users,         -- Number of users at this stage / 该阶段的用户数量
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 1) AS pct_of_total
    -- pct_of_total: what % of ALL installed users reached this stage
    -- 占所有安装用户的百分比
FROM users

UNION ALL

SELECT
    'played'         AS funnel_step,
    2                AS step_order,
    COUNT(*)         AS users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 1) AS pct_of_total
FROM users
WHERE sum_gamerounds > 0             -- At least 1 game round played / 至少玩过一局

UNION ALL

SELECT
    'engaged'        AS funnel_step,
    3                AS step_order,
    COUNT(*)         AS users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 1) AS pct_of_total
FROM users
WHERE sum_gamerounds >= 5            -- Played enough to be considered "engaged" / 玩了足够多局，视为"参与用户"

UNION ALL

SELECT
    'highly_engaged' AS funnel_step,
    4                AS step_order,
    COUNT(*)         AS users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 1) AS pct_of_total
FROM users
WHERE sum_gamerounds >= 30           -- Reached the gate area / 到达关卡门槛区域

UNION ALL

SELECT
    'retained_day1'  AS funnel_step,
    5                AS step_order,
    COUNT(*)         AS users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 1) AS pct_of_total
FROM users
WHERE retention_1 = 1                -- User returned on Day 1 / 用户在第1天回来了（短期留存）

UNION ALL

SELECT
    'retained_day7'  AS funnel_step,
    6                AS step_order,
    COUNT(*)         AS users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 1) AS pct_of_total
FROM users
WHERE retention_7 = 1                -- User returned on Day 7 (PRIMARY METRIC) / 用户在第7天回来了（主指标）

ORDER BY step_order;


-- ── Query 2: Funnel split by group (control vs treatment) ──
-- 按实验组拆分的漏斗（control vs treatment）
-- Purpose: Compare how control and treatment users move through the same funnel
-- 目的：对比两组用户在漏斗各阶段的差异，找出两组在哪一步开始分化
-- Each row = one experiment group
-- 每一行 = 一个实验组（gate_30 或 gate_40）

SELECT
    version,                          -- 'gate_30' = control（对照组）, 'gate_40' = treatment（实验组）

    COUNT(*) AS installed,            -- Total users in this group / 该组总用户数

    -- played: user opened the game at least once after installing
    -- 玩过：用户安装后至少打开并玩了一局
    SUM(CASE WHEN sum_gamerounds > 0  THEN 1 ELSE 0 END) AS played,
    ROUND(SUM(CASE WHEN sum_gamerounds > 0  THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS played_rate,

    -- engaged: user played 5+ rounds (saw meaningful content)
    -- 参与：用户玩了5局以上，接触到了足够的游戏内容
    SUM(CASE WHEN sum_gamerounds >= 5  THEN 1 ELSE 0 END) AS engaged,
    ROUND(SUM(CASE WHEN sum_gamerounds >= 5  THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS engaged_rate,

    -- highly_engaged: user played 30+ rounds (reached the gate area)
    -- 深度参与：用户玩了30局以上，到达了关卡门槛区域
    SUM(CASE WHEN sum_gamerounds >= 30 THEN 1 ELSE 0 END) AS highly_engaged,
    ROUND(SUM(CASE WHEN sum_gamerounds >= 30 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS highly_engaged_rate,

    -- D1 retention: did the user come back the next day?
    -- D1 留存：用户第二天有没有回来？反映游戏第一印象
    SUM(retention_1) AS retained_day1,
    ROUND(SUM(retention_1) * 100.0 / COUNT(*), 1) AS d1_retention_rate,

    -- D7 retention: did the user come back 7 days later? (PRIMARY METRIC)
    -- D7 留存：用户第7天有没有回来？（主指标）反映游戏长期粘性
    SUM(retention_7) AS retained_day7,
    ROUND(SUM(retention_7) * 100.0 / COUNT(*), 1) AS d7_retention_rate

FROM users
GROUP BY version
ORDER BY version;
