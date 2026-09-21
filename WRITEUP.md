# AI-Powered Data Q&A — Approach

I treated this as a data reliability problem rather than simply a chatbot problem. CSV/Excel files are loaded with Pandas and registered as DuckDB tables. A catalog containing schemas, row counts and sample values is passed with the user's question to a local Qwen model through Ollama.

The model generates read-only DuckDB SQL and a visualization plan. DuckDB executes the SQL and provides the actual result; Streamlit and Plotly render the output.

The key delta solutioning is the deterministic control layer around the LLM: schema grounding, structured output, read-only SQL validation, deterministic execution, one controlled error-driven repair, safe failure and visible generated SQL. This avoids relying on generated prose for numerical answers.

I intentionally avoided a large agent framework, vector database and cloud infrastructure because the exercise asks for a small 4–6 hour prototype. For production I would add a governed semantic layer, stronger SQL AST validation, authentication/RBAC, automatic join discovery, evaluation datasets, caching, data-quality checks and observability.
