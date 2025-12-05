import os

def call_openai(prompt: str):
    try:
        import openai
    except ImportError:
        raise RuntimeError("OpenAI not installed")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY environment variable")

    """
    client = openai.OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3
    )
    return {"translation": resp.choices[0].message.content}
    """

    # placeholder
    return {"translation": "[REAL MODEL CALL DISABLED]"}


def call_huggingface(model_name, prompt):
    # Outline only
    """
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
    tok = AutoTokenizer.from_pretrained(model_name)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    pipe = pipeline("text2text-generation", model=mdl, tokenizer=tok)
    result = pipe(prompt, max_length=200)
    return {"translation": result[0]["generated_text"]}
    """

    return {"translation": "[HF MODEL DISABLED]"}
