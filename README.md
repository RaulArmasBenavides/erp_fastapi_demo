
# 1) Usa la versión de Python del proyecto (pyenv)
pyenv local 3.9.13
pyenv exec python -V

# 2) Crea/activa un virtualenv (si no existe)
pyenv exec python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3) Instala dependencias
python -m pip install --upgrade pip
# si tienes requirements.txt:
pip install -r requirements.txt


API rest
uvicorn app.main:app --reload
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000





pip install mypy pyright ruff