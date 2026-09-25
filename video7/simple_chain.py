from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from common.config import chat_model


prompt = ChatPromptTemplate.from_template("""Extract information from the following text.
Text: {text}
Return ONLY valid JSON with keys name, age, and profession.
Use a number for age. Use null for missing information; do not invent facts.
No internet search tool is available in this example.""")


def main():
    text = input("Enter text about a person: ")
    chain = prompt | chat_model() | JsonOutputParser()
    result = chain.invoke({"text": text})
    print("Parsed result:", result)
    for key in ("name", "age", "profession"):
        print(f"{key.title()}:", result.get(key))


if __name__ == "__main__":
    main()
