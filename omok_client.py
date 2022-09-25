import socket
import pickle
import os

name = input("사용자명을 입력하세요 : ")
host = input("서버 ip를 입력하세요 : ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((host, 7777))
client.sendall(name.encode())


print(client.recv(4096).decode())
board = pickle.loads(client.recv(4096))
while True:
    print(client.recv(4096).decode())
    board = pickle.loads(client.recv(4096))
    try:
        x, y = map(int, input("(x, y) >>").split(","))
        if board[x][y] == "□":
            board[x][y] = "●"
        else:
            print("해당 위치에는 놓을 수 없습니다.")
            continue
    except IndexError:
        print("잘못된 위치입니다.")
        continue
    os.system("cls")

    client.send(pickle.dumps(board))
    print(client.recv(4096).decode())