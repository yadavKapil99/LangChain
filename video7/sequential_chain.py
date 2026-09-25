from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from common.config import chat_model

from langchain_core.runnables import RunnableLambda


def build_chain(model):
    report_prompt = ChatPromptTemplate.from_template("Generate a detailed report about {text}.")
    summary_prompt = ChatPromptTemplate.from_template(
        "Summarize this report into exactly 5 bullet points.\nReport: {report}"
    )
    return (report_prompt | model | StrOutputParser()
            | RunnableLambda(lambda report: {"report": report})
            | summary_prompt | model | StrOutputParser())


def main():
    text = input("Enter text about a person: ")
    print("Parsed result:", build_chain(chat_model()).invoke({"text": text}))


if __name__ == "__main__":
    main()
