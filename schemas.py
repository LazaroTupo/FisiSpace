from pydantic import BaseModel

class EstudianteBase(BaseModel):
    codigo: str
    apellidos_nombre: str
    dni: str
    correo: str

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteUpdate(EstudianteBase):
    pass

class Estudiante(EstudianteBase):
    id: int

    class Config:
        from_attributes = True

class CursoBase(BaseModel):
    ciclo: str
    codigo: str
    nombre: str
    creditos: float

class CursoCreate(CursoBase):
    pass

class CursoUpdate(CursoBase):
    pass

class Curso(CursoBase):
    id: int

    class Config:
        from_attributes = True
