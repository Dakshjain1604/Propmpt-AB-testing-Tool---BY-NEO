import scipy.stats as stats
import numpy as np
from typing import List, Dict, Any

def calculate_statistics(prompt_a_scores: List[float], prompt_b_scores: List[float]) -> Dict[str, Any]:
    """
    Perform statistical analysis comparing two sets of quality scores.
    
    Args:
        prompt_a_scores: List of quality scores (1-10) for Prompt A
        prompt_b_scores: List of quality scores (1-10) for Prompt B
    
    Returns:
        Dictionary containing statistical metrics including p-value, confidence, winner, etc.
    """
    if len(prompt_a_scores) == 0 or len(prompt_b_scores) == 0:
        raise ValueError("Score lists cannot be empty")
    
    prompt_a_array = np.array(prompt_a_scores)
    prompt_b_array = np.array(prompt_b_scores)
    
    t_statistic, p_value = stats.ttest_ind(prompt_a_array, prompt_b_array)
    
    mean_a = np.mean(prompt_a_array)
    mean_b = np.mean(prompt_b_array)
    std_a = np.std(prompt_a_array, ddof=1)
    std_b = np.std(prompt_b_array, ddof=1)
    
    pooled_std = np.sqrt(((len(prompt_a_array) - 1) * std_a**2 + (len(prompt_b_array) - 1) * std_b**2) / 
                         (len(prompt_a_array) + len(prompt_b_array) - 2))
    cohens_d = (mean_a - mean_b) / pooled_std if pooled_std != 0 else 0
    
    is_significant = p_value < 0.05
    
    if is_significant:
        if mean_a > mean_b:
            winner = "Prompt A"
            confidence = (1 - p_value) * 100
            improvement = ((mean_a - mean_b) / mean_b) * 100
        else:
            winner = "Prompt B"
            confidence = (1 - p_value) * 100
            improvement = ((mean_b - mean_a) / mean_a) * 100
    else:
        winner = "No significant difference"
        confidence = 0
        improvement = 0
    
    stderr_a = std_a / np.sqrt(len(prompt_a_array))
    stderr_b = std_b / np.sqrt(len(prompt_b_array))
    ci_95_a = (mean_a - 1.96 * stderr_a, mean_a + 1.96 * stderr_a)
    ci_95_b = (mean_b - 1.96 * stderr_b, mean_b + 1.96 * stderr_b)
    
    return {
        "winner": winner,
        "p_value": p_value,
        "confidence_pct": confidence,
        "is_significant": is_significant,
        "mean_a": mean_a,
        "mean_b": mean_b,
        "std_a": std_a,
        "std_b": std_b,
        "effect_size": cohens_d,
        "improvement_pct": improvement,
        "ci_95_a": ci_95_a,
        "ci_95_b": ci_95_b,
        "t_statistic": t_statistic,
        "sample_size": len(prompt_a_array)
    }

def calculate_roi(cost_a: float, cost_b: float, quality_a: float, quality_b: float, 
                  num_requests: int = 100000) -> Dict[str, Any]:
    """
    Calculate ROI and cost savings at scale.
    
    Args:
        cost_a: Average cost per request for Prompt A
        cost_b: Average cost per request for Prompt B
        quality_a: Average quality score for Prompt A
        quality_b: Average quality score for Prompt B
        num_requests: Number of requests to project (default 100k)
    
    Returns:
        Dictionary with cost analysis
    """
    total_cost_a = cost_a * num_requests
    total_cost_b = cost_b * num_requests
    cost_savings = total_cost_a - total_cost_b
    
    quality_per_dollar_a = quality_a / cost_a if cost_a > 0 else 0
    quality_per_dollar_b = quality_b / cost_b if cost_b > 0 else 0
    
    if cost_savings > 0:
        cheaper_prompt = "Prompt B"
        savings_pct = (cost_savings / total_cost_a) * 100
    elif cost_savings < 0:
        cheaper_prompt = "Prompt A"
        savings_pct = (abs(cost_savings) / total_cost_b) * 100
        cost_savings = abs(cost_savings)
    else:
        cheaper_prompt = "Equal"
        savings_pct = 0
    
    if quality_per_dollar_a > quality_per_dollar_b:
        better_value = "Prompt A"
    elif quality_per_dollar_b > quality_per_dollar_a:
        better_value = "Prompt B"
    else:
        better_value = "Equal"
    
    return {
        "cheaper_prompt": cheaper_prompt,
        "cost_savings": abs(cost_savings),
        "savings_pct": savings_pct,
        "total_cost_a": total_cost_a,
        "total_cost_b": total_cost_b,
        "quality_per_dollar_a": quality_per_dollar_a,
        "quality_per_dollar_b": quality_per_dollar_b,
        "better_value": better_value,
        "num_requests": num_requests
    }