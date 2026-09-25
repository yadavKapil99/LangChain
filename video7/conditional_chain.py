from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from common.config import chat_model

from langchain_core.runnables import RunnableBranch, RunnableLambda


def build_chains(model):
    classification = (
        ChatPromptTemplate.from_template(
            "Check the tone. Return ONLY Positive or Negative.\nText: {text}"
        ) | model | StrOutputParser() | RunnableLambda(lambda text: text.strip().lower())
    )
    positive = (ChatPromptTemplate.from_template(
        "Give a short friendly positive response to this message: {text}"
    ) | model | StrOutputParser())
    negative = (ChatPromptTemplate.from_template(
        "Give a short empathetic response to this negative message: {text}"
    ) | model | StrOutputParser())
    branch = RunnableBranch(
        (lambda data: data["classification"] == "positive", positive),
        (lambda data: data["classification"] == "negative", negative),
        positive,
    )
    return classification, branch


def main():
    classification_chain, conditional_chain = build_chains(chat_model())
    text = "I really love this product! It is amazing."
    classification = classification_chain.invoke({"text": text})
    print("Classification:", classification)
    result = conditional_chain.invoke({"text": text, "classification": classification})
    print("Response:", result)


if __name__ == "__main__":
    main()
