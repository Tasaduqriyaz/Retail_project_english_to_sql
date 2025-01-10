import streamlit as st
from langchain_helper import chain

st.title("Retail t_shirt store QA 🥼:")
question= st.text_input("Question ")

if question:
    response=chain()
    response=response.run(question)
    st.subheader("Answer")
    st.write(response)


