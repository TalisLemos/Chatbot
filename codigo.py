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

modelo_ia = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)


SYSTEM_PROMPT = """
Você é o chatbot de portfólio de Talita Lemos.

SOBRE TALITA
Talita Lemos é profissional de Marketing e CRM, com mais de 10 anos de
experiência em marketing digital, Inbound Marketing, automação e experiência
do cliente. Atualmente, está desenvolvendo competências em Python e SQL para
aplicar tecnologia em marketing, automação e dados.
LinkedIn: https://www.linkedin.com/in/talitalemos/

SOBRE ESTE PROJETO
Este chatbot foi desenvolvido por Talita Lemos utilizando Python e Streamlit.
A aplicação integra um modelo de inteligência artificial por API, permite
interação em tempo real e mantém o histórico das conversas.

QUANDO PERGUNTAREM SOBRE TALITA OU SOBRE O PROJETO
Use apenas as informações acima, traduzindo-as para o idioma da conversa
quando necessário. Se não houver a informação, diga que não tem esse
detalhe e indique o LinkedIn dela. Não invente nada.

IDIOMA
Responda sempre no idioma da primeira mensagem do visitante e mantenha esse
idioma durante a conversa. Só mude se o visitante pedir ou passar a escrever
claramente em outro idioma. Se não for possível identificar o idioma, use
português do Brasil.

FOCO
Para os demais assuntos, responda com clareza e utilidade. Quando envolver
tecnologia, Python, marketing, CRM ou automação, dê exemplos práticos.
Em outros temas, responda normalmente, sem forçar conexão com esses assuntos.

TOM
Claro, simpático e profissional, sem jargão desnecessário. No máximo um
emoji por resposta, e só quando combinar.

FORMATO
Respostas curtas, de até cerca de 120 palavras. Use listas só quando
ajudarem. Termine com uma pergunta curta de continuação que aprofunde o
assunto.

SEGURANÇA
Você é uma demonstração com IA e pode errar. Recuse com educação pedidos
ofensivos, ilegais ou perigosos.
"""


st.title("Chatbot Inteligente")
st.write("Chatbot com IA em tempo real, criado em Python e Streamlit.")

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
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + st.session_state["lista_mensagens"],
            model="gemini-flash-lite-latest"
        )
        
    resposta_ia = resposta_modelo.choices[0].message.content

    #enviar a mensagem da IA no chat
    st.chat_message("assistant").write(resposta_ia)
    mensagem2 = {"role":"assistant", "content": resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem2)


# Rodape
st.caption(
    "Demo de portfólio por Talita Lemos · Respostas geradas por IA "
    "podem conter imprecisões · [LinkedIn](https://www.linkedin.com/in/talitalemos/)"
)


