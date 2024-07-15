import socket
import playsound

HOST = '' # all interfaces
PORT = 58881

def alarm():
  playsound.playsound('./alarm.mp3')


def serve():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
      print('Connected by', addr)

      msg = conn.recv(1024).decode('utf-8').rstrip()
      print(msg)

      if msg == 'play alarm now':
        alarm()

      s.close()


if __name__ == '__main__':
  while True:
    serve()
