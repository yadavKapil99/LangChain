from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from common.config import require_key

embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=require_key("OPENROUTER_API_KEY", "OPEN_ROUTER_API_KEY"),
)

docs = [
    Document(page_content="Rohit Sharma is an Indian cricketer and the current captain of the Indian national team in limited-overs formats."),
    Document(page_content="Virat Kohli is an Indian cricketer and former captain of the Indian national team in all formats."),
    Document(page_content="Jasprit Bumrah is an Indian cricketer and a fast bowler who plays for the Indian national team."),
    Document(page_content="The geopolitical history of India and Pakistan from the perspective of China is complex and multifaceted, involving historical conflicts, territorial disputes, and strategic alliances. The relationship between India and Pakistan has been marked by wars, border skirmishes, and ongoing tensions over issues such as Kashmir. China has historically maintained a strategic partnership with Pakistan, providing economic and military support, while also engaging with India on various fronts. The geopolitical dynamics in the region are influenced by factors such as trade routes, regional security concerns, and the interests of global powers."),
    Document(page_content="Sania Nehwal is an Indian badminton player who has won numerous international titles and is considered one of the best female badminton players in India."),
    Document(page_content="John Wick is a fictional character and the protagonist of the John Wick film series, portrayed by Keanu Reeves. He is a retired hitman seeking vengeance for the death of his beloved dog, which was a gift from his deceased wife.")
]

vector_store = FAISS.from_documents(
    docs,
    embeddings,
)

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "lambda_mult": 0.1},
)

query = "What is cricket ?"


result = retriever.invoke(query)

for i, doc in enumerate(result):
    print(f"\n ---- Result {i+1} ----")
    print(f" Content \n ---- {doc.page_content} ----")