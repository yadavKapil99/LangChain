from common.config import embedding_model


def main():
    embeddings = embedding_model(dimensions=32)
    print("Embedding:", embeddings.embed_query("Hello, world!"))


if __name__ == "__main__":
    main()
