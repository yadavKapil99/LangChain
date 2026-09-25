import os

from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

print(f"Using model: {os.environ['OPENROUTER_MODEL']}")
print(f"Using base URL: {os.environ['OPENROUTER_BASE_URL']}")
print(f"Using API key: {os.environ['OPENROUTER_API_KEY']}")

model = ChatOpenAI(
    model=os.environ["OPENROUTER_MODEL"],
    base_url=os.environ["OPENROUTER_BASE_URL"],
    api_key=os.environ["OPENROUTER_API_KEY"],
)

loader = WebBaseLoader("https://en.wikipedia.org/wiki/Apple_M5")
docs = loader.load()

print(f"Loaded {len(docs)} document(s)")

prompt = ChatPromptTemplate.from_template(
    "Summarize this page in 3 bullet points:\n\n{page}"
)
chain = prompt | model | StrOutputParser()

# Start with a short excerpt while testing; a whole Wikipedia page can be large.
summary = chain.invoke({"page": docs[0].page_content[:12000]})
print(summary)