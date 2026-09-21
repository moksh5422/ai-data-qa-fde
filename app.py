import streamlit as st
import plotly.express as px
from data.ingestion import load_uploaded_files
from data.catalog import build_catalog
from llm.ollama_client import generate_plan
from query.validator import validate_sql
from query.executor import execute_sql
from query.repair import repair_query

st.set_page_config(page_title="AI Data Q&A", page_icon="📊", layout="wide")
st.title("📊 AI-Powered Data Q&A")
st.caption("Ask analytical questions across uploaded CSV and Excel files.")

with st.sidebar:
    st.header("Model")
    model = st.text_input("Ollama model", "qwen2.5:7b-instruct")
    st.markdown("**AI plans the query; DuckDB computes the answer.**")

uploads = st.file_uploader("Upload one or more CSV / Excel files", type=["csv", "xlsx", "xls"], accept_multiple_files=True)
if not uploads:
    st.info("Upload at least one file to start.")
    st.stop()

try:
    connection, tables, messages = load_uploaded_files(uploads)
    catalog = build_catalog(connection, tables)
except Exception as exc:
    st.error(f"Data loading failed: {exc}")
    st.stop()

st.success(f"Loaded {len(tables)} table(s).")
for message in messages:
    st.caption(message)

with st.expander("Data catalog"):
    st.code(catalog)

question = st.chat_input("Example: What is revenue by region?")
if question:
    st.chat_message("user").write(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Generating analytical plan..."):
                plan = generate_plan(question, catalog, model)
            sql = validate_sql(plan["sql"])
            try:
                result = execute_sql(connection, sql)
            except Exception as first_error:
                with st.spinner("Repairing query using the database error..."):
                    repaired = repair_query(question, catalog, sql, str(first_error), model)
                    sql = validate_sql(repaired["sql"])
                    result = execute_sql(connection, sql)
            if result.empty:
                st.warning("The query executed successfully but returned no rows.")
                st.code(sql, language="sql")
                st.stop()
            st.markdown(plan.get("answer_hint", "Here is the result."))
            st.dataframe(result, use_container_width=True, hide_index=True)
            chart = plan.get("chart", {})
            chart_type = chart.get("type", "none")
            x, y = chart.get("x"), chart.get("y")
            if chart_type != "none" and x in result.columns and y in result.columns:
                if chart_type == "line":
                    fig = px.line(result, x=x, y=y, markers=True)
                elif chart_type == "bar":
                    fig = px.bar(result, x=x, y=y)
                elif chart_type == "scatter":
                    fig = px.scatter(result, x=x, y=y)
                else:
                    fig = None
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            with st.expander("Generated SQL / audit"):
                st.code(sql, language="sql")
                st.json({"model": model, "question": question, "chart": chart})
        except Exception as exc:
            st.error("I couldn't reliably answer this question from the uploaded data. No unsupported answer was generated.")
            with st.expander("Technical details"):
                st.code(str(exc))
