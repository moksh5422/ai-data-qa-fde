# AI-Powered Data Q&A

A local-first AI analytics application for uploading multiple CSV/Excel files and asking analytical questions in plain English.

## Architecture

Upload → Pandas → Data catalog → DuckDB → Qwen/Ollama → SQL validation → DuckDB execution → table/chart.

**Core principle: AI plans the analysis; DuckDB computes the answer.**

## Setup

Python 3.11/3.12 recommended.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
ollama pull qwen2.5:7b-instruct
ollama serve
```

Open another terminal:

```powershell
.venv\Scripts\activate
streamlit run app.py
```

Or run `run.bat`.

## Demo

Upload `sample_data/orders.csv`, `sample_data/customers.csv`, and `sample_data/products.csv`.

Try:
- What is the total revenue?
- What is revenue by region?
- Show the monthly revenue trend.
- Which product category generated the most revenue?
- Compare average revenue between Enterprise and SMB customers.

## Delta solutioning

The LLM receives the real schema and sample metadata, generates read-only SQL, passes a safety gate, and DuckDB calculates the actual answer. If execution fails, one controlled repair uses the database error. Unsupported questions fail safely.

## Production evolution

Add a governed semantic layer, AST-level SQL validation, join-key discovery, authentication/RBAC, object storage, caching, evaluation datasets, observability, data-quality checks and resource limits.
