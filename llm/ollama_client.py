import json
import requests

from config import OLLAMA_URL
from llm.prompts import SYSTEM_PROMPT


def _call_ollama(prompt, model):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "format": "json",
            "options": {"temperature": 0},
        },
        timeout=180,
    )
    response.raise_for_status()
    return json.loads(response.json()["message"]["content"])


def generate_plan(question, catalog, model):
    return _call_ollama(f"DATA CATALOG:\n{catalog}\n\nUSER QUESTION:\n{question}", model)


def generate_repair(question, catalog, sql, error, model):
    prompt = f"""
The previous SQL failed.

USER QUESTION:
{question}

CATALOG:
{catalog}

FAILED SQL:
{sql}

DATABASE ERROR:
{error}

Return corrected JSON using the same schema. Do not explain.
"""
    return _call_ollama(prompt, model)
