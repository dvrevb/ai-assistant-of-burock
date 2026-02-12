from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from openai_responses import api_openai_responses
from langchain_agent.langchain_agent import chain_with_memory

from pydantic import BaseModel


app = FastAPI(
    title="OpenAI Chat API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_openai_responses.router)

class ChainInput(BaseModel):
    question: str
    conversation_id: str

@app.post("/chain")
async def run_chain(input: ChainInput):

    result = await chain_with_memory.ainvoke(
        {"question": input.question},
        config={"configurable": {"session_id": input.conversation_id}},
    )

    return {"output": result}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=False)