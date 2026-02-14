# Neo Prompt Tester 🧪

Scientific A/B Testing for AI Prompts - Compare two prompts with statistical rigor and beautiful reports.

## Features

- **Interactive & CLI Modes**: Run interactively or with command-line arguments
- **Statistical Analysis**: T-tests, p-values, confidence intervals, effect sizes
- **Quality Scoring**: LLM-as-judge evaluation (1-10 scale)
- **Performance Metrics**: Response time, token count, cost analysis
- **Beautiful Reports**: Self-contained HTML with Chart.js visualizations
- **ROI Calculations**: Cost savings projections at scale
- **Built-in Datasets**: Customer support, code tasks, creative prompts

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file with your API key(s):

```bash
cp .env.example .env
# Edit .env and add your key(s):
# ANTHROPIC_API_KEY=your_anthropic_key_here
# OPENAI_API_KEY=your_openai_key_here
# OPENROUTER_API_KEY=your_openrouter_key_here
```

**Supported Providers:**
- **Anthropic** (default): Claude models - `claude-sonnet-4-20250514`
- **OpenAI**: GPT models - `gpt-4o` (default)
- **OpenRouter**: Access to various models via unified API

### 3. Run a Test

**Interactive Mode:**
```bash
python neo_test.py
```

**Example 1: Testing Customer Support Tone (Anthropic - default):**
```bash
python neo_test.py \
  --prompt-a "You are a helpful customer support agent. Provide a clear, professional response to: {input}. Be empathetic, address the concern directly, and provide actionable next steps." \
  --prompt-b "As a friendly customer support specialist, help with: {input}. Use a warm, conversational tone while providing a helpful solution." \
  --dataset customer_support \
  --output ./results/tone_test.html
```

**Example 2: Testing Response Length (OpenAI):**
```bash
python neo_test.py \
  --provider openai \
  --prompt-a "Customer inquiry: {input}. Provide a concise, efficient solution in 2-3 sentences." \
  --prompt-b "Customer request: {input}. Provide a thorough response with: 1) Acknowledgment 2) Detailed solution 3) Follow-up steps." \
  --dataset customer_support
```

**Example 3: Testing Code Generation Approaches (OpenRouter):**
```bash
python neo_test.py \
  --provider openrouter \
  --model "anthropic/claude-3.5-sonnet" \
  --prompt-a "Write clean, production-ready code for: {input}. Include error handling and comments." \
  --prompt-b "Solve this coding task: {input}. Provide a simple, straightforward solution with explanations." \
  --dataset code_tasks
```

**Example 4: Testing Empathy vs Efficiency:**
```bash
python neo_test.py \
  --prompt-a "A customer needs help with: {input}. Respond with empathy and understanding, then provide the best solution." \
  --prompt-b "Customer question: {input}. Provide a direct, actionable solution with clear next steps." \
  --dataset customer_support
```

**Example 5: Testing Structured vs Freeform Responses:**
```bash
python neo_test.py \
  --provider openai \
  --model "gpt-4o" \
  --prompt-a "Task: {input}. Respond in this format: 1) Summary 2) Solution 3) Recommendation" \
  --prompt-b "Here's a task: {input}. Provide your best response in a natural, conversational way." \
  --dataset code_tasks
```

**Example 6: Testing Creative Writing Styles:**
```bash
python neo_test.py \
  --prompt-a "Write a creative response to: {input}. Be imaginative, vivid, and engaging with rich descriptions." \
  --prompt-b "Create content for: {input}. Keep it clear, concise, and punchy with short sentences." \
  --dataset creative_prompts
```

**Custom Model:**
```bash
python neo_test.py \
  --provider openai \
  --model "gpt-4-turbo" \
  --prompt-a "Answer: {input}" \
  --prompt-b "Response: {input}"
```

## Usage

### Prompt Format

Prompts must include `{input}` placeholder for variable substitution:

```
Good: "Answer the following question concisely: {input}"
Bad: "Answer the following question concisely"
```

### Built-in Datasets

- `customer_support` - 20 customer service questions
- `code_tasks` - 20 programming tasks
- `creative_prompts` - 20 creative writing prompts

### Custom Datasets

Use JSON format with `input` field:

```json
[
  {"input": "Your test case 1"},
  {"input": "Your test case 2"}
]
```

Then reference the file path:
```bash
python neo_test.py --dataset ./my_dataset.json
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--prompt-a` | First prompt (text or file path) | Interactive prompt |
| `--prompt-b` | Second prompt (text or file path) | Interactive prompt |
| `--dataset` | Dataset name or path | `customer_support` |
| `--output` | Output path for HTML report | `./results/report.html` |
| `--provider` | API provider (anthropic/openai/openrouter) | `anthropic` |
| `--model` | Model to use | Provider-specific default |

## Prompt Engineering Tips

### What Makes a Good Test?

**✅ Good A/B Tests:**
- Test one variable at a time (tone, length, structure, specificity)
- Use clear, measurable differences between prompts
- Test hypotheses like "Does adding examples improve code quality?"

**❌ Poor A/B Tests:**
- Changing multiple variables at once
- Vague or minimal differences between prompts
- Testing "Answer: {input}" vs "Response: {input}" (no meaningful difference)

### Common Test Scenarios

1. **Tone Testing**: Professional vs Casual, Empathetic vs Direct
2. **Length Testing**: Concise vs Detailed, Bullet points vs Paragraphs
3. **Structure Testing**: Freeform vs Formatted, Step-by-step vs Summary
4. **Specificity Testing**: General instructions vs Detailed requirements
5. **Context Testing**: Minimal context vs Rich background information
6. **Role Testing**: Different persona descriptions or expertise levels

## Output

The tool generates:

1. **Terminal Output**: Color-coded results with progress bar
2. **HTML Report**: Self-contained file with:
   - Winner announcement with statistical significance
   - Metrics comparison table
   - Interactive Chart.js visualizations
   - Quality scores line chart
   - Detailed test results (expandable)
   - ROI analysis with cost savings
   - Export to PDF and Markdown

## Statistical Analysis

The tool performs:

- **Independent samples t-test** to compare quality scores
- **P-value calculation** (significance threshold: 0.05)
- **Effect size** (Cohen's d)
- **Confidence intervals** (95%)
- **Percentage improvement** calculations

## Metrics Tracked

For each prompt:

- **Quality Score**: 1-10 rating by Claude (LLM-as-judge)
- **Response Time**: Seconds per request
- **Token Count**: Input + output tokens
- **Cost**: Based on Anthropic pricing (input: $3/M, output: $15/M)

## Example Results

```
📊 Test Results Summary
┌─────────────────────┬───────────┬───────────┐
│ Metric              │ Prompt A  │ Prompt B  │
├─────────────────────┼───────────┼───────────┤
│ Quality Score       │ 8.45      │ 7.82      │
│ Response Time (s)   │ 1.234     │ 1.456     │
│ Tokens/Response     │ 245       │ 312       │
│ Cost/Response ($)   │ 0.0042    │ 0.0051    │
└─────────────────────┴───────────┴───────────┘

🏆 Winner: Prompt A
Confidence: 97.45%
p-value: 0.0255
Quality Improvement: 8.06%
```

## Project Structure

```
neo-prompt-tester/
├── neo_test.py              # Main CLI entry point
├── evaluator.py             # Test engine with API integration
├── report_builder.py        # HTML report generation
├── stats_calculator.py      # Statistical analysis
├── datasets/                # Built-in test datasets
│   ├── customer_support.json
│   ├── code_tasks.json
│   └── creative_prompts.json
├── templates/
│   └── report_template.html # HTML template
├── results/                 # Generated reports
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- API key (Anthropic/OpenAI/OpenRouter)
- Dependencies (see requirements.txt)

## License

MIT

## Contributing

Contributions welcome! Please open an issue or PR.

## Support

For issues or questions, please open a GitHub issue.