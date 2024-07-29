# Basis-Image mit Python 3.12
FROM python:3.12-slim

# Installiere die notwendigen Systempakete
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Quellcode
COPY . .

# Setze Umgebungsvariablen (falls nötig)
ENV FLASK_APP=app/app.py

# Flask-Server starten
CMD ["flask", "run", "--host=0.0.0.0"]
