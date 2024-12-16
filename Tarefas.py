import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            tarefa TEXT,
            status TEXT,
            prioridade TEXT,
            prazo TEXT
        )
    """)
    conn.commit()
    return conn

# Adicionar uma nova tarefa ao banco de dados
def add_task(conn, usuario, tarefa, status, prioridade, prazo):
    c = conn.cursor()
    c.execute("INSERT INTO tasks (usuario, tarefa, status, prioridade, prazo) VALUES (?, ?, ?, ?, ?)",
              (usuario, tarefa, status, prioridade, prazo))
    conn.commit()

# Carregar tarefas do banco de dados
def load_tasks(conn, usuario):
    c = conn.cursor()
    c.execute("SELECT id, tarefa, status, prioridade, prazo FROM tasks WHERE usuario = ?", (usuario,))
    return pd.DataFrame(c.fetchall(), columns=["ID", "Tarefa", "Status", "Prioridade", "Prazo"])

# Excluir uma tarefa do banco de dados
def delete_task(conn, task_id):
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

# Alterar uma tarefa existente
def update_task(conn, task_id, tarefa, status, prioridade, prazo):
    c = conn.cursor()
    c.execute("""
        UPDATE tasks SET tarefa = ?, status = ?, prioridade = ?, prazo = ? WHERE id = ?
    """, (tarefa, status, prioridade, prazo, task_id))
    conn.commit()

# Gerar gráfico de contagem por status
def plot_status_count(tasks):
    status_counts = tasks['Status'].value_counts()
    fig, ax = plt.subplots()
    status_counts.plot(kind='bar', ax=ax)
    ax.set_title('Contagem de Tarefas por Status')
    ax.set_xlabel('Status')
    ax.set_ylabel('Contagem')
    st.pyplot(fig)

# Gerar gráfico de contagem por prioridade
def plot_priority_count(tasks):
    priority_counts = tasks['Prioridade'].value_counts()
    fig, ax = plt.subplots()
    priority_counts.plot(kind='bar', ax=ax)
    ax.set_title('Contagem de Tarefas por Prioridade')
    ax.set_xlabel('Prioridade')
    ax.set_ylabel('Contagem')
    st.pyplot(fig)

# Aplicação principal
def main():
    st.title("Gerenciador de Projetos")
    conn = init_db()

    # Autenticação simples
    st.sidebar.header("Autenticação")
    usuario = st.sidebar.text_input("Digite seu nome de usuário", "Convidado")
    if not usuario:
        st.warning("Por favor, insira um nome de usuário para continuar.")
        st.stop()

    # Menu
    st.sidebar.header("Menu")
    option = st.sidebar.selectbox("Escolha uma ação", ["Visualizar Tarefas", "Adicionar Nova Tarefa", "Alterar Tarefa", "Excluir Tarefa"])

    if option == "Visualizar Tarefas":
        st.subheader(f"Tarefas de {usuario}")
        tasks = load_tasks(conn, usuario)
        if tasks.empty:
            st.info("Nenhuma tarefa encontrada.")
        else:
            st.dataframe(tasks)
            # Exibir gráficos
            plot_status_count(tasks)
            plot_priority_count(tasks)

    elif option == "Adicionar Nova Tarefa":
        st.subheader("Adicionar Nova Tarefa")
        task_name = st.text_input("Nome da Tarefa")
        task_status = st.selectbox("Status", ["To Do", "Doing", "Done"])
        task_priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        task_deadline = st.date_input("Prazo")

        if st.button("Salvar Tarefa"):
            if task_name.strip():
                add_task(conn, usuario, task_name, task_status, task_priority, str(task_deadline))
                st.success("Tarefa adicionada com sucesso!")
            else:
                st.error("O nome da tarefa não pode ser vazio.")

    elif option == "Alterar Tarefa":
        st.subheader("Alterar Tarefa")
        tasks = load_tasks(conn, usuario)
        if tasks.empty:
            st.info("Nenhuma tarefa encontrada para alterar.")
        else:
            task_id = st.selectbox("Selecione o ID da tarefa para alterar", tasks["ID"])
            selected_task = tasks[tasks["ID"] == task_id].iloc[0]
            
            task_name = st.text_input("Nome da Tarefa", selected_task['Tarefa'])
            task_status = st.selectbox("Status", ["To Do", "Doing", "Done"], index=["To Do", "Doing", "Done"].index(selected_task['Status']))
            task_priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"], index=["Baixa", "Média", "Alta"].index(selected_task['Prioridade']))
            task_deadline = st.date_input("Prazo", pd.to_datetime(selected_task['Prazo']))

            if st.button("Atualizar Tarefa"):
                if task_name.strip():
                    update_task(conn, task_id, task_name, task_status, task_priority, str(task_deadline))
                    st.success("Tarefa atualizada com sucesso!")
                else:
                    st.error("O nome da tarefa não pode ser vazio.")

    elif option == "Excluir Tarefa":
        st.subheader("Excluir Tarefa")
        tasks = load_tasks(conn, usuario)
        if tasks.empty:
            st.info("Nenhuma tarefa encontrada para exclusão.")
        else:
            task_id = st.selectbox("Selecione o ID da tarefa para excluir", tasks["ID"])
            if st.button("Excluir"):
                delete_task(conn, task_id)
                st.success("Tarefa excluída com sucesso!")

if __name__ == "__main__":
    main()
