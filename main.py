from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Estudiante, Curso, Base
from database import SessionLocal, engine
import crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para verifiacr el codigo de estudiante

@app.get("/estudiantes/verificar/{codigo_estudiante}")
def verificar_codigo_estudiante(codigo_estudiante: str, db: Session = Depends(get_db)):
    estudiante = crud.get_estudiante_by_codigo(db, codigo_estudiante=codigo_estudiante)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"message": "Código válido", "estudiante_id": estudiante.id}

# Ruta para devolver las aulas de un curso por su nombre, codigo y seccion

@app.get("/cursos/salon/", response_model=schemas.CursoSalones)
def obtener_salon_por_curso(nombre_curso: str, codigo_curso: str, numero_seccion: str, db: Session = Depends(get_db)):
    seccion = crud.get_salon_por_curso(db, nombre_curso=nombre_curso, codigo_curso=codigo_curso, numero_seccion=numero_seccion)
    
    if seccion is None:
        raise HTTPException(status_code=404, detail="Sección no encontrada para el curso indicado")
    
    return {
        "salon_teoria": seccion.aula_teoria.nombre if seccion.aula_teoria else "No asignado",
        "salon_laboratorio": seccion.aula_labo.nombre if seccion.aula_labo else "No asignado"
    }

# Rutas para Estudiantes

@app.get("/estudiantes/")
def read_estudiantes(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    estudiantes = crud.get_estudiantes(db, skip=skip, limit=limit)
    return estudiantes

@app.get("/estudiantes/{estudiante_id}", response_model=schemas.Estudiante)
def read_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    estudiante = crud.get_estudiante(db, estudiante_id=estudiante_id)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

@app.post("/estudiantes/", response_model=schemas.Estudiante)
def create_estudiante(estudiante: schemas.EstudianteCreate, db: Session = Depends(get_db)):
    return crud.create_estudiante(db=db, estudiante=estudiante)

@app.put("/estudiantes/{estudiante_id}", response_model=schemas.Estudiante)
def update_estudiante(estudiante_id: int, estudiante: schemas.EstudianteUpdate, db: Session = Depends(get_db)):
    db_estudiante = crud.get_estudiante(db, estudiante_id=estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return crud.update_estudiante(db=db, estudiante_id=estudiante_id, estudiante=estudiante)

@app.delete("/estudiantes/{estudiante_id}", response_model=schemas.Estudiante)
def delete_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    db_estudiante = crud.get_estudiante(db, estudiante_id=estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    crud.delete_estudiante(db=db, estudiante_id=estudiante_id)
    return db_estudiante

# Rutas para Cursos

@app.get("/cursos/", response_model=list[schemas.Curso])
def read_cursos(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    cursos = crud.get_cursos(db, skip=skip, limit=limit)
    return cursos

@app.get("/cursos/{curso_id}", response_model=schemas.Curso)
def read_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = crud.get_curso(db, curso_id=curso_id)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@app.post("/cursos/", response_model=schemas.Curso)
def create_curso(curso: schemas.CursoCreate, db: Session = Depends(get_db)):
    return crud.create_curso(db=db, curso=curso)

@app.put("/cursos/{curso_id}", response_model=schemas.Curso)
def update_curso(curso_id: int, curso: schemas.CursoUpdate, db: Session = Depends(get_db)):
    db_curso = crud.get_curso(db, curso_id=curso_id)
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return crud.update_curso(db=db, curso_id=curso_id, curso=curso)

@app.delete("/cursos/{curso_id}", response_model=schemas.Curso)
def delete_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = crud.get_curso(db, curso_id=curso_id)
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    crud.delete_curso(db=db, curso_id=curso_id)
    return db_curso
