from sqlalchemy import Column, BigInteger, String, Float, SmallInteger, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Curso(Base):
    __tablename__ = "Curso"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    ciclo = Column(String, nullable=False)
    codigo = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    creditos = Column(Float, nullable=False)

class Aula(Base):
    __tablename__ = "Aula"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    capacidad = Column(SmallInteger, nullable=False)
    tipo = Column(String, nullable=False)

class Estudiante(Base):
    __tablename__ = "Estudiante"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String, nullable=False)
    apellidos_nombre = Column(String, nullable=False)
    dni = Column(String, nullable=False)
    correo = Column(String, nullable=False)

class Seccion(Base):
    __tablename__ = "Seccion"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id_curso = Column(BigInteger, ForeignKey('Curso.id'), nullable=False)
    id_aula_teoria = Column(BigInteger, ForeignKey('Aula.id'))
    id_aula_labo = Column(BigInteger, ForeignKey('Aula.id'))
    numero = Column(String, nullable=False)
    code_docente = Column(String, nullable=False)
    docente = Column(String, nullable=False)
    tope = Column(SmallInteger, nullable=False)
    dia_teoria = Column(String, nullable=False)
    horario_teoria = Column(String, nullable=False)
    dia_labo = Column(String, nullable=False)
    horario_labo = Column(String, nullable=False)

    curso = relationship("Curso")
    aula_teoria = relationship("Aula", foreign_keys=[id_aula_teoria])
    aula_labo = relationship("Aula", foreign_keys=[id_aula_labo])

class Matricula(Base):
    __tablename__ = "Matricula"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id_estudiante = Column(BigInteger, ForeignKey('Estudiante.id'), nullable=False)
    id_seccion = Column(BigInteger, ForeignKey('Seccion.id'), nullable=False)
    fecha = Column(Date, nullable=False)
    estado = Column(String, nullable=False)

    estudiante = relationship("Estudiante")
    seccion = relationship("Seccion")
