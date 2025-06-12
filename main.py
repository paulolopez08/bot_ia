import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi chat de IA", page_icon="🤖")

MODELOS = ['llama3-8b-8192' , 'llama3-70b-8192' , 'mixtral-8x7b-32768']

def configurar_modelo(cliente, modelo, mensaje):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role":"user", "content":mensaje}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state["mensajes"] = []

def crear_usuario_gorq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_pagina():
    st.title("Mi chatbot")
    st.sidebar.title("Configuracion de la IA")

    elegirModelo = st.sidebar.selectbox('Elegir un Modelo', options=MODELOS)

    return elegirModelo

def actualizar_historial(rol,contenido,avatar):
    st.session_state.mensajes.append({"role":rol,"content":contenido,"avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"],avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=600,border=True)
    with contenedorDelChat:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa
def main():
    modelo = configurar_pagina()

    clienteUsuario = crear_usuario_gorq()
    inicializar_estado()

    mensajeDeEntrada = st.chat_input('Escribi tu mensaje')
    mensajes = []
    area_chat()
    if mensajeDeEntrada:
        actualizar_historial("user", mensajeDeEntrada,"👨")

        chat_completo = configurar_modelo(clienteUsuario, modelo,mensajeDeEntrada)

        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
            actualizar_historial("assitant",respuesta_completa,"🤖")
        st.rerun()

if __name__ == "__main__":
    main()