from time import perf_counter
from langchain_core.prompts import PromptTemplate
from common.config import chat_model


prompt_template = PromptTemplate.from_template("""Summarise the cricketer {name}.
Explanation Length: {length}
Include:
1. Total matches in IPL, ODI, Test, T20 and Class A.
2. Best performance in each category.
3. Career peak and downfall.
If information is unavailable, say "Insufficient data available" instead of guessing.
Use a professional tone and keep the response concise.""")


def main():
    llm = chat_model(temperature=0.3, max_tokens=500)
    start = perf_counter()
    prompt = prompt_template.format(name="Surya Kumar", length="Medium")
    print(f"Prompt formatting: {perf_counter() - start:.4f}s")
    print("FINAL PROMPT:", prompt)
    start = perf_counter()
    for chunk in llm.stream(prompt):
        if isinstance(chunk.content, str):
            print(chunk.content, end="", flush=True)
    print(f"\nLLM response: {perf_counter() - start:.2f}s")


if __name__ == "__main__":
    main()
