from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from common.config import chat_model


def main():
    prompt = ChatPromptTemplate.from_template(
        "Explain in simple words: {topic}. Keep the explanation under 100 words."
    )
    chain = prompt | chat_model() | StrOutputParser()
    print(chain.invoke({"topic": "Stats of Surya Kumar Yadav in Test, ODI, T20 and IPL"}))


if __name__ == "__main__":
    main()
