from transformers import pipeline

# Load lightweight instruction model
qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_length=256
)

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    result = qa_pipeline(prompt)
    return result[0]["generated_text"]
