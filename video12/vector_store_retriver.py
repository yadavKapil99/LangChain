from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from common.config import require_key

embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=require_key("OPENROUTER_API_KEY", "OPEN_ROUTER_API_KEY"),
)

documents = [
    Document(page_content="Rohit Sharma is an Indian cricketer and the current captain of the Indian national team in limited-overs formats."),
    Document(page_content="Virat Kohli is an Indian cricketer and former captain of the Indian national team in all formats."),
    Document(page_content="Jasprit Bumrah is an Indian cricketer and a fast bowler who plays for the Indian national team."),
]

vectore_store = Chroma.from_documents(
    documents,
    embeddings,
    ids=[f"doc-{i}" for i in range(len(documents))],  # fixed ids so reruns overwrite instead of duplicating
    collection_name="geopolitics", 
    persist_directory="./chroma_db"
)


retriever = vectore_store.as_retriever(search_kwargs={"k": 2})

query = "Name the bowler who plays for the Indian national team."

# vectore_store.similarity_search(query, k=2)
# only on the basis of cosine similarity, we can use the retriever to get the most relevant documents based on the query.


result = retriever.invoke(query)

for i, doc in enumerate(result):
    print(f"\n ---- Result {i+1} ----")
    print(f" Content \n ---- {doc.page_content} ----")

