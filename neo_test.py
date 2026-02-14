import click
import json
import os
import webbrowser
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
from rich import box
from dotenv import load_dotenv

from evaluator import PromptEvaluator
from stats_calculator import calculate_statistics, calculate_roi
from report_builder import generate_html_report

load_dotenv()

console = Console()

def load_dataset(dataset_name: str) -> list:
    """Load a dataset from file."""
    if not dataset_name.endswith('.json'):
        dataset_path = os.path.join(os.path.dirname(__file__), "datasets", f"{dataset_name}.json")
    else:
        dataset_path = dataset_name
    
    if not os.path.exists(dataset_path):
        console.print(f"[red]Error: Dataset not found at {dataset_path}[/red]")
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    
    with open(dataset_path, "r") as f:
        return json.load(f)

def load_prompt(prompt_input: str) -> str:
    """Load prompt from file or return as-is if it's text."""
    if os.path.exists(prompt_input):
        with open(prompt_input, "r") as f:
            return f.read()
    return prompt_input

@click.command()
@click.option("--prompt-a", help="First prompt (text or file path)")
@click.option("--prompt-b", help="Second prompt (text or file path)")
@click.option("--dataset", default="customer_support", help="Dataset name or path (default: customer_support)")
@click.option("--output", default="./results/report.html", help="Output path for HTML report")
@click.option("--provider", default="anthropic", type=click.Choice(['anthropic', 'openai', 'openrouter'], case_sensitive=False), 
              help="LLM provider to use (default: anthropic)")
@click.option("--model", help="Model name (defaults based on provider)")
@click.option("--anthropic-api-key", help="Anthropic API key (or use ANTHROPIC_API_KEY env var)")
@click.option("--openai-api-key", help="OpenAI API key (or use OPENAI_API_KEY env var)")
@click.option("--openrouter-api-key", help="OpenRouter API key (or use OPENROUTER_API_KEY env var)")
def main(prompt_a, prompt_b, dataset, output, provider, model, anthropic_api_key, openai_api_key, openrouter_api_key):
    """
    Neo Prompt Tester - Scientific A/B Testing for AI Prompts
    
    Test two prompts against a dataset and generate a comprehensive HTML report.
    
    Supports multiple LLM providers:
    - anthropic: Claude models (default: claude-sonnet-4-20250514)
    - openai: GPT models (default: gpt-4o)
    - openrouter: Access various models (default: openai/gpt-4o)
    """
    console.print(Panel.fit(
        "[bold cyan]🧪 Neo Prompt Tester[/bold cyan]\n"
        "[dim]Scientific A/B Testing for AI Prompts[/dim]",
        border_style="cyan"
    ))
    
    if not prompt_a or not prompt_b:
        console.print("\n[yellow]Interactive Mode[/yellow]\n")
        
        console.print("[bold]Enter Prompt A[/bold] (can be text or file path):")
        prompt_a = console.input("[cyan]> [/cyan]")
        
        console.print("\n[bold]Enter Prompt B[/bold] (can be text or file path):")
        prompt_b = console.input("[cyan]> [/cyan]")
        
        console.print("\n[bold]Choose dataset[/bold] (customer_support, code_tasks, creative_prompts, or path):")
        console.print("[dim]Press Enter for default (customer_support)[/dim]")
        dataset_input = console.input("[cyan]> [/cyan]")
        if dataset_input:
            dataset = dataset_input
        
        console.print("\n[bold]Output path[/bold] (default: ./results/report.html):")
        console.print("[dim]Press Enter for default[/dim]")
        output_input = console.input("[cyan]> [/cyan]")
        if output_input:
            output = output_input
    
    anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
    openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
    openrouter_api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
    
    if provider == "anthropic" and not anthropic_api_key:
        console.print("[red]Error: Anthropic API key required. Set ANTHROPIC_API_KEY environment variable or use --anthropic-api-key[/red]")
        return
    elif provider == "openai" and not openai_api_key:
        console.print("[red]Error: OpenAI API key required. Set OPENAI_API_KEY environment variable or use --openai-api-key[/red]")
        return
    elif provider == "openrouter" and not openrouter_api_key:
        console.print("[red]Error: OpenRouter API key required. Set OPENROUTER_API_KEY environment variable or use --openrouter-api-key[/red]")
        return
    
    console.print("\n")
    
    try:
        prompt_a_text = load_prompt(prompt_a)
        prompt_b_text = load_prompt(prompt_b)
        dataset_data = load_dataset(dataset)
        
        if "{input}" not in prompt_a_text or "{input}" not in prompt_b_text:
            console.print("[yellow]Warning: Prompts should contain {input} placeholder for variable substitution[/yellow]")
        
        console.print(f"[green]✓[/green] Loaded prompts")
        console.print(f"[green]✓[/green] Loaded dataset: {len(dataset_data)} test cases")
        console.print(f"[green]✓[/green] Using provider: {provider}")
        
        evaluator = PromptEvaluator(
            provider=provider,
            api_key=anthropic_api_key,
            model=model,
            openai_api_key=openai_api_key,
            openrouter_api_key=openrouter_api_key
        )
        
        console.print(f"[green]✓[/green] Using model: {evaluator.model}\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task(
                f"[cyan]Testing prompts on {len(dataset_data)} cases...", 
                total=len(dataset_data)
            )
            
            def update_progress(current, total):
                progress.update(task, completed=current)
            
            results = evaluator.evaluate_prompts(
                prompt_a_text, 
                prompt_b_text, 
                dataset_data,
                progress_callback=update_progress
            )
        
        console.print("\n[green]✓[/green] Evaluation complete!\n")
        
        stats = calculate_statistics(
            results["prompt_a"]["quality_scores"],
            results["prompt_b"]["quality_scores"]
        )
        
        roi = calculate_roi(
            results["prompt_a"]["avg_cost"],
            results["prompt_b"]["avg_cost"],
            results["prompt_a"]["avg_quality"],
            results["prompt_b"]["avg_quality"],
            num_requests=100000
        )
        
        table = Table(title="Test Results Summary", box=box.ROUNDED)
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Prompt A", style="magenta")
        table.add_column("Prompt B", style="yellow")
        table.add_column("Difference", style="green")
        
        quality_diff = ((results["prompt_a"]["avg_quality"] - results["prompt_b"]["avg_quality"]) 
                       / results["prompt_b"]["avg_quality"] * 100)
        time_diff = ((results["prompt_a"]["avg_time"] - results["prompt_b"]["avg_time"]) 
                    / results["prompt_b"]["avg_time"] * 100)
        tokens_diff = ((results["prompt_a"]["avg_tokens"] - results["prompt_b"]["avg_tokens"]) 
                      / results["prompt_b"]["avg_tokens"] * 100)
        cost_diff = ((results["prompt_a"]["avg_cost"] - results["prompt_b"]["avg_cost"]) 
                    / results["prompt_b"]["avg_cost"] * 100)
        
        table.add_row(
            "Quality Score",
            f"{results['prompt_a']['avg_quality']:.2f}/10",
            f"{results['prompt_b']['avg_quality']:.2f}/10",
            f"{quality_diff:+.1f}%"
        )
        table.add_row(
            "Response Time",
            f"{results['prompt_a']['avg_time']:.3f}s",
            f"{results['prompt_b']['avg_time']:.3f}s",
            f"{time_diff:+.1f}%"
        )
        table.add_row(
            "Tokens/Response",
            f"{results['prompt_a']['avg_tokens']:.0f}",
            f"{results['prompt_b']['avg_tokens']:.0f}",
            f"{tokens_diff:+.1f}%"
        )
        table.add_row(
            "Cost/Response",
            f"${results['prompt_a']['avg_cost']:.6f}",
            f"${results['prompt_b']['avg_cost']:.6f}",
            f"{cost_diff:+.1f}%"
        )
        
        console.print(table)
        console.print()
        
        winner = "Prompt A" if stats["winner"] == "a" else "Prompt B"
        winner_style = "magenta" if stats["winner"] == "a" else "yellow"
        
        if stats["is_significant"]:
            console.print(Panel.fit(
                f"[bold {winner_style}]🏆 Winner: {winner}[/bold {winner_style}]\n"
                f"[green]Confidence: {stats['confidence_pct']:.1f}%[/green]\n"
                f"[dim]p-value: {stats['p_value']:.4f} (statistically significant)[/dim]",
                border_style=winner_style
            ))
        else:
            console.print(Panel.fit(
                f"[yellow]No statistically significant difference[/yellow]\n"
                f"[dim]p-value: {stats['p_value']:.4f}[/dim]\n"
                f"[dim]Both prompts perform similarly[/dim]",
                border_style="yellow"
            ))
        
        console.print()
        
        os.makedirs(os.path.dirname(output) or "./results", exist_ok=True)
        
        generate_html_report(
            results=results,
            stats=stats,
            roi=roi,
            output_path=output,
            prompt_a=prompt_a_text,
            prompt_b=prompt_b_text,
            dataset_name=dataset,
            model_name=evaluator.model,
            provider=provider
        )
        
        console.print(f"[green]✓[/green] Report generated: {output}")
        
        try:
            webbrowser.open(f"file://{os.path.abspath(output)}")
            console.print("[green]✓[/green] Report opened in browser\n")
        except:
            console.print("[yellow]![/yellow] Could not open browser automatically\n")
        
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()