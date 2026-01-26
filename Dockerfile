FROM python:3.9-slim

# Evita archivos .pyc y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (opcional pero recomendado)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (mejor cache)
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copiar el proyecto
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para levantar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
