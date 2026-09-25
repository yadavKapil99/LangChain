from typing import Literal
from pydantic import BaseModel, Field
from common.config import chat_model


class Stats(BaseModel):
    matches: int
    runs: int
    wickets: int


class Person(BaseModel):
    name: str
    age: int
    skills: list[str]
    stats: Stats
    best_performance: str | None = Field(description="Best performance in their field")
    last_data_update: str = Field(description="Date when data was last updated, YYYY-MM-DD")
    is_ready_for_captaincy: bool = Field(description="Whether the person is ready for captaincy")
    is_bowler: Literal["pos", "neg"] = Field(description="pos if a bowler, otherwise neg")
    pros: list[str] = Field(description="Positive aspects or strengths")
    cons: list[str] = Field(description="Negative aspects or weaknesses")


def main():
    structured_llm = chat_model(temperature=0.7).with_structured_output(
        Person, method="function_calling",
    )
    response = structured_llm.invoke([
        ("system", "You are a helpful assistant that provides information about people."),
        ("human", "Provide details about a person named Surya Kumar Yadav."),
    ])
    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
