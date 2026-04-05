FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

COPY . .

COPY ./AboutEverything/entrypoint.sh /app/AboutEverything/entrypoint.sh

WORKDIR /app/AboutEverything

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]