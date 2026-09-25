from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from common.config import chat_model


class PersonInfo(BaseModel):
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age as a number")
    profession: str = Field(description="The person's profession")
    skills: list[str] = Field(description="The person's skills")


parser = PydanticOutputParser(pydantic_object=PersonInfo)
prompt = ChatPromptTemplate.from_template(
    "Extract information from this text: {text}\n{format_instructions}"
).partial(format_instructions=parser.get_format_instructions())


def main():
    print("Format instructions:", parser.get_format_instructions())
    chain = prompt | chat_model() | parser
    result = chain.invoke({
        "text": "Rahul Yadav is 25 years old and works as a Full Stack Software Engineer. "
                "He has experience with Node.js, React, PostgreSQL and LangChain.",
    })
    print("Parsed result:", result.model_dump())
    print("Name:", result.name)
    print("Age:", result.age)
    print("Profession:", result.profession)
    print("Skills:", result.skills)


if __name__ == "__main__":
    main()
