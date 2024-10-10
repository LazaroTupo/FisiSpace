## Requisitos

Asegúrate de tener instalado lo siguiente antes de comenzar:

- Python 3.10 o superior
- Pip (para gestionar dependencias)

## Instalación

1. Clona este repositorio en tu máquina local o descarga los archivos.

```bash
git clone https://github.com/LazaroTupo/FisiSpace.git
cd FisiSpace
```

## Crear un entorno virtual para evitar conflictos con tus otros proyectos
1. Ejecuta el siguiente comando para crearlo
```
python -m venv .venv
```
2. Para activarlo
En linux
  ```
  source .venv/bin/activate
  ```
En Windows
  ```
  .venv\Scripts\activate
  ```
3. Instala las dependencias del proyecto:
```
pip install -r requirements.txt
```
## Ejecución
Para iniciar el servidor FastAPI, ejecuta el siguiente comando:
```
uvicorn main:app --reload
```
Ruta: http://127.0.0.1:8000/docs
