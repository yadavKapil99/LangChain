from common.config import chat_model


def main():
    llm = chat_model(temperature=0.7)
    response = llm.invoke("Meaning of name Kapil:")
    print(response)
    print("Response received successfully.", response.content)


if __name__ == "__main__":
    main()
