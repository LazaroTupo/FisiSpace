from sqlalchemy import create_engine, Column, BigInteger, String, Float, Date, SmallInteger, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from readEstudiantes import main as get_estudiantes
from readpdfCURSOS import main as get_cursos

DATABASE_URL = "postgresql://postgres.fsbjywdcpewilwhfvnyg:UaDv67yM5shjBI8L@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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


def reiniciar_tablas():
    # Eliminar todas las tablas si existen
    Base.metadata.drop_all(bind=engine)
    # Volver a crear todas las tablas
    Base.metadata.create_all(bind=engine)

def insertar_estudiantes(session, estudiantes_data):
    for estudiante in estudiantes_data:
        nuevo_estudiante = Estudiante(
            codigo=estudiante['codigo'],
            apellidos_nombre=estudiante['apellidos_nombre'],
            dni=estudiante['dni'],
            correo=estudiante['correo']
        )
        session.add(nuevo_estudiante)
    session.commit()

def insertar_cursos_y_secciones(session, cursos_data):
    for curso_data in cursos_data:
        curso = Curso(
            ciclo=curso_data['ciclo'],
            codigo=curso_data['codigo'],
            nombre=curso_data['nombre'],
            creditos=curso_data['creditos']
        )
        session.add(curso)
        session.flush()  # Necesario para obtener el ID del curso

        seccion = Seccion(
            id_curso=curso.id,
            id_aula_teoria=None,  # Asigna el ID del aula de teoría si está disponible
            id_aula_labo=None,  # Asigna el ID del aula de laboratorio si está disponible
            numero=curso_data['seccion'],
            code_docente=curso_data['codigo_docente'],
            docente=curso_data['docente'],
            tope=curso_data['tope'],
            dia_teoria=curso_data['dia_teoria'],
            horario_teoria=curso_data['horario_teoria'],
            dia_labo=curso_data['dia_laboratorio'],
            horario_labo=curso_data['horario_laboratorio']
        )
        session.add(seccion)
    session.commit()

# Reiniciar todas las tablas
# reiniciar_tablas()

# Obtener los datos de los estudiantes desde el PDF
pdf_file_path = r"D:\2023 FISI.pdf"
#pdf_file_path = r"D:\Programacion_Asignaturas.pdf"
data = get_estudiantes(pdf_file_path)

# Crear una sesión y insertar los datos
session = SessionLocal()
insertar_estudiantes(session, data)
session.close()

print("Datos de estudiantes insertados exitosamente.")
