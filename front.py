import streamlit as st
from LLM_Routing import route_user_question  # your existing routing function
from Functions import momentum, macd, rsi, volatility, volume  # your existing tools

st.set_page_config(page_title="Agentic Stock Copilot", layout="wide")
st.title("Agentic Stock Copilot")
st.write("Type any stock-related question below. The AI will use your tools to answer.")


user_question = st.text_input(
    "Ask a stock question:",
    placeholder="e.g., 'What is the momentum of NVDA?'"
)

if st.button("Analyze"):
    if not user_question.strip():
        st.warning("Please type a question.")
    else:
        try:
            # Call the existing routing function from llm_routing.py
            # It already handles LLM + tool execution
            answer = route_user_question(user_question)
            st.subheader("Agentic Response")
            st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")