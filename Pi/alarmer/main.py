import socket
import os

HOST = '' # all interfaces
PORT = 58881

def alarm():
  os.system('ffplay -autoexit -nodisp ./alarm.mp3 2>/dev/null')



def serve():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
      print('Connected by', addr)

      data = conn.recv(1024)
      while len(data) > 0:
        msg = data.decode('utf-8').rstrip()
        print(f'Received: {msg}')

        if msg == 'play alarm now':
          alarm()

        data = conn.recv(1024)

      print('Connection lost')
      s.close()


if __name__ == '__main__':
  while True:
    serve()
