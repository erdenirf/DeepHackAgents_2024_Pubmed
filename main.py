import streamlit as st
from langchain.chat_models.gigachat import GigaChat
from langchain.chains import RetrievalQA
import dotenv
import os
from services.vectorstore_connect import qdrant_vectorstore

try:
    dotenv.load_dotenv()
except:
    pass

GIGACHAT_API_CREDENTIALS = os.environ.get("GIGACHAT_API_CREDENTIALS")

giga = GigaChat(credentials=GIGACHAT_API_CREDENTIALS,
                scope='GIGACHAT_API_CORP', 
                verify_ssl_certs=False,
                model="GigaChat-Plus",
                profanity_check=False,
                #streaming=True
                )

qa = RetrievalQA.from_llm(llm=giga, retriever=qdrant_vectorstore.as_retriever())

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
    result = qa(question)
    #result = giga(st.session_state["messages"])
    msg = result['result']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)