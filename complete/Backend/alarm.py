import socket

def play_alarm(pi_id: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 58881 if pi_id == 1 else 58882
    sock.connect(('host.docker.internal', port))
    try:
        sock.sendall(b'play alarm now')
        print(f'[INFO] [ALARM] alarm played for {['pi-window', 'pi-desk'][pi_id - 1]}')
    finally:
        sock.close()

if __name__ == '__main__':
    play_alarm(1)

