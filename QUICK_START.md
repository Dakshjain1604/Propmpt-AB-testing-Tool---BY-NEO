# Quick Start Guide - Neo Prompt Tester with Multi-Provider Support

## Prerequisites

1. Python 3.8+ installed
2. Virtual environment activated
3. Valid API key for at least one provider

## Setup

### 1. Activate Virtual Environment

```bash
cd /root/promptABtesting
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### 2. Set API Key

Choose one provider and set its API key:

**Option A: Anthropic (Claude)**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

**Option B: OpenAI (GPT)**
```bash
export OPENAI_API_KEY="sk-..."
```

**Option C: OpenRouter**
```bash
export OPENROUTER_API_KEY="sk-or-..."
```

Alternatively, add to `.env` file:
```bash
cp .env.example .env
# Edit .env and add your key
```

## Usage

### Interactive Mode

Simply run:
```bash
python neo_test.py
```

You'll be prompted for:
1. Prompt A (text or file path)
2. Prompt B (text or file path)
3. Dataset choice (customer_support, code_tasks, creative_prompts, or custom path)
4. Output path (optional)

### Direct Mode

#### Using Anthropic (Default)

```bash
python neo_test.py \
  --prompt-a "Please provide a helpful answer: {input}" \
  --prompt-b "Here is a detailed response: {input}" \
  --dataset customer_support \
  --output ./results/my_test.html
```

#### Using OpenAI

```bash
python neo_test.py \
  --provider openai \
  --prompt-a "Answer this: {input}" \
  --prompt-b "Respond to: {input}" \
  --dataset code_tasks
```

#### Using OpenRouter

```bash
python neo_test.py \
  --provider openrouter \
  --model "anthropic/claude-3.5-sonnet" \
  --prompt-a "Provide answer: {input}" \
  --prompt-b "Give response: {input}" \
  --dataset creative_prompts
```

#### Custom Model

```bash
python neo_test.py \
  --provider openai \
  --model "gpt-4-turbo" \
  --prompt-a "Answer: {input}" \
  --prompt-b "Response: {input}"
```

## Built-in Datasets

1. **customer_support** - 20 customer service scenarios
2. **code_tasks** - 20 programming challenges  
3. **creative_prompts** - 20 creative writing tasks

## Custom Dataset

Create a JSON file with this structure:

```json
[
  {"input": "Your first test case"},
  {"input": "Your second test case"},
  ...
]
```

Then use it:
```bash
python neo_test.py \
  --prompt-a "..." \
  --prompt-b "..." \
  --dataset /path/to/your/dataset.json
```

## Viewing Results

After the test completes:

1. **Terminal**: Shows summary statistics and winner
2. **HTML Report**: Automatically opens in browser
   - Located at `./results/report.html` (or your specified path)
   - Self-contained - can be shared/viewed offline
   - Contains charts, detailed results, and statistical analysis

## Troubleshooting

### "API key required" error

Make sure you've set the correct environment variable:
```bash
echo $ANTHROPIC_API_KEY  # Should show your key
echo $OPENAI_API_KEY
echo $OPENROUTER_API_KEY
```

### "Module not found" error

Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### "Authentication error" (401)

Your API key is invalid or expired. Get a new key from:
- Anthropic: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/api-keys
- OpenRouter: https://openrouter.ai/keys

## Examples

### Example 1: Test customer support prompts with Anthropic

```bash
export ANTHROPIC_API_KEY="your-key"

python neo_test.py \
  --prompt-a "Provide a concise answer: {input}" \
  --prompt-b "Give a detailed, empathetic response: {input}" \
  --dataset customer_support
```

### Example 2: Test code generation with OpenAI

```bash
export OPENAI_API_KEY="your-key"

python neo_test.py \
  --provider openai \
  --prompt-a "Write Python code for: {input}" \
  --prompt-b "Create a Python function that: {input}" \
  --dataset code_tasks \
  --output ./results/code_comparison.html
```

### Example 3: Test creative writing with OpenRouter

```bash
export OPENROUTER_API_KEY="your-key"

python neo_test.py \
  --provider openrouter \
  --model "anthropic/claude-3.5-sonnet" \
  --prompt-a "Write creatively about: {input}" \
  --prompt-b "Compose an artistic piece on: {input}" \
  --dataset creative_prompts
```

## Understanding Results

The HTML report includes:

1. **Winner Announcement**: Which prompt performed better (if statistically significant)
2. **Summary Table**: Average quality, time, tokens, cost for each prompt
3. **Charts**: 
   - Bar chart comparing all 4 metrics
   - Line chart showing quality scores across test cases
4. **Statistical Analysis**: p-value, confidence level, effect size
5. **ROI Calculation**: Projected cost savings at scale (100k requests)
6. **Detailed Results**: Individual responses and scores for each test case

## Tips

- Use `{input}` placeholder in your prompts - it gets replaced with test cases
- Start with built-in datasets to learn the tool
- Longer, more detailed prompts often score higher but cost more
- Run at least 15-20 test cases for reliable statistical significance
- Compare similar prompt styles (both short, or both detailed)

## Support

For issues or questions:
1. Check `DELIVERABLES_STATUS.md` for implementation details
2. Review `MULTI_PROVIDER_IMPLEMENTATION.md` for architecture
3. See `README.md` for comprehensive documentation