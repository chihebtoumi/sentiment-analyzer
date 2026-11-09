# 💬 Sentiment Analyzer: Parallel LLM Tasks

A Streamlit web app that analyzes any text with a large language model.
Enter a text and get:

- **Text**: your original input
- **Sentiment**: positive, negative or neutral
- **Topic**: a concise description of what the text is about
- **Follow-up question**: a relevant question to explore the text further

## How it works

The app is built with LangChain Expression Language (LCEL), following the
parallel chains approach from notebook 24 (*Parallel Chains*).

Three independent LLM chains run **in parallel** with `RunnableParallel`:

1. Sentiment analysis
2. Main topic extraction
3. Follow-up question generation

Because these tasks do not depend on each other, the total response time is
about that of the slowest single call instead of the sum of all three.

```
text -> prepare input -> [ sentiment | topic | follow-up ] (parallel) -> results
```

The LLM is served by [Groq](https://console.groq.com). The default model is
`openai/gpt-oss-20b`, configurable with the `GROQ_MODEL` environment variable.

## Project structure

```
sentiment-analyzer/
├── app.py            # Streamlit interface
├── chains.py         # LangChain parallel chain
├── pyproject.toml    # Dependencies (uv)
├── uv.lock
├── .env.example      # Environment variables template
└── README.md
```

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- A free Groq API key: https://console.groq.com

### Setup

```bash
git clone https://github.com/chihebtoumi/sentiment-analyzer.git
cd sentiment-analyzer
uv sync
```

Create your `.env` file from the template:

```bash
# Windows
copy .env.example .env
# Mac/Linux
cp .env.example .env
```

Then open `.env` and add your key:

```
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

> Never commit your `.env` file. It is listed in `.gitignore`.

## Usage

```bash
uv run streamlit run app.py
```

Once the app is running, open http://localhost:8501 in your browser.

1. Type or paste a text in the input box.
2. Click **Analyze**.
3. Read the sentiment, topic and follow-up question.

### Example

**Input:** `I had a fantastic time hiking up the mountain yesterday.`

| Field | Output |
|---|---|
| Sentiment | Positive |
| Topic | Hiking |
| Follow-up question | What were the most memorable parts of your hike? |

## Tech stack

Python · Streamlit · LangChain · Groq · uv

## Troubleshooting

- **`GROQ_API_KEY is missing`**: check that `.env` is in the project root and is not named `.env.txt`.
- **`model_not_found` (404)**: the model may have been retired. Pick a current model ID on the [Groq models page](https://console.groq.com/docs/models) and set it in `GROQ_MODEL`.
- **Rate limit errors**: the free tier has limits. Wait a few seconds and retry.

## Author

Chiheb Toumi ([@chihebtoumi](https://github.com/chihebtoumi))