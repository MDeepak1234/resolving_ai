
import streamlit as st
import uuid

from config import APP_NAME
from database.db import create_tables, save_message, get_chat_history
from graph.workflow import support_workflow

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖"
)

st.title("🤖 AI Customer Support Assistant")
st.caption("Your intelligent ShopEase customer support assistant.")

create_tables()

# Maintain session ID in browser URL
if "session_id" not in st.query_params:
    st.query_params["session_id"] = str(uuid.uuid4())

session_id = st.query_params["session_id"]

# Load conversation history
if "messages" not in st.session_state:
    history = get_chat_history(session_id)

    st.session_state.messages = []

    for message in history:
        st.session_state.messages.append({
            "role": message["role"],
            "content": message["content"]
        })

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept new customer message
if prompt := st.chat_input("How can I help you today?"):

    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    save_message(session_id, "user", prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("assistant"):

        with st.spinner("Understanding your request..."):

            try:
                # Prepare LangGraph input
                initial_state = {
                    "customer_message": prompt,
                    "chat_history": st.session_state.messages[:-1],
                    "intent": "",
                    "order_id": "",
                    "answer": "",
                    "sources": []
                }

                # Execute LangGraph workflow
                result = support_workflow.invoke(initial_state)

                answer = result["answer"]

                st.markdown(answer)

                # Display source documents
                if result["sources"]:
                    with st.expander("View Sources"):
                        for source in result["sources"]:
                            st.write(source)

                # Save assistant response
                save_message(session_id, "assistant", answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")
