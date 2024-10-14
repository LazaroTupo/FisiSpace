# crud.py
from sqlalchemy.orm import Session
from models import Estudiante, Curso, Seccion
import schemas

# Estudiante

def get_estudiantes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Estudiante).offset(skip).limit(limit).all()

def get_estudiante(db: Session, estudiante_id: int):
    return db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()

def get_estudiante_por_codigo(db: Session, codigo_estudiante: str):
    return db.query(Estudiante).filter(Estudiante.codigo == codigo_estudiante).first()

def create_estudiante(db: Session, estudiante: schemas.EstudianteCreate):
    db_estudiante = Estudiante(**estudiante.dict())
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante

def update_estudiante(db: Session, estudiante_id: int, estudiante: schemas.EstudianteUpdate):
    db_estudiante = get_estudiante(db, estudiante_id)
    for key, value in estudiante.dict().items():
        setattr(db_estudiante, key, value)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante

def delete_estudiante(db: Session, estudiante_id: int):
    db_estudiante = get_estudiante(db, estudiante_id)
    db.delete(db_estudiante)
    db.commit()
    return db_estudiante

# Curso

def get_cursos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Curso).offset(skip).limit(limit).all()

def get_curso(db: Session, curso_id: int):
    return db.query(Curso).filter(Curso.id == curso_id).first()

def create_curso(db: Session, curso: schemas.CursoCreate):
    db_curso = Curso(**curso.dict())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

def update_curso(db: Session, curso_id: int, curso: schemas.CursoUpdate):
    db_curso = get_curso(db, curso_id)
    for key, value in curso.dict().items():
        setattr(db_curso, key, value)
    db.commit()
    db.refresh(db_curso)
    return db_curso

def delete_curso(db: Session, curso_id: int):
    db_curso = get_curso(db, curso_id)
    db.delete(db_curso)
    db.commit()
    return db_curso

# Salón

def get_salon_por_curso(db: Session, nombre_curso: str, codigo_curso: str, numero_seccion: str):
    # Buscar la sección que corresponde al curso y sección indicados
    return db.query(Seccion).join(Curso).filter(
        Curso.nombre == nombre_curso,
        Curso.codigo == codigo_curso,
        Seccion.numero == numero_seccion
    ).first()