FROM python:3.11.9
RUN apt update && apt upgrade -y
RUN apt install -y \
  gstreamer1.0-tools \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-ugly \
  libgirepository1.0-dev \
  libcairo2-dev \
  python3-gi \
  python3-gi-cairo \
  gir1.2-gstreamer-1.0 \
  pkg-config

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python",  "./main.py"]

EXPOSE 58881
