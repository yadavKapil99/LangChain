import argparse
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from common.config import PROJECT_ROOT


def load_directory(path=PROJECT_ROOT, recursive=False):
    loader = DirectoryLoader(
        str(path), glob="*.pdf", loader_cls=PyPDFLoader,
        loader_kwargs={"mode": "page"}, recursive=recursive,
        exclude=["**/node_modules/**", "**/.venv/**", "**/.git/**"],
    )
    return loader.load()


def main():
    cli = argparse.ArgumentParser(description="Load PDFs directly from a directory.")
    cli.add_argument("path", nargs="?", type=Path, default=PROJECT_ROOT)
    cli.add_argument("--recursive", action="store_true", help="Also search subdirectories")
    args = cli.parse_args()
    print("Loading documents from directory...")
    docs = load_directory(args.path, recursive=args.recursive)
    print(docs)
    print(f"Documents loaded successfully. Pages: {len(docs)}")


if __name__ == "__main__":
    main()
