# AI Data Analyst Agent

An interactive, AI-assisted data analysis dashboard that lets you explore datasets, ask questions in plain English, inspect generated SQL, and visualize results.

Built with **Python** and **Streamlit**, the application uses **DuckDB** for read-only analytical SQL and supports **OpenAI**, **Google Gemini**, and **Anthropic Claude** as optional AI providers.

## Features

- **Load datasets:** Start with the built-in sample dataset, upload a CSV file, or upload a SQLite database and select a table.
- **Explore data:** Preview records, inspect the schema, and review row counts, missing values, and duplicate rows.
- **Analyze without AI:** Calculate sums, averages, counts, minimums, and maximums, with optional grouping and chart selection.
- **Ask questions in plain English:** Ask an AI provider a question about the selected dataset and receive a DuckDB SQL query, a suggested pandas code snippet, a written answer, and additional insights.
- **Inspect SQL and results:** Review the generated SQL and the query output.
- **Visualize results:** Create interactive bar, line, scatter, histogram, and pie charts with Plotly.
- **Export results:** Download analysis results as a CSV file.
- **Choose an AI provider:** Configure OpenAI, Google Gemini, or Anthropic Claude.

## Application status and limitations

This is an initial portfolio version. The following distinctions are important:

- **Database connections:** The current application supports CSV uploads and SQLite database file uploads. It does not currently connect to PostgreSQL or other remote databases.
- **Python analysis:** The AI-generated Python/pandas snippet is displayed for inspection; the application does not execute that generated code.
- **Agent behavior:** The current workflow requests structured analysis from an LLM and executes the returned SQL. It is not yet an autonomous multi-step agent with independent tool selection, tool calling, and iterative analysis.
- **Accounts:** User authentication and multi-user account management are not implemented.

These capabilities may be added in future versions. They should not be assumed to be available in this release.

## Tech stack

| Technology | Purpose |
| --- | --- |
| Python | Application logic |
| Streamlit | Interactive web interface |
| Pandas and NumPy | Data loading, transformation, and analysis |
| DuckDB | In-memory analytical SQL execution |
| Plotly | Interactive visualizations |
| OpenAI API | Optional AI analysis provider |
| Google Gemini API | Optional AI analysis provider |
| Anthropic Claude API | Optional AI analysis provider |
| SQLite | Uploaded database file support |

## Project structure

```text
ai-data-analyst-agent/
├── app.py                 # Streamlit application and dashboard
├── analysis.py            # Sample data, manual analysis, AI calls, SQL, and charts
├── ui_assets.py           # UI styling and SVG icon helpers
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
├── .env.example           # Example environment variables
├── .gitignore             # Files excluded from version control
├── requirements.txt       # Python dependencies
└── README.md
```

## Requirements

- Python 3.10 or newer
- An API key for an AI provider to use the AI analysis feature. Manual analysis works without an API key.

## Run locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/arafam/ai-data-analyst-agent.git
   cd ai-data-analyst-agent
   ```

2. **Create and activate a virtual environment:**

   macOS / Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   py -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

3. **Install dependencies:**

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure an AI provider (optional):**

   Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

   Add the API key for the provider you want to use. The application reads environment variables but does not automatically load a `.env` file. If you use one, load its values into your shell or configure them in your deployment environment. You can also enter an API key in the AI analysis interface.

5. **Start the application:**

   ```bash
   streamlit run app.py
   ```

6. Open the local URL printed by Streamlit, usually [http://localhost:8501](http://localhost:8501).

## Environment variables

All provider settings are optional. Configure only the provider you plan to use.

| Variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_MODEL` | OpenAI model name (default: `gpt-4.1-mini`) |
| `GEMINI_API_KEY` | Google Gemini API key |
| `GEMINI_MODEL` | Gemini model name (default: `gemini-2.5-flash`) |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `ANTHROPIC_MODEL` | Claude model name (default: `claude-sonnet-5-5`) |

Keep real API keys in your local environment or deployment secret manager. Never commit `.env`, API keys, database credentials, or private datasets.

## Example questions

- Which region has the highest total sales?
- Show monthly revenue over time.
- What are the top 10 products by profit?
- Are there outliers in the order amount column?
- Compare average sales across categories.

The available questions depend on the columns and contents of the loaded dataset.

## How it works

1. Select the sample dataset, upload a CSV, or upload a SQLite database and choose a table.
2. The application displays a data overview, column schema, and basic data-quality metrics.
3. For AI analysis, the application sends the selected provider the user's question, dataset schema, and a sample of up to five rows.
4. The AI provider returns structured content containing a SQL query, suggested Python code, chart settings, an answer, and insights.
5. The application applies basic SQL checks and executes the query against an in-memory DuckDB connection.
6. The application displays the answer, query results, SQL, suggested Python snippet, and available chart.

Manual analysis is also available and does not require an AI API key.

## Security and privacy

This project is an educational and portfolio demonstration, **not a production-ready service**.

- AI analysis sends the user's question, dataset schema, and up to five sample rows to the selected AI provider. Do not use confidential or sensitive data unless you have reviewed the provider's data-handling terms and have permission to share it.
- SQL validation uses application-level checks and DuckDB's external-access setting. These safeguards provide defense in depth, but they are not a complete security boundary.
- AI-generated Python is displayed only; it is not executed by the application.
- Uploaded SQLite files are read by the application. Upload only database files you trust.
- Keep API keys and database credentials out of source control.

Before using this application with untrusted users or sensitive data, add stronger SQL parsing and query controls, resource limits, isolated execution where needed, authentication and authorization, secure secret management, logging, and a privacy review.

## Planned improvements

Potential future work includes remote database connections, safe Python execution in an isolated environment, multi-step agent orchestration with tool calling, automated tests, and production deployment hardening.
