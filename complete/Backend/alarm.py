import socket

def play_alarm(pi_id: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 58881 if pi_id == 1 else 58882
    sock.connect(('localhost', port))
    try:
        sock.sendall(b'play alarm now')
    finally:
        sock.close()

if __name__ == '__main__':
    play_alarm(1)

