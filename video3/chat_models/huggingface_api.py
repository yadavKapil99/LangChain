from common.config import huggingface_model


def main():
    llm = huggingface_model()
    print("Sending request...")
    response = llm.invoke("What is the capital of France? Answer in one word.")
    print("Response:", response.content)


if __name__ == "__main__":
    main()
