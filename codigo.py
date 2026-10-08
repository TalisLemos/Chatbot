#Titulo
#Campo de mensagem (input)
#Quando usuario enviar uma mensagem
    # Mostrar a mensagem na conversa
    # Mandar a mensagem para IA responder
    # Mostrar a resposta da IA

# streamlit e openai
# streamlit run codigo.py /// rodar codigo

import streamlit as st
from openai import OpenAI

modelo_ia = OpenAI(api_key=st.secrets["GEMINI_API_KEY"],
                   base_url="https://generativelanguage.googleapis.com/v1beta/openai")

st.title("Chatbot Inteligente")
st.write("Chatbot com IA em tempo real, criado em Python e Streamlit por Talita Lemos.")

# criar historico de mensagems
if not "lista_mensagens" in st.session_state:
    st.session_state["lista_mensagens"] = []

mensagem_usuario = st.chat_input("Escreva sua mensagem aqui")

pergunta1 = False

if not st.session_state["lista_mensagens"]:
    st.markdown("""
    **Olá! 👋**

    Faça uma pergunta para começar a conversa.
    """)

    pergunta1 = st.button("Como posso usar Python no marketing?")

if pergunta1:
    mensagem_usuario = "Como posso usar Python no marketing?"

for mensagem in st.session_state["lista_mensagens"]:
    quem_enviou = mensagem["role"]
    texto_mensagem = mensagem["content"]
    st.chat_message(quem_enviou).write(texto_mensagem)


if mensagem_usuario:
    #exibir mensagem
    # user -> usuario
    # assistant -> robo/ia
    st.chat_message("user").write(mensagem_usuario)
    mensagem1 = {"role":"user", "content": mensagem_usuario}
    st.session_state["lista_mensagens"].append(mensagem1)

    # pegar a resposta da IA
    with st.spinner("O assistente está pensando..."):
        resposta_modelo = modelo_ia.chat.completions.create(
            messages=st.session_state["lista_mensagens"],
            model="gemini-flash-lite-latest"
        )

    resposta_ia = resposta_modelo.choices[0].message.content

    #enviar a mensagem da IA no chat
    st.chat_message("assistant").write(resposta_ia)
    mensagem2 = {"role":"assistant", "content": resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem2)


# Rodape
st.caption(
    "Demo de portfólio por Talita Lemos · Respostas geradas por IA, "
    "podem conter imprecisões · [LinkedIn](https://www.linkedin.com/in/talitalemos/)"
)


