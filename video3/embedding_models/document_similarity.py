from math import sqrt
from pprint import pprint
from common.config import embedding_model


def cosine_similarity(left, right):
    if len(left) != len(right):
        raise ValueError("Embedding dimensions must match")
    magnitude = sqrt(sum(x * x for x in left) * sum(y * y for y in right))
    return sum(x * y for x, y in zip(left, right)) / magnitude if magnitude else 0.0


def rank_documents(query, documents, vectors):
    if len(documents) != len(vectors):
        raise ValueError("Each document must have an embedding")
    return sorted(
        ({"document": document, "score": cosine_similarity(query, vector)}
         for document, vector in zip(documents, vectors)),
        key=lambda result: result["score"], reverse=True,
    )


def main():
    documents = [
        "Virat Kohli is an Indian cricketer known for his aggressive batting style and leadership qualities.",
        "Sachin Tendulkar is a former Indian cricketer widely regarded as one of the greatest batsmen in history.",
        "Mithali Raj is a former Indian cricketer and captain of the Indian women's national cricket team.",
        "Rohit Sharma is an Indian cricketer known for his elegant batting style and ability to score big centuries.",
        "Jasprit Bumrah is an Indian cricketer known for his exceptional fast bowling skills.",
    ]
    embeddings = embedding_model(dimensions=320)
    query = embeddings.embed_query("Who is the best cricketer in India?")
    vectors = embeddings.embed_documents(documents)
    results = rank_documents(query, documents, vectors)
    pprint(results)
    print("Most similar:")
    pprint(results[0])


if __name__ == "__main__":
    main()
