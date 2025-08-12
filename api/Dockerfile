FROM python:3.9-slim

WORKDIR /app

COPY ./api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY sentiment_model.pkl /app/sentiment_model.pkl
COPY IMDB_Dataset.csv /app/IMDB_Dataset.csv

COPY ./api /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]