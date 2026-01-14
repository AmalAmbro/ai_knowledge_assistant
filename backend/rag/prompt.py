def build_prompt(context: str, question: str) -> str:
    return f"""
You are a factual assistant.
Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}
"""
