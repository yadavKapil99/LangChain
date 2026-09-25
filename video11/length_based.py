from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


load_test = TextLoader("../video10/textFile.txt", encoding="utf-8").load()

print(load_test[0].page_content);

splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0, separator="")

split_docs = splitter.split_documents(load_test);


print("========================================")

print(f"Number of split documents: {len(split_docs)}")

print(split_docs[0].page_content);

print("========================================")


pdf_loader = PyPDFLoader("../Ashish_resume.pdf").load();

print(f"Number of pages in PDF: {len(pdf_loader)}");

split_pdf_docs = splitter.split_documents(pdf_loader);

print("========================================")
print(f"Number of split PDF documents: {len(split_pdf_docs)}")
print(split_pdf_docs[0]);
