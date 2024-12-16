import streamlit as st
from datetime import datetime
from database import criar_usuario, criar_tarefa, excluir_tarefa, listar_tarefas, autenticar_usuario
import pandas as pd

# Função para registro de usuário
def registrar_usuario():
    username = st.text_input("Escolha um nome de usuário")
    password = st.text_input("Escolha uma senha", type='password')

    if st.button("Registrar"):
        usuario = criar_usuario(username, password)
        if usuario:
            st.success(f"Usuário {username} registrado com sucesso!")
        else:
            st.error("Nome de usuário já existe. Tente outro.")

# Função para login de usuário
def login_usuario():
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type='password')

    if st.button("Entrar"):
        usuario = autenticar_usuario(username, password)
        if usuario:
            st.session_state.usuario_id = usuario.id
            st.session_state.username = username
            st.success(f"Bem-vindo, {username}!")
        else:
            st.error("Usuário ou senha incorretos. Tente novamente.")

# Função para exibir e gerenciar tarefas
def gerenciar_tarefas():
    usuario_id = st.session_state.usuario_id
    tarefas = listar_tarefas(usuario_id)

    if tarefas:
        tarefas_df = pd.DataFrame([{
            'ID': t.id, 'Título': t.titulo, 'Status': t.status, 'Data de Vencimento': t.data_vencimento
        } for t in tarefas])
        st.table(tarefas_df)

        tarefa_id = st.selectbox("Escolha uma tarefa para excluir", tarefas_df['ID'])
        if st.button("Excluir Tarefa"):
            if excluir_tarefa(tarefa_id):
                st.success("Tarefa excluída com sucesso!")
            else:
                st.error("Erro ao excluir tarefa.")
    else:
        st.info("Você não tem tarefas cadastradas.")

# Função para adicionar novas tarefas
def adicionar_tarefa():
    titulo = st.text_input("Título da Tarefa")
    descricao = st.text_area("Descrição da Tarefa")
    status = st.selectbox("Status", ["to_do", "doing", "done"])
    data_vencimento = st.date_input("Data de Vencimento", min_value=datetime.today())

    if st.button("Adicionar Tarefa"):
        criar_tarefa(st.session_state.usuario_id, titulo, descricao, status, data_vencimento)
        st.success("Tarefa adicionada com sucesso!")

# Função principal
def main():
    st.title("Gerenciador de Tarefas")

    if "usuario_id" not in st.session_state:
        escolha = st.radio("Escolha uma opção", ("Login", "Registrar"))
        if escolha == "Login":
            login_usuario()
        elif escolha == "Registrar":
            registrar_usuario()
    else:
        st.sidebar.write(f"Olá, {st.session_state.username}")
        if st.sidebar.button("Sair"):
            del st.session_state["usuario_id"]
            del st.session_state["username"]
            st.experimental_rerun()

        st.subheader("Adicionar Nova Tarefa")
        adicionar_tarefa()

        st.subheader("Minhas Tarefas")
        gerenciar_tarefas()

if __name__ == "__main__":
    main()
