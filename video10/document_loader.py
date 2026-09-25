import argparse
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from common.config import PROJECT_ROOT


def load_pdf(path):
    return PyPDFLoader(str(path), mode="page").load()


def main():
    cli = argparse.ArgumentParser(description="Load a PDF, with one document per page.")
    cli.add_argument("path", nargs="?", type=Path,
                     default=PROJECT_ROOT / "System Design Interview by Alex Xu (1).pdf")
    args = cli.parse_args()
    print("Loading PDF from file...")
    docs = load_pdf(args.path)
    print(docs)
    print(f"PDF loaded successfully. Pages: {len(docs)}")


if __name__ == "__main__":
    main()
