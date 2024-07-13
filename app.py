import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceEndpoint


load_dotenv()
title = os.getenv('PROJECT_TITLE')
st.set_page_config(page_title=title, page_icon="✈️")
st.title(title)
prompt = ChatPromptTemplate.from_template(os.getenv('TEMPLATE'))

def get_response(user_query, chat_history):
    llm = HuggingFaceEndpoint(
        huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN"),
        repo_id=os.getenv("MODEL_BASE_REPO_ID"),
        task=os.getenv("TASK")
    )
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "chat_history": chat_history,
        "user_query": user_query
    })
    return response

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am Prayāṇa AI. How can I help you?"),
    ]


for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)


user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    response = get_response(user_query, st.session_state.chat_history)

    # Remove any unwanted prefixes from the response
    response = response.replace("AI response:", "").replace("chat response:", "").replace("bot response:", "").strip()
    response = response.replace("AI Assistant:", "").replace("AI", "").replace("Assistant", "").replace(":", "")

    with st.chat_message("AI"):
        st.write(response)

    st.session_state.chat_history.append(AIMessage(content=response))
