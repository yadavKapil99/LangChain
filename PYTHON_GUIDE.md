# Python equivalents for the reference notes

The original `.txt` study notes are preserved. Use the following Python syntax
when translating their JavaScript examples.

| JavaScript | Python |
| --- | --- |
| `PromptTemplate.fromTemplate(...)` | `PromptTemplate.from_template(...)` |
| `ChatPromptTemplate.fromMessages(...)` | `ChatPromptTemplate.from_messages(...)` |
| `prompt.format({name: "Kapil"})` | `prompt.format(name="Kapil")` |
| `prompt.formatMessages({...})` | `prompt.format_messages(...)` |
| `prompt.pipe(model).pipe(parser)` | `prompt | model | parser` |
| `StringOutputParser` | `StrOutputParser` |
| `withStructuredOutput(schema)` | `with_structured_output(Schema, method="function_calling")` |
| `StructuredOutputParser.fromNamesAndDescriptions(...)` | `PydanticOutputParser(pydantic_object=Schema)` |
| `getFormatInstructions()` | `get_format_instructions()` |
| `withConfig({runName: "demo"})` | `with_config(run_name="demo")` |
| `withRetry({stopAfterAttempt: 3})` | `with_retry(stop_after_attempt=3)` |
| `withFallbacks({fallbacks: [other]})` | `with_fallbacks([other])` |
| `embedQuery(text)` | `embed_query(text)` |
| `embedDocuments(texts)` | `embed_documents(texts)` |
| `pageContent` | `page_content` |
| `PDFLoader` | `PyPDFLoader` |
| `console.log(value)` | `print(value)` |

`invoke`, `batch`, `stream`, and `partial` keep their names. Synchronous calls
need no `await`; async alternatives include `ainvoke`, `abatch`, and `astream`.

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from common.config import chat_model

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {role} assistant."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
]).partial(role="travel")
chain = prompt | chat_model() | StrOutputParser()
result = chain.invoke({"history": [], "question": "Explain train travel."})
print(result)
```

Zero-shot, one-shot, few-shot, role, context, constraint, delimiter,
classification, extraction, and summarization prompts use the same natural
language instructions in Python. Pass variables with `format` keyword arguments
or an input dictionary to a chain. Literal JSON braces in templates must be
doubled (`{{` and `}}`). A prompt requesting internet research does not itself
give a model browsing tools.

## Pydantic replaces Zod

```python
from typing import Literal
from pydantic import BaseModel, Field

class Stats(BaseModel):
    matches: int
    runs: int

class Person(BaseModel):
    name: str = Field(description="Full name")
    age: int
    skills: list[str]
    stats: Stats
    role: Literal["developer", "designer", "student"]
    is_experienced: bool
    nickname: str | None = None
    best_performance: str | None
    metadata: dict[str, str] = Field(default_factory=dict)
```

`str`, `int`/`float`, `bool`, `list`, nested BaseModel classes, `Literal`, unions
such as `str | int`, and `dict` cover the Zod types in the original notes.
A nullable field (`str | None`) without a default is still required. Adding
`= None` allows it to be omitted. `Field(description=...)` explains a field;
`Field(default_factory=list)` provides a fresh collection for each instance.

A schema describes output structure; a prompt describes the task. Structured
output does not guarantee that factual claims are correct. Pydantic results
provide attributes (`result.name`), `model_dump()` for dictionaries, and
`model_dump_json()` for JSON. `JsonOutputParser` returns dictionaries, accessed
with `result["name"]` or `result.get("name")`.

## Runnables

```python
from langchain_core.runnables import (
    RunnableBranch, RunnableLambda, RunnableParallel, RunnablePassthrough,
)

uppercase = RunnableLambda(lambda text: text.upper())
parallel = RunnableParallel(original=RunnablePassthrough(), upper=uppercase)
print(parallel.invoke("hello"))
branch = RunnableBranch((lambda text: bool(text), uppercase), RunnablePassthrough())
print(branch.invoke("hello"))
```

A branch ends with a default runnable. Parallel chains receive the same input.
Sequential chains pass one output into the next step; use a RunnableLambda when
you need to turn a string into a dictionary for the next prompt.

## References

- [LangChain Python integrations](https://reference.langchain.com/python/integrations/overview)
- [Document loaders](https://reference.langchain.com/python/langchain-community/document_loaders)
