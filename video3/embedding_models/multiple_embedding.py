from common.config import embedding_model


def main():
    documents = [
        "The capital of France is Paris.",
        "The capital of Germany is Berlin.",
        "The capital of Italy is Rome.",
        "The capital of Spain is Madrid.",
        "The capital of Portugal is Lisbon.",
    ]
    embeddings = embedding_model(dimensions=32)
    print("Embeddings:", embeddings.embed_documents(documents))


if __name__ == "__main__":
    main()
