import argparse
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from common.config import chat_model


def load_text(path):
    return TextLoader(str(path), encoding="utf-8").load()


def main():
    cli = argparse.ArgumentParser(description="Load a text file and summarize it.")
    cli.add_argument("path", nargs="?", type=Path, default=Path(__file__).with_name("textFile.txt"))
    cli.add_argument("--load-only", action="store_true", help="Skip the model call")
    args = cli.parse_args()
    print("Loading text from file...")
    docs = load_text(args.path)
    for document in docs:
        print(document.page_content)
    print(f"Text loaded successfully. Documents: {len(docs)}")
    if not args.load_only:
        prompt = ChatPromptTemplate.from_template("Write a summary of the following text: {text}")
        chain = prompt | chat_model() | StrOutputParser()
        print("Summary:", chain.invoke({"text": "\n\n".join(doc.page_content for doc in docs)}))


if __name__ == "__main__":
    main()
