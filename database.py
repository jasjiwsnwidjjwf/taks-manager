from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Usuario, Tarefa
from sqlalchemy.exc import IntegrityError

# Conexão com o banco de dados SQLite
DATABASE_URL = "sqlite:///tarefas.db"  # Usando SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

def criar_usuario(username, password):
    session = Session()
    novo_usuario = Usuario(username=username, password=password)
    session.add(novo_usuario)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return None  # Caso o nome de usuário já exista
    return novo_usuario

def autenticar_usuario(username, password):
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.username == username, Usuario.password == password).first()
    return usuario

def criar_tarefa(usuario_id, titulo, descricao, status, data_vencimento):
    session = Session()
    nova_tarefa = Tarefa(titulo=titulo, descricao=descricao, status=status, data_vencimento=data_vencimento, usuario_id=usuario_id)
    session.add(nova_tarefa)
    session.commit()

def excluir_tarefa(tarefa_id):
    session = Session()
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if tarefa:
        session.delete(tarefa)
        session.commit()
        return True
    return False

def listar_tarefas(usuario_id):
    session = Session()
    tarefas = session.query(Tarefa).filter(Tarefa.usuario_id == usuario_id).all()
    return tarefas
