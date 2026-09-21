from llm.ollama_client import generate_repair


def repair_query(question, catalog, sql, error, model):
    return generate_repair(question, catalog, sql, error, model)
