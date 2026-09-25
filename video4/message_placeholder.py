from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from common.config import chat_model


prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly {userRole} assistant. Talk to the user like a "
     "{userRole} expert. Use simple language and keep the conversation engaging."),
    MessagesPlaceholder("chatHistory"),
    ("human", "{userInput}"),
])


def main():
    history = [
        HumanMessage(content="I want to request a refund for my order 12345."),
        AIMessage(content="Sure! Can you please provide the reason for your refund request?"),
        HumanMessage(content="The product I received was damaged and not as described."),
        AIMessage(content="I apologize for the inconvenience. I will initiate the refund process "
                  "for order 12345. You should receive a confirmation email shortly."),
    ]
    messages = prompt_template.format_messages(
        userRole="customer service agent", userInput="Where is my refund?", chatHistory=history,
    )
    print("Original messages:", messages)
    response = chat_model(temperature=0.7, max_tokens=500).invoke(messages)
    print("AI response:", response.content)
    messages.append(response)
    print("Updated messages:", messages)


if __name__ == "__main__":
    main()
