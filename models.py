from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base para as classes do SQLAlchemy
Base = declarative_base()

# Definição da tabela de usuários
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    tarefas = relationship("Tarefa", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id}, username={self.username})>"

# Definição da tabela de tarefas
class Tarefa(Base):
    __tablename__ = 'tarefas'

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    status = Column(String, nullable=False)  # to_do, doing, done
    data_vencimento = Column(Date, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship("Usuario", back_populates="tarefas")

    def __repr__(self):
        return f"<Tarefa(id={self.id}, titulo={self.titulo}, status={self.status})>"
