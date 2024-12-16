import streamlit as st
import psycopg2
import os
from datetime import datetime

# Conexão com o banco de dados PostgreSQL usando variável de ambiente do Railway
DATABASE_URL = os.getenv("DATABASE_URL")

# Conectar ao PostgreSQL
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# Criando um cursor para interagir com o banco de dados
cur = conn.cursor()

# Criar a tabela (se ela não existir) - Adicionando o campo status e data de criação
cur.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        descricao TEXT,
        status TEXT NOT NULL DEFAULT 'To Do',  -- Campo de status
        concluida BOOLEAN NOT NULL DEFAULT FALSE,
        data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  -- Data de criação
    )
""")
conn.commit()

# Função para criar uma tarefa
def criar_tarefa(nome, descricao, status):
    cur.execute("""
        INSERT INTO tarefas (nome, descricao, status, concluida) 
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (nome, descricao, status, False))
    tarefa_id = cur.fetchone()[0]
    conn.commit()
    return tarefa_id

# Função para listar tarefas
def listar_tarefas():
    cur.execute("SELECT id, nome, descricao, status, concluida, data_criacao FROM tarefas")
    return cur.fetchall()

# Função para excluir tarefa
def excluir_tarefa(tarefa_id):
    cur.execute("DELETE FROM tarefas WHERE id = %s", (tarefa_id,))
    conn.commit()

# Função para marcar tarefa como concluída
def concluir_tarefa(tarefa_id):
    cur.execute("UPDATE tarefas SET concluida = TRUE WHERE id = %s", (tarefa_id,))
    conn.commit()

# Função para atualizar o status da tarefa
def atualizar_status(tarefa_id, novo_status):
    cur.execute("UPDATE tarefas SET status = %s WHERE id = %s", (novo_status, tarefa_id))
    conn.commit()

# Função para autenticar o usuário
def autenticar_usuario():
    if 'username' not in st.session_state:
        st.session_state.username = None

    if st.session_state.username is None:
        with st.form(key="login_form"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            submit_button = st.form_submit_button(label="Entrar")
            
            if submit_button:
                if usuario == "admin" and senha == "senha123":  # Substitua por lógica real
                    st.session_state.username = usuario
                    st.success(f"Bem-vindo, {usuario}!")
                else:
                    st.error("Usuário ou senha inválidos.")
    else:
        st.sidebar.write(f"Bem-vindo, {st.session_state.username}!")
        if st.sidebar.button("Sair"):
            st.session_state.username = None
            st.experimental_rerun()

# Função para exibir o menu e retornar a página escolhida
def exibir_menu():
    menu = ["Home", "Tarefas"]
    escolha = st.sidebar.selectbox("Menu", menu)

    if escolha == "Home":
        exibir_home()
    elif escolha == "Tarefas":
        exibir_tarefas()

# Função para a página inicial
def exibir_home():
    st.title("Bem-vindo ao Gerenciador de Tarefas")
    st.write("Aqui você pode criar, gerenciar e monitorar suas tarefas.")

# Função para exibir a página de tarefas
def exibir_tarefas():
    st.title("Gerenciador de Tarefas")

    # Formulário para criar uma nova tarefa
    with st.form(key='task_form'):
        nome = st.text_input("Nome da Tarefa")
        descricao = st.text_area("Descrição")
        status = st.selectbox("Status", ["To Do", "Doing", "Done"])  # Campo de status
        submit_button = st.form_submit_button(label="Criar Tarefa")

        if submit_button:
            if nome and descricao:
                tarefa_id = criar_tarefa(nome, descricao, status)
                st.success(f"Tarefa criada com sucesso! ID: {tarefa_id}")
            else:
                st.error("Por favor, preencha todos os campos.")

    # Exibir tarefas existentes
    tarefas = listar_tarefas()

    if tarefas:
        for tarefa in tarefas:
            id_tarefa, nome, descricao, status, concluida, data_criacao = tarefa
            st.write(f"**ID**: {id_tarefa}, **Nome**: {nome}, **Descrição**: {descricao}, **Status**: {status}, **Concluída**: {concluida}, **Data de Criação**: {data_criacao.strftime('%d/%m/%Y %H:%M:%S')}")

            # Botão para excluir tarefa
            if st.button(f"Excluir Tarefa {id_tarefa}"):
                excluir_tarefa(id_tarefa)
                st.experimental_rerun()

            # Botão para marcar tarefa como concluída
            if not concluida and st.button(f"Concluir Tarefa {id_tarefa}"):
                concluir_tarefa(id_tarefa)
                st.experimental_rerun()

            # Opção para atualizar o status da tarefa
            novo_status = st.selectbox(f"Atualizar status da Tarefa {id_tarefa}", ["To Do", "Doing", "Done"])
            if st.button(f"Alterar Status para {novo_status} para Tarefa {id_tarefa}"):
                atualizar_status(id_tarefa, novo_status)
                st.experimental_rerun()

# Função principal da interface do Streamlit
def app():
    autenticar_usuario()
    
    if st.session_state.username:
        exibir_menu()

if __name__ == "__main__":
    app()
