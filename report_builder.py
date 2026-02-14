import json
import os
from datetime import datetime
from typing import Dict, Any

def generate_html_report(results: Dict[str, Any], 
                         stats: Dict[str, Any],
                         roi: Dict[str, Any],
                         output_path: str,
                         prompt_a: str = "",
                         prompt_b: str = "",
                         dataset_name: str = "",
                         model_name: str = "",
                         provider: str = "anthropic") -> str:
    """
    Generate a self-contained HTML report with embedded data and visualizations.
    
    Args:
        results: Results from PromptEvaluator
        stats: Statistical analysis results
        roi: ROI calculation results
        output_path: Path where the HTML file should be saved
        prompt_a: First prompt text
        prompt_b: Second prompt text
        dataset_name: Name of the dataset used
        model_name: Model name used for testing
        provider: LLM provider used
    
    Returns:
        Path to the generated HTML file
    """
    evaluation_results = results
    stats_results = stats
    roi_results = roi
    template_path = os.path.join(os.path.dirname(__file__), "templates", "report_template.html")
    
    with open(template_path, "r") as f:
        html_template = f.read()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    winner_class = "" if stats_results.get("significant", stats_results.get("is_significant", False)) else "no-diff"
    winner_label = "Prompt A" if stats_results["winner"] == "a" else "Prompt B"
    winner_text = f"🏆 Winner: {winner_label}"
    
    config_info = f"Provider: {provider} | Model: {model_name} | Dataset: {dataset_name}"
    if not stats_results["is_significant"]:
        winner_text = "📊 No Significant Difference Detected"
    
    detailed_results_html = ""
    for idx, (result_a, result_b) in enumerate(zip(
        evaluation_results["prompt_a"]["results"],
        evaluation_results["prompt_b"]["results"]
    )):
        detailed_results_html += f"""
        <div class="test-case">
            <div class="test-case-header">Test Case {idx + 1}: {result_a['input']}</div>
            <div class="response-comparison">
                <div class="response-box">
                    <h4 class="prompt-a">Prompt A Response</h4>
                    <div class="response-text">{result_a['response']}</div>
                    <div class="response-score prompt-a">Quality: {result_a['quality']:.1f}/10</div>
                    <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                        Time: {result_a['time']:.2f}s | Tokens: {result_a['total_tokens']} | Cost: ${result_a['cost']:.4f}
                    </div>
                </div>
                <div class="response-box">
                    <h4 class="prompt-b">Prompt B Response</h4>
                    <div class="response-text">{result_b['response']}</div>
                    <div class="response-score prompt-b">Quality: {result_b['quality']:.1f}/10</div>
                    <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                        Time: {result_b['time']:.2f}s | Tokens: {result_b['total_tokens']} | Cost: ${result_b['cost']:.4f}
                    </div>
                </div>
            </div>
        </div>
        """
    
    def convert_to_json_serializable(obj):
        """Convert numpy types to native Python types for JSON serialization."""
        if isinstance(obj, dict):
            return {k: convert_to_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_to_json_serializable(item) for item in obj]
        elif hasattr(obj, 'item'):
            return obj.item()
        elif isinstance(obj, bool):
            return bool(obj)
        elif isinstance(obj, (int, float)):
            return float(obj) if isinstance(obj, float) else int(obj)
        return obj
    
    test_data = {
        "metrics": {
            "quality_a": evaluation_results["prompt_a"]["avg_quality"],
            "quality_b": evaluation_results["prompt_b"]["avg_quality"],
            "time_a": evaluation_results["prompt_a"]["avg_time"],
            "time_b": evaluation_results["prompt_b"]["avg_time"],
            "tokens_a": evaluation_results["prompt_a"]["avg_tokens"],
            "tokens_b": evaluation_results["prompt_b"]["avg_tokens"],
            "cost_a": evaluation_results["prompt_a"]["avg_cost"],
            "cost_b": evaluation_results["prompt_b"]["avg_cost"]
        },
        "stats": stats_results,
        "roi": roi_results,
        "quality_scores_a": evaluation_results["prompt_a"]["quality_scores"],
        "quality_scores_b": evaluation_results["prompt_b"]["quality_scores"],
        "test_cases": evaluation_results["prompt_a"]["results"]
    }
    
    test_data_json = json.dumps(convert_to_json_serializable(test_data))
    
    replacements = {
        "{{TIMESTAMP}}": timestamp,
        "{{WINNER_CLASS}}": winner_class,
        "{{WINNER_TEXT}}": winner_text,
        "{{CONFIDENCE}}": f"{stats_results['confidence_pct']:.2f}",
        "{{P_VALUE}}": f"{stats_results['p_value']:.4f}",
        "{{EFFECT_SIZE}}": f"{stats_results['effect_size']:.3f}",
        "{{QUALITY_A}}": f"{evaluation_results['prompt_a']['avg_quality']:.2f}",
        "{{QUALITY_B}}": f"{evaluation_results['prompt_b']['avg_quality']:.2f}",
        "{{TIME_A}}": f"{evaluation_results['prompt_a']['avg_time']:.3f}",
        "{{TIME_B}}": f"{evaluation_results['prompt_b']['avg_time']:.3f}",
        "{{TOKENS_A}}": f"{evaluation_results['prompt_a']['avg_tokens']:.0f}",
        "{{TOKENS_B}}": f"{evaluation_results['prompt_b']['avg_tokens']:.0f}",
        "{{COST_A}}": f"{evaluation_results['prompt_a']['avg_cost']:.4f}",
        "{{COST_B}}": f"{evaluation_results['prompt_b']['avg_cost']:.4f}",
        "{{CHEAPER_PROMPT}}": roi_results["cheaper_prompt"],
        "{{COST_SAVINGS}}": f"{roi_results['cost_savings']:.2f}",
        "{{SAVINGS_PCT}}": f"{roi_results['savings_pct']:.2f}",
        "{{BETTER_VALUE}}": roi_results["better_value"],
        "{{DETAILED_RESULTS}}": detailed_results_html,
        "{{TEST_DATA_JSON}}": test_data_json
    }
    
    html_output = html_template
    for placeholder, value in replacements.items():
        html_output = html_output.replace(placeholder, str(value))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(html_output)
    
    return output_path