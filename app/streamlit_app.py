import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from statsmodels.stats.proportion import proportions_ztest
import warnings
warnings.filterwarnings('ignore')

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="App Recommendation A/B Test Analytics",
    page_icon=None,
    layout="wide"
)

# ── Load data ──────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = sqlite3.connect('data/app_ab_test.db')
    df = pd.read_sql_query('SELECT * FROM users', conn)
    conn.close()
    return df

df = load_data()
ctrl = df[df['version'] == 'gate_30']
trt  = df[df['version'] == 'gate_40']

# ── Sidebar navigation ─────────────────────────────────────
st.sidebar.title("Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Go to / 跳转至",
    ["Overview", "Funnel Analysis", "A/B Test Results", "Segment Analysis", "Final Recommendation"]
)

# ══════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ══════════════════════════════════════════════════════════
if page == "Overview":

    st.title("App Recommendation A/B Test Analytics")
    st.markdown("*An end-to-end product data science project evaluating whether a new in-app progression module improves user retention.*")
    st.markdown("---")

    # Experiment description
    st.subheader("Experiment Background / 实验背景")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **What was tested?**
        A mobile game tested moving the in-app progression gate from **round 30** to **round 40**.

        **Groups:**
        - **Control (gate_30):** Original version
        - **Treatment (gate_40):** New progression module

        **Primary metric:** 7-day retention
        """)

    with col2:
        st.markdown("""
        **测试内容**
        游戏将进度关卡门槛从**第 30 关**移至**第 40 关**，测试是否能提升留存率。

        **实验组别：**
        - **Control (gate_30)：** 旧版本
        - **Treatment (gate_40)：** 新推荐/进度模块

        **主指标：** 7 日留存率
        """)

    st.markdown("---")

    # Sample size metrics
    st.subheader("Sample Overview / 样本概况")
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(label="Total Users / 总用户数", value=f"{len(df):,}")
    with m2:
        st.metric(label="Control (gate_30)", value=f"{len(ctrl):,}")
    with m3:
        st.metric(label="Treatment (gate_40)", value=f"{len(trt):,}")
    with m4:
        ratio = len(ctrl) / len(trt)
        st.metric(label="Split Ratio / 分组比例", value=f"{ratio:.3f}")

    st.markdown("---")

    # Key results preview
    st.subheader("Key Results at a Glance / 核心结果一览")

    d1_ctrl = ctrl['retention_1'].mean()
    d1_trt  = trt['retention_1'].mean()
    d7_ctrl = ctrl['retention_7'].mean()
    d7_trt  = trt['retention_7'].mean()

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**D1 Retention / 1日留存率**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Control", f"{d1_ctrl:.2%}")
        c2.metric("Treatment", f"{d1_trt:.2%}", delta=f"{(d1_trt-d1_ctrl)*100:+.2f}pp")
        c3.metric("p-value", "0.074")

    with r2:
        st.markdown("**D7 Retention / 7日留存率 (Primary / 主指标)**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Control", f"{d7_ctrl:.2%}")
        c2.metric("Treatment", f"{d7_trt:.2%}", delta=f"{(d7_trt-d7_ctrl)*100:+.2f}pp")
        c3.metric("p-value", "0.002")

    st.markdown("---")
    st.info("Use the sidebar to navigate to detailed analysis. / 使用左侧导航栏查看详细分析。")


# ══════════════════════════════════════════════════════════
# PAGE 2: FUNNEL ANALYSIS
# ══════════════════════════════════════════════════════════
elif page == "Funnel Analysis":

    st.title("Funnel Analysis / 漏斗分析")
    st.markdown("User drop-off from install through to 7-day retention. / 用户从安装到 7 日留存的流失漏斗。")
    st.markdown("---")

    # Overall funnel data
    funnel_steps = ['Installed', 'Played\n(>0 rounds)', 'Engaged\n(5+ rounds)',
                    'Highly Engaged\n(30+ rounds)', 'D1 Retained', 'D7 Retained']
    funnel_values = [
        len(df),
        (df['sum_gamerounds'] > 0).sum(),
        (df['sum_gamerounds'] >= 5).sum(),
        (df['sum_gamerounds'] >= 30).sum(),
        df['retention_1'].sum(),
        df['retention_7'].sum(),
    ]
    funnel_pcts = [v / len(df) * 100 for v in funnel_values]

    fig, ax = plt.subplots(figsize=(12, 5))
    colors = plt.cm.Blues(np.linspace(0.85, 0.35, len(funnel_steps)))
    bars = ax.barh(funnel_steps[::-1], funnel_values[::-1], color=colors[::-1], height=0.6)
    for bar, val, pct in zip(bars, funnel_values[::-1], funnel_pcts[::-1]):
        ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
                f'{val:,}  ({pct:.1f}%)', va='center', fontsize=10)
    ax.set_title('User Engagement Funnel — All Users', fontsize=14)
    ax.set_xlabel('Number of Users')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.set_xlim(0, 110000)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    # Group comparison
    st.subheader("Funnel by Group / 两组漏斗对比")
    stages = ['Played', 'Engaged\n(5+)', 'Highly Engaged\n(30+)', 'D1 Retained', 'D7 Retained']
    ctrl_vals = [
        (ctrl['sum_gamerounds'] > 0).mean() * 100,
        (ctrl['sum_gamerounds'] >= 5).mean() * 100,
        (ctrl['sum_gamerounds'] >= 30).mean() * 100,
        ctrl['retention_1'].mean() * 100,
        ctrl['retention_7'].mean() * 100,
    ]
    trt_vals = [
        (trt['sum_gamerounds'] > 0).mean() * 100,
        (trt['sum_gamerounds'] >= 5).mean() * 100,
        (trt['sum_gamerounds'] >= 30).mean() * 100,
        trt['retention_1'].mean() * 100,
        trt['retention_7'].mean() * 100,
    ]

    x = np.arange(len(stages))
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.bar(x - 0.2, ctrl_vals, 0.4, label='Control (gate_30)', color='#4878CF', alpha=0.85)
    ax2.bar(x + 0.2, trt_vals,  0.4, label='Treatment (gate_40)', color='#D65F5F', alpha=0.85)
    for i, (c, t) in enumerate(zip(ctrl_vals, trt_vals)):
        ax2.text(i - 0.2, c + 0.3, f'{c:.1f}%', ha='center', fontsize=8, color='#4878CF', fontweight='bold')
        ax2.text(i + 0.2, t + 0.3, f'{t:.1f}%', ha='center', fontsize=8, color='#D65F5F', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(stages, fontsize=10)
    ax2.set_ylabel('Rate (%)')
    ax2.set_title('Funnel Conversion Rates: Control vs Treatment', fontsize=13)
    ax2.legend()
    ax2.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig2)


# ══════════════════════════════════════════════════════════
# PAGE 3: A/B TEST RESULTS
# ══════════════════════════════════════════════════════════
elif page == "A/B Test Results":

    st.title("A/B Test Results / A/B 检验结果")
    st.markdown("Hypothesis testing and confidence intervals for D1 and D7 retention. / D1 和 D7 留存率的假设检验与置信区间。")
    st.markdown("---")

    # Compute stats
    n_c, n_t = len(ctrl), len(trt)
    r1c = ctrl['retention_1'].sum(); r1t = trt['retention_1'].sum()
    r7c = ctrl['retention_7'].sum(); r7t = trt['retention_7'].sum()

    def get_stats(n1, x1, n2, x2):
        p1, p2 = x1/n1, x2/n2
        diff = p1 - p2
        z, p = proportions_ztest([x1, x2], [n1, n2], alternative='two-sided')
        se = np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
        return p1, p2, diff, p, diff-1.96*se, diff+1.96*se

    p1_d1, p2_d1, diff_d1, pval_d1, lo_d1, hi_d1 = get_stats(n_t, r1t, n_c, r1c)
    p1_d7, p2_d7, diff_d7, pval_d7, lo_d7, hi_d7 = get_stats(n_t, r7t, n_c, r7c)

    # Metrics
    st.subheader("Retention Rate Comparison / 留存率对比")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**D1 Retention / 1日留存率**")
        a, b, c = st.columns(3)
        a.metric("Control", f"{p2_d1:.2%}")
        b.metric("Treatment", f"{p1_d1:.2%}", delta=f"{diff_d1*100:+.2f}pp")
        c.metric("p-value", f"{pval_d1:.4f}")
        st.caption("Not statistically significant (p > 0.05) / 不显著（p > 0.05）")

    with col2:
        st.markdown("**D7 Retention / 7日留存率 — Primary Metric / 主指标**")
        a, b, c = st.columns(3)
        a.metric("Control", f"{p2_d7:.2%}")
        b.metric("Treatment", f"{p1_d7:.2%}", delta=f"{diff_d7*100:+.2f}pp")
        c.metric("p-value", f"{pval_d7:.4f}")
        st.caption("Statistically significant (p < 0.05) / 显著（p < 0.05）")

    st.markdown("---")

    # CI chart
    st.subheader("Uplift with 95% Confidence Interval / Uplift 与 95% 置信区间")
    fig, ax = plt.subplots(figsize=(9, 3))
    for y, diff, lo, hi, label, pval in [
        (1, diff_d1*100, lo_d1*100, hi_d1*100, 'D1 Retention', pval_d1),
        (0, diff_d7*100, lo_d7*100, hi_d7*100, 'D7 Retention\n(Primary)', pval_d7),
    ]:
        color = '#D65F5F' if hi < 0 else '#888888'
        ax.plot([lo, hi], [y, y], color=color, linewidth=4, solid_capstyle='round')
        ax.scatter([diff], [y], color=color, s=80, zorder=5)
        ax.text(hi + 0.05, y, f'{diff:+.2f}pp  CI[{lo:+.2f}, {hi:+.2f}]',
                va='center', fontsize=9, color=color)
    ax.axvline(0, color='black', linewidth=1.2, linestyle='--', alpha=0.4)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['D7 Retention\n(Primary)', 'D1 Retention'], fontsize=10)
    ax.set_xlabel('Uplift (percentage points)')
    ax.set_title('Treatment Uplift with 95% CI\nRed = significant | Grey = not significant', fontsize=11)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_xlim(-2.2, 1.2)
    plt.tight_layout()
    st.pyplot(fig)


# ══════════════════════════════════════════════════════════
# PAGE 4: SEGMENT ANALYSIS
# ══════════════════════════════════════════════════════════
elif page == "Segment Analysis":

    st.title("Segment Analysis / 分群分析")
    st.markdown("Does the treatment effect differ across user engagement segments? / treatment 效果在不同参与度分群中是否有差异？")
    st.markdown("---")

    seg_order = ['non_player', 'low', 'medium', 'high']
    seg_labels = ['Non-player\n(0 rounds)', 'Low\n(1-4 rounds)', 'Medium\n(5-29 rounds)', 'High\n(30+ rounds)']
    rows = []
    for seg in seg_order:
        s = df[df['engagement_segment'] == seg]
        c = s[s['version'] == 'gate_30']
        t = s[s['version'] == 'gate_40']
        rc, rt = c['retention_7'].sum(), t['retention_7'].sum()
        nc, nt = len(c), len(t)
        rate_c, rate_t = rc/nc, rt/nt
        diff = rate_t - rate_c
        z, p = proportions_ztest([rt, rc], [nt, nc], alternative='two-sided')
        se = np.sqrt(rate_t*(1-rate_t)/nt + rate_c*(1-rate_c)/nc)
        rows.append({'segment': seg, 'n_ctrl': nc, 'n_trt': nt,
                     'rate_ctrl': rate_c, 'rate_trt': rate_t,
                     'uplift': diff, 'p_value': p,
                     'ci_lo': diff-1.96*se, 'ci_hi': diff+1.96*se})
    df_seg = pd.DataFrame(rows)

    # Bar chart
    x = np.arange(len(seg_order))
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(x - 0.2, df_seg['rate_ctrl']*100, 0.4, label='Control (gate_30)', color='#4878CF', alpha=0.85)
    ax.bar(x + 0.2, df_seg['rate_trt']*100,  0.4, label='Treatment (gate_40)', color='#D65F5F', alpha=0.85)
    for i, row in df_seg.iterrows():
        ax.text(i - 0.2, row['rate_ctrl']*100 + 0.2, f"{row['rate_ctrl']:.1%}", ha='center', fontsize=8.5, color='#4878CF', fontweight='bold')
        ax.text(i + 0.2, row['rate_trt']*100  + 0.2, f"{row['rate_trt']:.1%}",  ha='center', fontsize=8.5, color='#D65F5F', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(seg_labels, fontsize=10)
    ax.set_ylabel('D7 Retention Rate (%)')
    ax.set_title('D7 Retention by Segment: Control vs Treatment', fontsize=13)
    ax.legend()
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    # CI chart
    st.subheader("Uplift by Segment / 各分群 Uplift")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    for i, (_, row) in enumerate(df_seg.iterrows()):
        y = len(df_seg) - 1 - i
        uplift = row['uplift'] * 100
        lo = row['ci_lo'] * 100
        hi = row['ci_hi'] * 100
        color = '#D65F5F' if (row['p_value'] < 0.05 and uplift < 0) else '#888888'
        ax2.plot([lo, hi], [y, y], color=color, linewidth=4, solid_capstyle='round')
        ax2.scatter([uplift], [y], color=color, s=80, zorder=5)
        ax2.text(hi + 0.08, y, f"{uplift:+.2f}pp  p={row['p_value']:.3f}", va='center', fontsize=9, color=color)
    ax2.axvline(0, color='black', linewidth=1.2, linestyle='--', alpha=0.4)
    ax2.set_yticks(range(len(seg_labels)))
    ax2.set_yticklabels(seg_labels[::-1], fontsize=10)
    ax2.set_xlabel('Uplift (percentage points)')
    ax2.set_title('Segment Uplift with 95% CI\nRed = significant | Grey = not significant', fontsize=11)
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.set_xlim(-2.8, 1.5)
    plt.tight_layout()
    st.pyplot(fig2)

    # Summary table
    st.markdown("---")
    st.subheader("Summary Table / 汇总表")
    display = df_seg[['segment', 'n_ctrl', 'n_trt', 'rate_ctrl', 'rate_trt', 'uplift', 'p_value']].copy()
    display['rate_ctrl'] = display['rate_ctrl'].map('{:.2%}'.format)
    display['rate_trt']  = display['rate_trt'].map('{:.2%}'.format)
    display['uplift']    = display['uplift'].map('{:+.3%}'.format)
    display['p_value']   = display['p_value'].map('{:.4f}'.format)
    display.columns = ['Segment', 'n Control', 'n Treatment', 'Control D7', 'Treatment D7', 'Uplift', 'p-value']
    st.dataframe(display, use_container_width=True)


# ══════════════════════════════════════════════════════════
# PAGE 5: FINAL RECOMMENDATION
# ══════════════════════════════════════════════════════════
elif page == "Final Recommendation":

    st.title("Final Recommendation / 最终建议")
    st.markdown("---")

    st.error("Do not launch gate_40 globally. / 不建议全量上线 gate_40。")

    st.markdown("---")
    st.subheader("Evidence / 数据依据")

    st.markdown("""
    **1. D7 retention decreased significantly overall.**
    The treatment group's 7-day retention was 0.82 percentage points lower than control (p=0.002).
    The 95% CI [-1.33pp, -0.31pp] is entirely below zero.

    **1. 整体 7 日留存率显著下降。**
    Treatment 组比 control 组低 0.82 个百分点（p=0.002），置信区间完全在 0 以下。

    ---

    **2. Medium-engagement users were significantly harmed.**
    The only statistically confirmed segment-level effect was a -0.56pp drop in the medium segment (p=0.027).

    **2. 普通玩家受到了显著的负面影响。**
    唯一统计显著的分群效果为 medium 分群下降 0.56 个百分点（p=0.027）。

    ---

    **3. No segment showed a significant positive effect.**
    The slightly positive signal in the low-engagement segment (+0.19pp) was not statistically significant (p=0.256).

    **3. 没有任何分群出现显著正向效果。**
    低参与度分群的微弱正向信号（+0.19pp）不具统计显著性（p=0.256）。
    """)

    st.markdown("---")
    st.subheader("Next Steps / 下一步建议")
    st.markdown("""
    1. Keep the current version (gate_30). / 维持当前版本（gate_30）。
    2. Redesign the progression gate timing based on user research. / 基于用户研究重新设计关卡门槛时机。
    3. Run a follow-up experiment with event-level tracking. / 设计包含事件级别追踪的后续实验。
    4. Collect pre-experiment user features for better segment analysis. / 收集实验前用户特征以支持更严格的分群分析。
    """)
