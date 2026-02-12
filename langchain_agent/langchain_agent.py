from pydantic import BaseModel, Field
from typing import List, Tuple
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_agent.prompts import CONDENSE_QUESTION_PROMPT, prompt_template, FINAL_ANSWER_PROMPT
from operator import itemgetter
from langchain_agent.vector_store import retriever, _combine_documents


class ChatHistory(BaseModel):
    """Chat history with the bot."""

    chat_history: List[Tuple[str, str]] = Field(
        ...,
        json_schema_extra={"widget": {"type": "chat", "input": "question"}},
    )
    question: str


def _format_chat_history(chat_history: List[Tuple]) -> str:
    """Format chat history into a string."""
    buffer = ""
    for dialogue_turn in chat_history:
        human = "Human: " + dialogue_turn[0]
        ai = "Assistant: " + dialogue_turn[1]
        buffer += "\n" + "\n".join([human, ai])
    return buffer

_inputs = RunnableMap(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: _format_chat_history(x["chat_history"])
    )
    | CONDENSE_QUESTION_PROMPT
    | ChatOpenAI(temperature=0, model='gpt-4')
    | StrOutputParser(),
)

_context = {
    "context": itemgetter("standalone_question") | retriever | _combine_documents,
    "question": lambda x: x["standalone_question"],
}

conversational_qa_chain = (
    _inputs | _context | FINAL_ANSWER_PROMPT | ChatOpenAI(temperature=0, model='gpt-4') | StrOutputParser()
)

chain = conversational_qa_chain.with_types(input_type=ChatHistory)