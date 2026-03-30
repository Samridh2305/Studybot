def build_prompt(context, query):
    return f"""
You are a helpful AI assistant.

Answer the question strictly using the context below.

Rules:
- Only use the provided context
- If answer is missing, say "I don't know"
- Cite sources in format: (filename, page number)

Context:
{context}

Question:
{query}

Answer format:
- Answer:
- Sources:
"""