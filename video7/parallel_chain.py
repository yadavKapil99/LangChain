from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from common.config import chat_model

import json
from langchain_core.runnables import RunnableParallel


def build_chains(model):
    notes = (ChatPromptTemplate.from_template(
        "Generate short and simple notes from the following text: {text}"
    ) | model | StrOutputParser())
    quiz = (ChatPromptTemplate.from_template(
        'Generate 5 MCQs based on: {text}. Return ONLY valid JSON: '
        '{{"questions": [{{"question": "...", "options": ["A) ...", "B) ...", '
        '"C) ...", "D) ..."], "answer": "A"}}]}}'
    ) | model | JsonOutputParser())
    parallel = RunnableParallel(notes=notes, mcqs=quiz)
    merge = (ChatPromptTemplate.from_template(
        'Merge notes and MCQs into one JSON object. Notes: {notes} MCQs: {mcqs}. '
        'Return ONLY JSON with keys "notes" (string) and "questions" (array of MCQs).'
    ) | model | JsonOutputParser())
    return parallel, merge


def main():
    parallel_chain, merge_chain = build_chains(chat_model())
    parallel_result = parallel_chain.invoke({"text": "India"})
    print("Parallel result:", json.dumps(parallel_result, indent=2))
    result = merge_chain.invoke({
        "notes": parallel_result["notes"], "mcqs": json.dumps(parallel_result["mcqs"]),
    })
    print("Final result:", json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
