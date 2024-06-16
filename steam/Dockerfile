# Pobierz oficjalny obraz Python w wersji 3.8
FROM python:3.8-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki zależności do kontenera
COPY requirements.txt requirements.txt

# Zainstaluj zależności
RUN pip install -r requirements.txt

# Skopiuj pozostałe pliki do kontenera
COPY . .

# Uruchom aplikację
CMD ["python", "app.py"]
