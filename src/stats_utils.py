import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import statsmodels.stats.power as power
import statsmodels.stats.proportion as prop

def proportion_difference_confidence_interval(p1, n1, p2, n2, confidence_level=0.95):
    """
    Computes the Wald confidence interval for the difference between two independent proportions: p2 - p1.
    
    Parameters:
    - p1 (float): Conversion rate of Group 1 (Control)
    - n1 (int): Sample size of Group 1
    - p2 (float): Conversion rate of Group 2 (Treatment)
    - n2 (int): Sample size of Group 2
    - confidence_level (float): The confidence level (default: 0.95)
    
    Returns:
    - lower_bound (float), upper_bound (float)
    """
    diff = p2 - p1
    se = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2))
    
    z_critical = stats.norm.ppf(1 - (1 - confidence_level) / 2)
    margin_of_error = z_critical * se
    
    return diff - margin_of_error, diff + margin_of_error

def bootstrap_ab_test(data, group_col, target_col, num_bootstrap_reps=10000, confidence_level=0.95, seed=42):
    """
    Performs bootstrap resampling to estimate the difference in conversion rates between two groups.
    
    Parameters:
    - data (DataFrame): The input dataset.
    - group_col (str): Column name for groups ('control' and 'treatment').
    - target_col (str): Column name for conversions (binary 0/1).
    - num_bootstrap_reps (int): Number of bootstrap iterations.
    - confidence_level (float): Confidence level for the interval.
    - seed (int): Seed for reproducibility.
    
    Returns:
    - diffs (ndarray): Array of simulated differences (p_treatment - p_control).
    - lower_ci (float): Lower confidence interval limit.
    - upper_ci (float): Upper confidence interval limit.
    - prob_treatment_better (float): The proportion of bootstrap replicates where treatment conversion > control.
    """
    np.random.seed(seed)
    
    control_vals = data[data[group_col] == 'control'][target_col].values
    treatment_vals = data[data[group_col] == 'treatment'][target_col].values
    
    n_control = len(control_vals)
    n_treatment = len(treatment_vals)
    
    # Pre-allocate array for results
    diffs = np.zeros(num_bootstrap_reps)
    
    for i in range(num_bootstrap_reps):
        boot_control = np.random.choice(control_vals, size=n_control, replace=True)
        boot_treatment = np.random.choice(treatment_vals, size=n_treatment, replace=True)
        
        diffs[i] = np.mean(boot_treatment) - np.mean(boot_control)
        
    alpha = 1 - confidence_level
    lower_ci = np.percentile(diffs, (alpha / 2) * 100)
    upper_ci = np.percentile(diffs, (1 - alpha / 2) * 100)
    
    prob_treatment_better = np.mean(diffs > 0)
    
    return diffs, lower_ci, upper_ci, prob_treatment_better

def plot_power_curve(baseline_conversion, significance_level=0.05, power_target=0.8, effect_sizes=None):
    """
    Plots a power curve displaying sample size required per group for various effect sizes (lifts).
    
    Parameters:
    - baseline_conversion (float): Conversion rate of the control group (e.g. 0.05).
    - significance_level (float): Alpha parameter (default 0.05).
    - power_target (float): Target power (default 0.8).
    - effect_sizes (list/array): List of absolute lifts to plot (e.g., [0.01, 0.02, 0.03]).
    """
    if effect_sizes is None:
        effect_sizes = np.linspace(0.005, 0.05, 100)
        
    analysis = power.NormalIndPower()
    
    sample_sizes = []
    for lift in effect_sizes:
        treatment_conversion = baseline_conversion + lift
        
        # Calculate Cohen's h for proportions
        h = prop.proportion_effectsize(treatment_conversion, baseline_conversion)
        
        # Calculate sample size for one-sided test (since our hypothesis is treatment > control)
        # We divide alpha by 2 for standard two-sided or specify alternative='larger' in power solver
        try:
            n = analysis.solve_power(effect_size=h, alpha=significance_level, power=power_target, ratio=1.0, alternative='larger')
            sample_sizes.append(n)
        except Exception:
            sample_sizes.append(np.nan)
            
    plt.figure(figsize=(10, 6))
    plt.plot(effect_sizes * 100, sample_sizes, color='#2ec4b6', linewidth=2.5, label='Required Sample Size')
    plt.axhline(y=10000, color='#ff9f1c', linestyle='--', label='Current Sample Size (10,000)')
    
    # Find required sample size for exactly 2% lift
    h_2pct = prop.proportion_effectsize(baseline_conversion + 0.02, baseline_conversion)
    n_2pct = analysis.solve_power(effect_size=h_2pct, alpha=significance_level, power=power_target, ratio=1.0, alternative='larger')
    
    plt.axvline(x=2.0, color='#e71d36', linestyle=':', label=f'MDE 2.0% (Req: {int(n_2pct):,})')
    plt.scatter([2.0], [n_2pct], color='#e71d36', zorder=5)
    
    plt.title('Power Analysis: Required Sample Size vs. Minimum Detectable Effect (MDE)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Minimum Detectable Effect (Absolute Lift %)', fontsize=12)
    plt.ylabel('Required Sample Size per Group', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(frameon=True, facecolor='white', edgecolor='none')
    plt.tight_layout()
    
    return plt.gcf()
