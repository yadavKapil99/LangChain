from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from common.config import chat_model


def main():
    messages = [
        SystemMessage(content="You are a friendly AI assistant. Talk to the user like a close friend. "
                      "Use simple language and keep the conversation engaging."),
        HumanMessage(content="Hello! How are you today?"),
    ]
    response = chat_model(temperature=0.7, max_tokens=500).invoke(messages)
    print("AI response:", response.content)
    messages.append(AIMessage(content=response.content))
    print("Updated messages:", messages)
    print([message.content for message in messages])


if __name__ == "__main__":
    main()
