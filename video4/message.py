from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from common.config import chat_model


prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly AI assistant. Talk naturally like a close friend. "
     "Use simple language, match the user's tone, explain technical topics clearly, "
     "and do not make up information."),
    MessagesPlaceholder("history"),
    ("human", "{user_input}"),
])


def main():
    llm = chat_model(temperature=0.7, max_tokens=500)
    history = []
    print("Friendly AI Chatbot. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if not user_input:
            continue
        messages = prompt_template.format_messages(history=history, user_input=user_input)
        print("AI: ", end="", flush=True)
        parts = []
        for chunk in llm.stream(messages):
            if isinstance(chunk.content, str):
                parts.append(chunk.content)
                print(chunk.content, end="", flush=True)
        history.extend([HumanMessage(content=user_input), AIMessage(content="".join(parts))])
        print()
    print("Chat history:")
    for message in history:
        print(f"{message.type}: {message.content}")


if __name__ == "__main__":
    main()
