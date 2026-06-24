import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="مراسل الذكاء الاصطناعي", page_icon="🤖")
st.title("🤖 مراسل - المساعد الذكي العربي")
st.write("مساعدك العربي الشامل")

# استخدام المفتاح من الإعدادات الآمنة في Streamlit
api_key = st.secrets["GROQ_API_KEY"]

if api_key:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "أنت مساعد ذكي تتحدث العربية بطلاقة وتساعد المستخدمين في مهامهم اليومية."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("كيف أساعدك؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.error("لم يتم العثور على مفتاح API. يرجى التأكد من إضافته في إعدادات Secrets.")
