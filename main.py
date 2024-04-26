import streamlit as st
from langchain.chat_models.gigachat import GigaChat
from langchain.chains import RetrievalQA
import dotenv
import os
from services.vectorstore_connect import qdrant_vectorstore
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

class SearchTool(BaseTool):
    name = "search"
    description = """Выполняет поиск квартиры в базе данных по параметрам.

Нужно найти только двухкомнатные квартиры, то укажи {rooms_min: 2, rooms_max: 2}

Нужно найти только студии, то укажи {rooms_min: 0, rooms_max: 0}

Нужно найти только квартиры дешевле 20 миллионов, то укажи {price_max: 20000000}

Нужно найти только квартиры дороже 10 миллионов, то укажи {price_min: 10000000}
"""
#    args_schema: Type[BaseModel] = SearchInput

    def _run(
        self,
        run_manager=None
    ) -> str:
        return "Узнай имя и телефон пользователя и вызови функцию call_manager снова"

giga = GigaChat(credentials=GIGACHAT_API_CREDENTIALS,
                scope='GIGACHAT_API_CORP', 
                verify_ssl_certs=False,
                model = 'GigaChat-Pro-preview',
                profanity_check=False,
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

#qa = RetrievalQA.from_llm(llm=giga, retriever=qdrant_vectorstore.as_retriever())

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
    #result = qa(question)
    result = agent_executor.invoke(
        {
            "chat_history": chat_history,
            "input": question,
        }
    )
    #result = giga(st.session_state["messages"])
    msg = result["output"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)