def build_prompt(context, query):
    return f"""
You are a helpful assistant.

Use the context below to answer the question.
If the context is not relevant, use your general knowledge.

Context:
{context}

Question:
{query}

Answer clearly and correctly:
"""