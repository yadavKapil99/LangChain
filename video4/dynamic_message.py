from langchain_core.prompts import ChatPromptTemplate
from common.config import chat_model


prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly {userRole} assistant. Talk to the user like a "
     "{userRole} expert. Use simple language and keep the conversation engaging."),
    ("human", "Explain in simple terms: {userInput}"),
])


def main():
    messages = prompt_template.format_messages(
        userInput="What is the capital of France?", userRole="travel",
    )
    print("Original messages:")
    for message in messages:
        print(type(message).__name__, message.content)
    response = chat_model(temperature=0.7, max_tokens=500).invoke(messages)
    print("AI response:", response.content)
    messages.append(response)
    print("Updated messages:")
    for message in messages:
        print(type(message).__name__, message.content)


if __name__ == "__main__":
    main()
