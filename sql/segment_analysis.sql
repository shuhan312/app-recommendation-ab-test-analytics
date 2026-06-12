-- =============================================================
-- segment_analysis.sql
-- Heterogeneous Treatment Effect (HTE) Analysis by User Segment
-- 异质性处理效应（HTE）分群分析
--
-- Segments are defined in notebook 01 based on sum_gamerounds:
-- 分群定义（notebook 01 中生成，基于 sum_gamerounds）：
--   non_player : 0 rounds       — installed but never played / 安装后从未玩过
--   low        : 1–4 rounds     — light engagement / 轻度参与
--   medium     : 5–29 rounds    — regular players  / 普通玩家
--   high       : 30+ rounds     — heavy players    / 重度玩家
--
-- Table: users
-- Columns used: version, engagement_segment, retention_7
-- =============================================================


-- -------------------------------------------------------------
-- Query 1: Sample Size by Segment and Group
-- 查询 1：各分群内两组的样本量
-- Verify balance within each segment.
-- 验证每个分群内控制组和实验组的样本量是否均衡。
-- -------------------------------------------------------------
SELECT
    engagement_segment,
    version                          AS experiment_group,
    COUNT(*)                         AS total_users
FROM users
GROUP BY engagement_segment, version
ORDER BY
    CASE engagement_segment
        WHEN 'non_player' THEN 1
        WHEN 'low'        THEN 2
        WHEN 'medium'     THEN 3
        WHEN 'high'       THEN 4
    END,
    version;


-- -------------------------------------------------------------
-- Query 2: D7 Retention Rate by Segment and Group
-- 查询 2：各分群内两组的 D7 留存率
-- Core table for heterogeneous treatment effect analysis.
-- 异质性处理效应分析的核心数据表。
-- -------------------------------------------------------------
SELECT
    engagement_segment,
    version                                                     AS experiment_group,
    COUNT(*)                                                    AS total_users,
    SUM(retention_7)                                            AS retained_day7,
    ROUND(SUM(retention_7) * 100.0 / COUNT(*), 3)              AS d7_retention_pct
FROM users
GROUP BY engagement_segment, version
ORDER BY
    CASE engagement_segment
        WHEN 'non_player' THEN 1
        WHEN 'low'        THEN 2
        WHEN 'medium'     THEN 3
        WHEN 'high'       THEN 4
    END,
    version;


-- -------------------------------------------------------------
-- Query 3: Uplift by Segment (Treatment vs Control)
-- 查询 3：各分群的 Uplift（实验组 vs 控制组）
-- Uplift = treatment D7 rate - control D7 rate
-- Uplift = 实验组 D7 留存率 - 控制组 D7 留存率
-- Negative uplift means treatment performed worse in that segment.
-- 负的 uplift 表示该分群内实验组表现更差。
-- -------------------------------------------------------------
SELECT
    engagement_segment,
    ROUND(MAX(CASE WHEN version = 'gate_30' THEN d7_pct END), 3) AS control_d7_pct,
    ROUND(MAX(CASE WHEN version = 'gate_40' THEN d7_pct END), 3) AS treatment_d7_pct,
    ROUND(
        MAX(CASE WHEN version = 'gate_40' THEN d7_pct END) -
        MAX(CASE WHEN version = 'gate_30' THEN d7_pct END),
    3)                                                           AS uplift_pp,
    CASE
        WHEN MAX(CASE WHEN version = 'gate_40' THEN d7_pct END) >
             MAX(CASE WHEN version = 'gate_30' THEN d7_pct END)
        THEN 'treatment higher / 实验组更高'
        ELSE 'control higher / 控制组更高'
    END                                                          AS direction
FROM (
    SELECT
        engagement_segment,
        version,
        SUM(retention_7) * 100.0 / COUNT(*) AS d7_pct
    FROM users
    GROUP BY engagement_segment, version
)
GROUP BY engagement_segment
ORDER BY
    CASE engagement_segment
        WHEN 'non_player' THEN 1
        WHEN 'low'        THEN 2
        WHEN 'medium'     THEN 3
        WHEN 'high'       THEN 4
    END;


-- -------------------------------------------------------------
-- Query 4: Segment Size as Share of Total
-- 查询 4：各分群占总样本的比例
-- Helps interpret the business importance of each segment.
-- 帮助判断每个分群在业务层面的重要程度。
-- -------------------------------------------------------------
SELECT
    engagement_segment,
    COUNT(*)                                                     AS segment_users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2)   AS pct_of_total,
    ROUND(SUM(retention_7) * 100.0 / COUNT(*), 3)               AS overall_d7_pct
FROM users
GROUP BY engagement_segment
ORDER BY
    CASE engagement_segment
        WHEN 'non_player' THEN 1
        WHEN 'low'        THEN 2
        WHEN 'medium'     THEN 3
        WHEN 'high'       THEN 4
    END;
