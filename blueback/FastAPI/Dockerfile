FROM python:3.11.9

WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload"]

