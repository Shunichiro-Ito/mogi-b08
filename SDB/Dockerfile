FROM python:latest

WORKDIR /app

COPY ./src/ /app/

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]