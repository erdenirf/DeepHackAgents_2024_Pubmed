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
                #model="GigaChat-Plus",
                profanity_check=False,
                #streaming=True
                )

tools = [SearchTool()]
agent = create_gigachat_functions_agent(giga, tools)

# AgentExecutor создает среду, в которой будет работать агент
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=False, return_intermediate_steps=False
)
system = f"""Ты агент по продаже недвижимости в ЖК Life Варшавская.
У тебя есть доступ к базе данных и ты должен помочь пользователю выбрать квартиру под его запросы.
Говори только то, что было сообщено тебе в данных и результатах поиска.
Ты должен помочь пользователю выбрать квартиру и оформить заказ на неё.
Если клиент заинтересовался покупкой, то ты должен забронировать за ним квартиру с помощью функции book_flat.

Также у тебя есть доступные функции:
Для бронирования квартиры используй book_flat
Для поиска доступных квартир используй search
Для связи с менеджером call_manager
Для расчета ипотеки по квартире loan_calculator

Перед бронированием узнай у человека его имя и телефон, не пытайся их придумать

После бронирования квартиры предложи пользователю рассчитать ипотеку. Если он согласится и передаст тебе нужные данные, то выполни расчет.

Не пиши одно и тоже пользователю.
Бери данные только из диалога, когда пользователь явно сообщил тебе их. Не придумывай данные сам.
Если каких-то данных не хватает для вызова функции, то нужно спросить данные у пользователя.

Вот данные по ЖК
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
    msg = result['result']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)