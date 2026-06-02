# Executive Summary — App Recommendation A/B Test
# 执行摘要 — App 推荐模块 A/B 实验

---

## Recommendation / 最终建议

**Do not launch gate_40 globally.**
**不建议全量上线 gate_40。**

The new recommendation/progression module did not improve user retention. It caused a statistically significant decrease in 7-day retention, with the most confirmed harm to medium-engagement users.

新推荐/进度模块未能提升用户留存率。整体 7 日留存率出现了统计显著的下降，其中对普通玩家（medium 分群）的负面影响得到了最确定的数据支撑。

---

## Experiment Background / 实验背景

| | English | 中文 |
|---|---|---|
| **Experiment** | Moving the progression gate from round 30 to round 40 | 将进度门槛从第 30 关移至第 40 关 |
| **Control group** | gate_30 — original version | gate_30 — 旧版本 |
| **Treatment group** | gate_40 — new module | gate_40 — 新推荐/进度模块 |
| **Sample size** | 90,189 users total | 共 90,189 名用户 |
| **Primary metric** | 7-day retention | 7 日留存率 |
| **Secondary metric** | 1-day retention, total game rounds | 1 日留存率、总游戏轮数 |

This experiment randomly assigned users to one of two versions of the game at install time, then measured whether the change in gate placement affected how many users returned after 1 day and 7 days.

本次实验在用户安装游戏时将其随机分配至两个版本之一，随后观察关卡门槛位置的改变是否影响了用户在第 1 天和第 7 天的回访率。

---

## Key Numbers / 关键数字

### Overall Retention / 整体留存率

| Metric / 指标 | Control (gate_30) | Treatment (gate_40) | Uplift | p-value | Significant / 显著 |
|---|---|---|---|---|---|
| D1 Retention / 1日留存 | 44.82% | 44.23% | -0.59pp | 0.074 | No / 否 |
| D7 Retention / 7日留存 | 19.02% | 18.20% | -0.82pp | 0.002 | Yes / 是 |

### Segment-level D7 Retention / 分群 7 日留存率

| Segment / 分群 | Control | Treatment | Uplift | p-value | Significant / 显著 |
|---|---|---|---|---|---|
| Non-player (0 rounds) | 0.8% | 0.6% | -0.19pp | 0.470 | No / 否 |
| Low (1-4 rounds) | 1.2% | 1.4% | +0.19pp | 0.256 | No / 否 |
| Medium (5-29 rounds) | 6.2% | 5.6% | -0.56pp | 0.027 | Yes / 是 |
| High (30+ rounds) | 43.9% | 43.0% | -0.87pp | 0.108 | No / 否 |

The tables show that the treatment group performed worse than control on the primary metric (D7 retention) at both the overall level and within the medium segment. The only positive signal came from low-engagement users, but it was not statistically significant and the absolute numbers were very small.

数据表格显示，treatment 组在主指标（7 日留存率）上，无论是整体层面还是 medium 分群内部，均低于 control 组。唯一正向信号来自低参与度用户，但该差距不具统计显著性，且绝对数值极小，无法作为上线依据。

---

## Key Findings / 主要发现

**1. The new module significantly reduced 7-day retention overall.**
**新模块显著降低了整体 7 日留存率。**

The treatment group's D7 retention was 0.82 percentage points lower than control (p=0.002). The 95% confidence interval [-1.33pp, -0.31pp] is entirely below zero, confirming this is not random variation.

Treatment 组的 7 日留存率比 control 组低 0.82 个百分点（p=0.002），95% 置信区间 [-1.33pp, -0.31pp] 完全在 0 以下，排除了随机波动的可能。

This is the most important finding. The primary metric moved in the wrong direction, and the statistical evidence is strong enough to be conclusive.

这是最核心的发现。主指标朝错误方向移动，且统计证据足够强，可以作为明确结论。

---

**2. The effect on 1-day retention was not statistically significant.**
**1 日留存率的差距不显著。**

The -0.59pp difference in D1 retention (p=0.074) is within the range of random noise and cannot be treated as a confirmed finding.

D1 留存率的 -0.59pp 差距（p=0.074）在随机误差范围内，不能作为确定性结论。

Although the direction is negative, the evidence is not strong enough to confirm a real effect on day 1. The primary basis for the recommendation rests on the D7 result.

尽管方向为负，但证据不足以确认 D1 留存率存在真实影响。本次建议的主要依据为 D7 的结果。

---

**3. Medium-engagement users were the most conclusively harmed.**
**普通玩家（Medium）是受影响最确定的群体。**

Among all segments, only the medium group (5-29 rounds) showed a statistically significant negative effect (p=0.027). These are regular players who engaged with the game but had not yet reached the gate area — the new module appears to have disrupted their experience.

在所有分群中，只有 medium 分群（5-29 局）的负效果达到统计显著（p=0.027）。这类用户有一定参与度但尚未到达关卡门槛区域，新模块可能干扰了他们的游戏体验。

This segment represents the largest portion of engaged users and is the most commercially valuable group to retain. A confirmed negative effect here is a strong signal against launch.

该分群代表了参与用户中最大的群体，也是留存价值最高的商业群体。该分群确认出现负效果，是反对上线的重要信号。

---

**4. The effect on high-engagement users is directionally negative but unconfirmed.**
**重度玩家（High）的负向趋势明显但未得到统计确认。**

Heavy players (30+ rounds) showed the largest observed uplift (-0.87pp), but the result did not reach statistical significance (p=0.108). This may be due to insufficient sample size and warrants further investigation.

重度玩家（30+ 局）观察到最大的 uplift（-0.87pp），但未达到统计显著（p=0.108），可能受限于该分群的样本量，需进一步研究。

While this finding cannot be used as a definitive conclusion, the consistent negative direction across all segments strengthens the overall case against the new module.

尽管该发现不能作为确定性结论，但所有分群方向一致的负向趋势，进一步加强了反对新模块的整体论据。

---

## Limitations / 局限性

**The dataset is user-level, not event-level.**
**数据集为用户级别而非事件级别。**

The engagement funnel was constructed using game-round thresholds as proxies, which may not fully capture real user behaviour.

参与漏斗使用游戏轮数阈值构建，可能无法完整反映真实用户行为路径。

---

**No pre-experiment covariates are available.**
**缺乏实验前用户特征数据。**

Sample balance was assessed by size and post-treatment engagement distributions only, not by baseline user characteristics.

样本平衡性仅通过样本量和实验后参与分布进行了诊断性验证，未能基于实验前用户特征进行严格验证。

---

**Engagement segments are post-treatment constructs.**
**参与度分群基于实验后数据定义。**

The low / medium / high segments are defined using post-treatment game rounds, which may partially reflect the treatment effect itself rather than being pure baseline characteristics.

分群（low / medium / high）基于实验后的游戏轮数定义，可能部分反映了 treatment 效果本身，而非纯粹的用户基线特征。

These limitations do not invalidate the overall conclusion, but they do suggest that the segment-level findings should be interpreted with care and validated with richer data in future experiments.

上述局限性不影响整体结论的有效性，但提示分群层面的发现应谨慎解读，并在未来实验中通过更丰富的数据加以验证。

---

## Next Steps / 下一步建议

**1. Keep the current version (gate_30).**
**维持当前版本（gate_30）。**

The evidence does not support launching gate_40 at any scale. Rolling back or maintaining the original version is the appropriate product decision.

现有证据不支持在任何规模上线 gate_40。维持或回退至原版本是当前合适的产品决策。

---

**2. Redesign the progression gate timing.**
**重新设计关卡门槛的时机。**

Consider user research or qualitative testing to understand what gate placement actually improves the user experience before running another experiment.

在开展下一次实验之前，建议先通过用户研究或定性测试，了解什么样的关卡设置真正能改善用户体验。

---

**3. Run a follow-up experiment with richer tracking.**
**设计更完整追踪的后续实验。**

Collect event-level data (per-session play, drop-off points) to build a more accurate funnel and better measure where users disengage.

收集事件级别数据（每局游玩、流失节点），构建更精确的漏斗，更准确地定位用户流失位置。

---

**4. Collect pre-experiment user features.**
**收集实验前用户特征。**

Demographics, device type, or prior engagement history would enable more rigorous heterogeneous treatment effect analysis and more reliable segment-level conclusions in future experiments.

用户画像、设备类型或历史参与数据将支持未来实验中更严格的异质性处理效应分析，使分群层面的结论更加可靠。

---

*Analysis conducted using Cookie Cats A/B test dataset. Full methodology and code available in the project notebooks.*
*分析基于 Cookie Cats A/B 实验数据集。完整方法论和代码详见项目 notebooks。*
