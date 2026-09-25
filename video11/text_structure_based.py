from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader



splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    separators=["\n\n", "\n", " ", ""]
    )

load_txt = TextLoader("../video10/textFile.txt", encoding="utf-8").load()

splitted_text = splitter.split_documents(load_txt);

print("========================================")
print(f"Number of split documents: {len(splitted_text)}")
print(splitted_text)

