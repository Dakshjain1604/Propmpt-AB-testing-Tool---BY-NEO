# 🧪 Neo Prompt Tester

<div align="center">

**Scientific A/B Testing for AI Prompts - Compare prompts with statistical rigor and beautiful reports**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Features](#-features) • [Quick Start](#-quick-start) • [Examples](#-usage-examples) • [Documentation](#-documentation)

</div>

---

## 🎯 Overview

**Neo Prompt Tester** is a scientific toolkit for evaluating and comparing AI prompts through rigorous A/B testing. Get statistically significant results with confidence intervals, effect sizes, and beautiful HTML reports - all from the command line.

### Why Neo Prompt Tester?

- **📊 Statistical Rigor** - T-tests, p-values, confidence intervals, and effect sizes
- **🎨 Beautiful Reports** - Self-contained HTML with interactive Chart.js visualizations  
- **⚡ Multi-Provider** - Support for Anthropic, OpenAI, and OpenRouter
- **💰 ROI Analysis** - Cost savings projections at scale
- **🔬 LLM-as-Judge** - Quality scoring on 1-10 scale with detailed reasoning
- **📈 Performance Metrics** - Response time, token count, and cost tracking

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Interactive & CLI Modes** | Run interactively or with command-line arguments |
| **Statistical Analysis** | Independent t-tests with p-values and effect sizes (Cohen's d) |
| **Quality Scoring** | LLM-as-judge evaluation with 1-10 scoring |
| **Performance Metrics** | Response time, token count, and cost per request |
| **Beautiful Reports** | Self-contained HTML with Chart.js visualizations |
| **ROI Calculations** | Cost savings projections at scale |
| **Built-in Datasets** | Customer support, code tasks, creative prompts |

### Supported Providers

```
🤖 Anthropic    → Claude models (default: claude-sonnet-4-20250514)
🧠 OpenAI       → GPT models (default: gpt-4o)  
🌐 OpenRouter   → Unified API for various models
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- API key from at least one provider (Anthropic/OpenAI/OpenRouter)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd neo-prompt-tester

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add your API key(s)
```

### Your First Test

**Interactive Mode:**
```bash
python neo_test.py
```

**Command Line Mode:**
```bash
python neo_test.py \
  --prompt-a "You are a helpful customer support agent. Provide a clear, professional response to: {input}. Be empathetic and actionable." \
  --prompt-b "As a friendly support specialist, help with: {input}. Use a warm, conversational tone." \
  --dataset customer_support \
  --output ./results/tone_test.html
```

---

## 📚 Usage Examples

### Example 1: Testing Customer Support Tone (Anthropic)

```bash
python neo_test.py \
  --prompt-a "You are a helpful customer support agent. Provide a clear, professional response to: {input}. Be empathetic, address the concern directly, and provide actionable next steps." \
  --prompt-b "As a friendly customer support specialist, help with: {input}. Use a warm, conversational tone while providing a helpful solution." \
  --dataset customer_support \
  --output ./results/tone_test.html
```

**What This Tests:** Professional vs. conversational tone in customer support

---

### Example 2: Testing Response Length (OpenAI)

```bash
python neo_test.py \
  --provider openai \
  --prompt-a "Customer inquiry: {input}. Provide a concise, efficient solution in 2-3 sentences." \
  --prompt-b "Customer request: {input}. Provide a thorough response with: 1) Acknowledgment 2) Detailed solution 3) Follow-up steps." \
  --dataset customer_support
```

**What This Tests:** Concise vs. detailed responses for customer queries

---

### Example 3: Testing Code Generation Approaches (OpenRouter)

```bash
python neo_test.py \
  --provider openrouter \
  --model "anthropic/claude-3.5-sonnet" \
  --prompt-a "Write clean, production-ready code for: {input}. Include error handling and comments." \
  --prompt-b "Solve this coding task: {input}. Provide a simple, straightforward solution with explanations." \
  --dataset code_tasks
```

**What This Tests:** Production-ready vs. simple code solutions

---

### Example 4: Testing Empathy vs Efficiency

```bash
python neo_test.py \
  --prompt-a "A customer needs help with: {input}. Respond with empathy and understanding, then provide the best solution." \
  --prompt-b "Customer question: {input}. Provide a direct, actionable solution with clear next steps." \
  --dataset customer_support
```

**What This Tests:** Empathetic approach vs. direct efficiency

---

### Example 5: Testing Structured vs Freeform Responses

```bash
python neo_test.py \
  --provider openai \
  --model "gpt-4o" \
  --prompt-a "Task: {input}. Respond in this format: 1) Summary 2) Solution 3) Recommendation" \
  --prompt-b "Here's a task: {input}. Provide your best response in a natural, conversational way." \
  --dataset code_tasks
```

**What This Tests:** Structured formatting vs. natural prose

---

### Example 6: Testing Creative Writing Styles

```bash
python neo_test.py \
  --prompt-a "Write a creative response to: {input}. Be imaginative, vivid, and engaging with rich descriptions." \
  --prompt-b "Create content for: {input}. Keep it clear, concise, and punchy with short sentences." \
  --dataset creative_prompts
```

**What This Tests:** Descriptive vs. punchy creative writing

---

## 📖 Documentation

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--prompt-a` | First prompt (text or file path) | Interactive prompt |
| `--prompt-b` | Second prompt (text or file path) | Interactive prompt |
| `--dataset` | Dataset name or path | `customer_support` |
| `--output` | Output path for HTML report | `./results/report.html` |
| `--provider` | API provider (anthropic/openai/openrouter) | `anthropic` |
| `--model` | Model to use | Provider-specific default |

### Prompt Format

Prompts **must** include `{input}` placeholder for variable substitution:

```
✅ Good: "Answer the following question concisely: {input}"
❌ Bad:  "Answer the following question concisely"
```

### Built-in Datasets

| Dataset | Description | Size |
|---------|-------------|------|
| `customer_support` | Customer service questions | 20 cases |
| `code_tasks` | Programming tasks | 20 cases |
| `creative_prompts` | Creative writing prompts | 20 cases |

### Custom Datasets

Create a JSON file with `input` field:

```json
[
  {"input": "Your test case 1"},
  {"input": "Your test case 2"},
  {"input": "Your test case 3"}
]
```

Then reference the file:
```bash
python neo_test.py --dataset ./my_dataset.json
```

---

## 📊 Output & Reports

### Terminal Output

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

### HTML Report

The generated HTML report includes:

- **Winner Announcement** - Statistical significance and confidence level
- **Metrics Comparison Table** - Side-by-side performance comparison
- **Interactive Visualizations** - Chart.js graphs for quality scores
- **Detailed Results** - Expandable test case details
- **ROI Analysis** - Cost savings projections at scale
- **Export Options** - PDF and Markdown export buttons

---

## 🧪 Statistical Analysis

### Metrics Tracked

For each prompt:

- **Quality Score**: 1-10 rating by LLM-as-judge (Claude)
- **Response Time**: Seconds per request
- **Token Count**: Input + output tokens
- **Cost**: Based on provider pricing

### Statistical Tests

The tool performs:

- **Independent samples t-test** - Compares quality scores between prompts
- **P-value calculation** - Significance threshold: 0.05
- **Effect size (Cohen's d)** - Measures practical significance
- **Confidence intervals** - 95% confidence bounds
- **Percentage improvement** - Relative performance gain

---

## 💡 Prompt Engineering Tips

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

1. **Tone Testing** - Professional vs Casual, Empathetic vs Direct
2. **Length Testing** - Concise vs Detailed, Bullet points vs Paragraphs
3. **Structure Testing** - Freeform vs Formatted, Step-by-step vs Summary
4. **Specificity Testing** - General instructions vs Detailed requirements
5. **Context Testing** - Minimal context vs Rich background information
6. **Role Testing** - Different persona descriptions or expertise levels

---

## 📁 Project Structure

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

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- All tests pass
- Code follows project style guidelines
- New features include documentation
- Update README.md if needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- **Anthropic Claude** - LLM-as-judge evaluation
- **OpenAI GPT** - Alternative testing provider
- **Chart.js** - Beautiful interactive visualizations
- **Python** - Core implementation language

---

## 📞 Support

For issues or questions:

- 🐛 **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- 📧 **Email**: support@example.com

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

*Scientific A/B testing for the age of AI*

</div>