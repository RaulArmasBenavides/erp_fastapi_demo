Ejecutar docker-compose

# Primera opción Ejecutar con docker compose ( Recomendable) 

docker compose up -d --build

<img width="1522" height="151" alt="image" src="https://github.com/user-attachments/assets/0e26deba-8b75-414e-8097-3057e3baad1d" />



# Segunda opción Ejecutar con python instalado local mente
## 1) Usa la versión de Python del proyecto (pyenv)
pyenv local 3.9.13
pyenv exec python -V

## 2) Crea/activa un virtualenv (si no existe)
Ubicate en la ruta del proyecto y crea un entorno virtual 
pyenv exec python -m venv .venv
.\.venv\Scripts\Activate.ps1

## 3) Instala dependencias 
python -m pip install --upgrade pip
### si tienes requirements.txt:
pip install -r requirements.txt

## Correr el api rest con uvicorn

API rest
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000





