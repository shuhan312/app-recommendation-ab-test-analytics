"""
A/B Testing utility functions.
封装 A/B 测试的核心统计函数，供 notebooks 调用。

Functions
---------
run_ztest           : Two-proportion z-test (two-sided)
compute_uplift_ci   : 95% confidence interval for the uplift
run_ab_test         : Full pipeline — rates, uplift, z-test, CI in one call
print_ab_result     : Pretty-print an ABTestResult
"""

import numpy as np
from dataclasses import dataclass
from statsmodels.stats.proportion import proportions_ztest


@dataclass
class ABTestResult:
    """All outputs from a single A/B test comparison. / 单次 A/B 测试的完整结果。"""
    metric: str
    n_ctrl: int
    n_trt: int
    x_ctrl: int        # successes (retained users) in control / 控制组留存用户数
    x_trt: int         # successes (retained users) in treatment / 实验组留存用户数
    rate_ctrl: float   # retention rate, control / 控制组留存率
    rate_trt: float    # retention rate, treatment / 实验组留存率
    abs_uplift: float  # treatment rate - control rate / 绝对提升（pp）
    rel_uplift: float  # abs_uplift / control rate / 相对提升（%）
    z_stat: float
    p_value: float
    ci_lower: float    # lower bound of 95% CI for uplift / uplift 置信区间下界
    ci_upper: float    # upper bound of 95% CI for uplift / uplift 置信区间上界
    significant: bool  # p_value < alpha
    alpha: float


def run_ztest(n_ctrl, x_ctrl, n_trt, x_trt):
    """
    Two-proportion z-test (two-sided).
    双比例 z 检验（双尾）。

    Parameters
    ----------
    n_ctrl, x_ctrl : total and retained users in control group
    n_trt,  x_trt  : total and retained users in treatment group

    Returns
    -------
    (z_statistic, p_value)
    """
    z_stat, p_value = proportions_ztest(
        count=[x_trt, x_ctrl],
        nobs=[n_trt, n_ctrl],
        alternative='two-sided'
    )
    return float(z_stat), float(p_value)


def compute_uplift_ci(n_ctrl, x_ctrl, n_trt, x_trt, alpha=0.05):
    """
    95% confidence interval for the difference in two proportions.
    两个比例之差的置信区间。

    Formula: (p_trt - p_ctrl) ± z_crit * sqrt(p_trt*(1-p_trt)/n_trt + p_ctrl*(1-p_ctrl)/n_ctrl)

    Returns
    -------
    (uplift, ci_lower, ci_upper)  — all in percentage-point units as floats
    """
    p_trt  = x_trt  / n_trt
    p_ctrl = x_ctrl / n_ctrl
    diff   = p_trt - p_ctrl
    se     = np.sqrt(p_trt  * (1 - p_trt)  / n_trt +
                     p_ctrl * (1 - p_ctrl) / n_ctrl)
    z_crit = 1.96   # z-value for 95% CI (alpha=0.05) / 95% 置信区间对应的 z 值
    return diff, diff - z_crit * se, diff + z_crit * se


def run_ab_test(df, metric_col, group_col='version',
                control_label='gate_30', treatment_label='gate_40', alpha=0.05):
    """
    Full A/B test pipeline for a binary metric.
    对二元指标运行完整的 A/B 测试流程。

    Computes in one call:
      - retention rates for each group / 两组留存率
      - absolute and relative uplift / 绝对提升与相对提升
      - two-proportion z-test / 双比例 z 检验
      - 95% confidence interval for the uplift / uplift 的置信区间

    Parameters
    ----------
    df             : pd.DataFrame with user-level data
    metric_col     : binary outcome column (0/1), e.g. 'retention_7'
    group_col      : column identifying the experiment group
    control_label  : value in group_col for control
    treatment_label: value in group_col for treatment
    alpha          : significance level (default 0.05)

    Returns
    -------
    ABTestResult dataclass
    """
    ctrl = df[df[group_col] == control_label]
    trt  = df[df[group_col] == treatment_label]

    n_ctrl = len(ctrl)
    n_trt  = len(trt)
    x_ctrl = int(ctrl[metric_col].sum())
    x_trt  = int(trt[metric_col].sum())

    rate_ctrl  = x_ctrl / n_ctrl
    rate_trt   = x_trt  / n_trt
    abs_uplift = rate_trt - rate_ctrl
    rel_uplift = abs_uplift / rate_ctrl if rate_ctrl != 0 else float('nan')

    z_stat, p_value             = run_ztest(n_ctrl, x_ctrl, n_trt, x_trt)
    uplift, ci_lower, ci_upper  = compute_uplift_ci(n_ctrl, x_ctrl, n_trt, x_trt, alpha)

    return ABTestResult(
        metric=metric_col,
        n_ctrl=n_ctrl,   n_trt=n_trt,
        x_ctrl=x_ctrl,   x_trt=x_trt,
        rate_ctrl=rate_ctrl,   rate_trt=rate_trt,
        abs_uplift=abs_uplift, rel_uplift=rel_uplift,
        z_stat=z_stat,         p_value=p_value,
        ci_lower=ci_lower,     ci_upper=ci_upper,
        significant=p_value < alpha,
        alpha=alpha
    )


def print_ab_result(result):
    """
    Pretty-print an ABTestResult.
    格式化打印 A/B 测试结果。
    """
    sig_label = "SIGNIFICANT ✓" if result.significant else "not significant"
    direction = ""
    if result.significant:
        direction = " (treatment WORSE)" if result.abs_uplift < 0 else " (treatment BETTER)"

    print(f"Metric : {result.metric}")
    print(f"  Control   n={result.n_ctrl:,}   rate={result.rate_ctrl:.3%}")
    print(f"  Treatment n={result.n_trt:,}   rate={result.rate_trt:.3%}")
    print(f"  Abs uplift : {result.abs_uplift:+.4%}  |  Rel uplift : {result.rel_uplift:+.2%}")
    print(f"  Z-stat={result.z_stat:.4f}   p={result.p_value:.4f}   {sig_label}{direction}")
    print(f"  95% CI : [{result.ci_lower:+.4%},  {result.ci_upper:+.4%}]")
