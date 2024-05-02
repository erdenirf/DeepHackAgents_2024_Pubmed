import streamlit as st
from langchain.chat_models.gigachat import GigaChat
from typing import Optional, Type
import dotenv
import os
from langchain.pydantic_v1 import BaseModel, Field
from services.retrievers_ensemble_retriever import get_ensemble_retriver
from langchain.tools import BaseTool
from langchain.agents import (
    AgentExecutor,
    create_gigachat_functions_agent,
)
from langchain.agents.gigachat_functions_agent.base import (
    format_to_gigachat_function_messages,
)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

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
        result = get_ensemble_retriver().get_relevant_documents(question)
        
        result_string = "Agent Tool RAG: Найденные статьи:\n\n"
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
    agent=agent, tools=tools, verbose=False, return_intermediate_steps=True
)
system = f"""Ты ИИ-ассистент и справочник по медицине

У тебя есть доступные функции:
Получить RAG context из векторной базы данных
"""  # noqa
chat_history = [SystemMessage(content=system)]

with st.sidebar:
    "Ответы от чат-бота носят справочный характер."

    "Ответы от ИИ-ассистента не являются врачебной рекомендацией, лучше обратиться в мед. организацию."

st.title("💬 Мед чат-бот")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Вас приветствует мед чат-бот"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    result = agent_executor.invoke(
        {
            "chat_history": chat_history,
            "input": question,
        }
    )
    #result = giga(st.session_state["messages"])
    msg = result["output"]
    details = result["intermediate_steps"]
    if len(details) > 0:
        tool_question, tool_answer = details[0]
        st.session_state.messages.append({"role": "assistant", "content": tool_answer})
        st.chat_message("assistant", avatar='🤖').write(tool_answer)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)