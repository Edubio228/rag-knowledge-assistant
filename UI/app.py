import streamlit as st
import requests

st.title("AI Knowledge Assistant")

question = st.text_input("Ask a question about your documents:")
if st.button("Ask"):
    response = requests.post(
        "http://localhost:8000/ask",
        json={"question": question, "top_k": 3}
    )
    if response.status_code == 200:
        data = response.json()
        st.write("### Answer")
        st.write(data["answer"])
        st.write("### Sources")
        for citation in data["citations"]:
            st.write(f"📄 {citation['source']}: {citation['chunk'][:100]}...")