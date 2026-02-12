from pydantic import BaseModel
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_agent.prompts import CONDENSE_QUESTION_PROMPT, FINAL_ANSWER_PROMPT
from operator import itemgetter
from langchain_agent.vector_store import retriever, _combine_documents
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

class ChainInput(BaseModel):
    question: str
    conversation_id: str


# Condense Question Chain
_inputs = RunnableMap(
    standalone_question=CONDENSE_QUESTION_PROMPT
    | ChatOpenAI(temperature=0, model="gpt-4")
    | StrOutputParser(),
)

# Retrieval Context
_context = {
    "context": itemgetter("standalone_question") | retriever | _combine_documents,
    "question": itemgetter("standalone_question"),
}

# Final QA Chain
conversational_qa_chain = (
    _inputs
    | _context
    | FINAL_ANSWER_PROMPT
    | ChatOpenAI(temperature=0, model="gpt-4")
    | StrOutputParser()
)

# In-Memory Session Store
store = {}

def get_session_history(conversation_id: str) -> BaseChatMessageHistory:
    if conversation_id not in store:
        store[conversation_id] = ChatMessageHistory()
    return store[conversation_id]


#  Wrap with Message History
chain_with_memory = RunnableWithMessageHistory(
    conversational_qa_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)