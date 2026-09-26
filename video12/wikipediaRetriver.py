import wikipedia
from langchain_community.retrievers import WikipediaRetriever
from requests.exceptions import JSONDecodeError

wikipedia.set_user_agent("gen-ai-lessons/0.1 (LangChain learning project)")

retriever =  WikipediaRetriever(top_k_results = 2, lang = "en")

query = "The geopolitical history of India and Pakistan from the perspective of china"

try:
  docs = retriever.invoke(query)
except JSONDecodeError:
  raise SystemExit(
    "Wikipedia returned a non-JSON response (likely rate limiting or a network/VPN block). "
    "Wait a minute and retry, or check that https://en.wikipedia.org opens in your browser."
  )

for i, doc in enumerate(docs):
  print(f"\n ---- Result {i+1} ----")
  print(f" Content \n ---- {doc.page_content} ----")
