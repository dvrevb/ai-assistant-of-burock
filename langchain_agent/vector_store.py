from langchain_core.prompts import format_document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate

embeddings = OpenAIEmbeddings(model = 'text-embedding-ada-002', chunk_size=5000)

persist_directory = '../utils/vector-store'

vectordb = Chroma(
    embedding_function=embeddings,
    persist_directory=persist_directory
)

retriever = vectordb.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": 3,
                },
            )

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")

def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    """Combine documents into a single string."""
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)