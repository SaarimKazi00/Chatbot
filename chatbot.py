import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def ask_gemini(user_question):
    model = genai.GenerativeModel('gemini-pro')

    prompt = f'Given the user input provide the most appropriate highly detailed response also provide short examples if possible in text format only, thankyou. {user_question}'

    response_gemini = model.generate_content(prompt)
    response_gemini = response_gemini.text.replace('**', '').replace('*', '•')

    return response_gemini


def format_response(response):
    lines = response.split('•')
    lines = [line.strip() for line in lines if line.strip()]
    formatted_lines = []
    for line in lines:
        if line.isdigit():
            formatted_lines.append(f"**{line}.**")
        else:
            formatted_lines.append(f"- {line}")
    return '\n'.join(formatted_lines)


def main():
    st.set_page_config("Chat Bot")
    st.header("Chat Bot🤖")

    user_question = st.text_input("Ask your question:", "")

    if st.button("Submit"):
        with st.spinner("Generating response..."):
            raw_gemini_response = ask_gemini(user_question)

            formatted_gemini_response = format_response(raw_gemini_response)

            st.markdown(formatted_gemini_response, unsafe_allow_html=True)


if __name__ == "__main__":
    main()