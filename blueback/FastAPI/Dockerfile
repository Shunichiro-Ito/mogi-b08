FROM python:3.11.9
RUN apt update && apt upgrade -y
RUN apt install -y libgl1-mesa-dev

WORKDIR /usr/src/app
COPY . .

RUN pip install -r torch.requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

