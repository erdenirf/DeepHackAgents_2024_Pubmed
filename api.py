#!/usr/bin/env python
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models.gigachat import GigaChat
from langchain_core.prompts import PromptTemplate
import dotenv
import os
from langserve import add_routes
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import (
    AgentExecutor,
    create_gigachat_functions_agent,
)
from langchain.agents.gigachat_functions_agent.base import (
    format_to_gigachat_function_messages,
)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.pydantic_v1 import BaseModel, Field
from services.vectorstore_connect import qdrant_vectorstore
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

try:
    dotenv.load_dotenv()
except:
    pass

GIGACHAT_API_CREDENTIALS = os.environ.get("GIGACHAT_API_CREDENTIALS")

class SearchInput(BaseModel):
    question: str = Field(
        description="вопрос пользователя"
    )

class SearchTool(BaseTool):
    name = "search"
    description = """Выполняет поиск вопроса пользователя по медицине в базе данных 
"""
    args_schema: Type[BaseModel] = SearchInput

    def _run(
        self,
        question: str,
        run_manager=None
    ) -> str:
        msg = f"Ищем в базе статей вопрос: {question} "
        result = qdrant_vectorstore.as_retriever().get_relevant_documents(question)
        
        result_string = "Найденные статьи:\n\n"
        for index, item in enumerate(result):
            result_string += f"{index+1} \t" + item.page_content
            result_string += "\n" + item.metadata['source'] + "\n\n"

        return result_string

giga = GigaChat(credentials=GIGACHAT_API_CREDENTIALS,
                scope='GIGACHAT_API_CORP', 
                verify_ssl_certs=False,
                model = 'GigaChat-Pro-preview',
                profanity_check=False,
                timeout=600,
                #streaming=True
                )

tools = [SearchTool()]
agent = create_gigachat_functions_agent(giga, tools)

# AgentExecutor создает среду, в которой будет работать агент
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=False, return_intermediate_steps=False
)
system = f"""Ты ИИ-ассистент и справочник по медицине

У тебя есть доступные функции:
Получить RAG context из векторной базы данных
"""  # noqa
chat_history = [SystemMessage(content=system)]

app = FastAPI(
  title="GigaChain Server",
  version="1.0",
  description="Простой API-сервер, использующий runnable-интерфейсы GigaChain",
)
retriever = qdrant_vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content + "\n" + doc.metadata['source'] for doc in docs)

template = """Ты ИИ-ассистент и справочник по медицине

Возьми ответ из указанных ниже источников научных статей по медицине:

{context}

Вопрос: {question}

Также в ответе выведи источники из базы данных

Полезный ответ:"""
prompt = PromptTemplate.from_template(template)
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | giga
)
add_routes(
    app,
    rag_chain,
    path="/gigachat",
) 

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)