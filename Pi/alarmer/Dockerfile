FROM python:3.11.9
RUN apt update && apt upgrade -y
RUN apt install -y cmake libgirepository1.0-dev

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 58881

ENTRYPOINT python ./main.py
