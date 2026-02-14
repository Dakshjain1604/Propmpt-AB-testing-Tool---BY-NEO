import os
from typing import Dict, List, Any, Optional
import time
from anthropic import Anthropic
from openai import OpenAI
import tiktoken

class PromptEvaluator:
    def __init__(self, provider: str = "anthropic", api_key: Optional[str] = None, 
                 model: Optional[str] = None, openai_api_key: Optional[str] = None,
                 openrouter_api_key: Optional[str] = None):
        """
        Initialize the evaluator with specified provider.
        
        Args:
            provider: API provider ('anthropic', 'openai', or 'openrouter')
            api_key: Anthropic API key (for backward compatibility)
            model: Model name to use
            openai_api_key: OpenAI API key
            openrouter_api_key: OpenRouter API key
        """
        self.provider = provider.lower()
        
        if self.provider == "anthropic":
            if not api_key:
                raise ValueError("Anthropic API key required for provider 'anthropic'")
            self.client = Anthropic(api_key=api_key)
            self.model = model or "claude-sonnet-4-20250514"
            self.input_token_price = 3.00 / 1_000_000
            self.output_token_price = 15.00 / 1_000_000
            
        elif self.provider == "openai":
            if not openai_api_key:
                raise ValueError("OpenAI API key required for provider 'openai'")
            self.client = OpenAI(api_key=openai_api_key)
            self.model = model or "gpt-4o"
            self.input_token_price = 2.50 / 1_000_000
            self.output_token_price = 10.00 / 1_000_000
            
        elif self.provider == "openrouter":
            if not openrouter_api_key:
                raise ValueError("OpenRouter API key required for provider 'openrouter'")
            self.client = OpenAI(
                api_key=openrouter_api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            self.model = model or "openai/gpt-4o"
            self.input_token_price = 2.50 / 1_000_000
            self.output_token_price = 10.00 / 1_000_000
            
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'anthropic', 'openai', or 'openrouter'")
    
    def execute_prompt(self, prompt_template: str, input_text: str) -> Dict[str, Any]:
        """
        Execute a prompt with given input and measure metrics.
        
        Args:
            prompt_template: Prompt template with {input} placeholder
            input_text: Input text to substitute
        
        Returns:
            Dictionary with response, time, tokens, and cost
        """
        prompt = prompt_template.replace("{input}", input_text)
        
        start_time = time.time()
        
        if self.provider == "anthropic":
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            response_text = message.content[0].text
            input_tokens = message.usage.input_tokens
            output_tokens = message.usage.output_tokens
            
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            response_text = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
        
        end_time = time.time()
        response_time = end_time - start_time
        
        total_tokens = input_tokens + output_tokens
        cost = (input_tokens * self.input_token_price) + (output_tokens * self.output_token_price)
        
        return {
            "response": response_text,
            "time": response_time,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost": cost
        }
    
    def judge_quality(self, input_text: str, response: str) -> float:
        """
        Use LLM to judge the quality of a response on a 1-10 scale.
        
        Args:
            input_text: Original input/question
            response: Response to evaluate
        
        Returns:
            Quality score from 1-10
        """
        judge_prompt = f"""You are an expert evaluator. Rate the following response on a scale of 1-10 based on:
- Relevance to the input
- Completeness
- Clarity
- Accuracy
- Usefulness

Input: {input_text}

Response: {response}

Provide ONLY a single number between 1 and 10 as your rating. Do not include any other text."""

        try:
            if self.provider == "anthropic":
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=10,
                    messages=[
                        {"role": "user", "content": judge_prompt}
                    ]
                )
                score_text = message.content[0].text.strip()
            else:
                response_obj = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=10,
                    messages=[
                        {"role": "user", "content": judge_prompt}
                    ]
                )
                score_text = response_obj.choices[0].message.content.strip()
            
            score = float(score_text)
            score = max(1.0, min(10.0, score))
            return score
        except (ValueError, IndexError, AttributeError):
            return 5.0
    
    def evaluate_prompts(self, prompt_a: str, prompt_b: str, 
                        dataset: List[Dict[str, str]], 
                        progress_callback=None) -> Dict[str, Any]:
        """
        Evaluate two prompts on a dataset.
        
        Args:
            prompt_a: First prompt template
            prompt_b: Second prompt template
            dataset: List of test cases with 'input' field
            progress_callback: Optional callback function for progress updates
        
        Returns:
            Dictionary with detailed results for both prompts
        """
        results_a = []
        results_b = []
        
        total_tests = len(dataset)
        
        for idx, test_case in enumerate(dataset):
            input_text = test_case["input"]
            
            result_a = self.execute_prompt(prompt_a, input_text)
            quality_a = self.judge_quality(input_text, result_a["response"])
            result_a["quality"] = quality_a
            result_a["input"] = input_text
            results_a.append(result_a)
            
            result_b = self.execute_prompt(prompt_b, input_text)
            quality_b = self.judge_quality(input_text, result_b["response"])
            result_b["quality"] = quality_b
            result_b["input"] = input_text
            results_b.append(result_b)
            
            if progress_callback:
                progress_callback(idx + 1, total_tests)
        
        avg_quality_a = sum(r["quality"] for r in results_a) / len(results_a)
        avg_time_a = sum(r["time"] for r in results_a) / len(results_a)
        avg_tokens_a = sum(r["total_tokens"] for r in results_a) / len(results_a)
        avg_cost_a = sum(r["cost"] for r in results_a) / len(results_a)
        
        avg_quality_b = sum(r["quality"] for r in results_b) / len(results_b)
        avg_time_b = sum(r["time"] for r in results_b) / len(results_b)
        avg_tokens_b = sum(r["total_tokens"] for r in results_b) / len(results_b)
        avg_cost_b = sum(r["cost"] for r in results_b) / len(results_b)
        
        return {
            "prompt_a": {
                "results": results_a,
                "avg_quality": avg_quality_a,
                "avg_time": avg_time_a,
                "avg_tokens": avg_tokens_a,
                "avg_cost": avg_cost_a,
                "quality_scores": [r["quality"] for r in results_a]
            },
            "prompt_b": {
                "results": results_b,
                "avg_quality": avg_quality_b,
                "avg_time": avg_time_b,
                "avg_tokens": avg_tokens_b,
                "avg_cost": avg_cost_b,
                "quality_scores": [r["quality"] for r in results_b]
            }
        }