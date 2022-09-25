import socket
import os
import pickle

class RunServer:
    players =[]
    board = [["□"]*20 for _ in range(20)]
    vector = [(1,0),(-1,0),(0,1),(0,-1),
        (-1,-1),(-1,1),(1,-1),(1,1)]

    def __init__(self, host, port, hname, n):
        self.host = host
        self.port = port
        self.setPlayername(hname)
        self.n = n
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.message = ""
        
    def run(self):
        self.server.bind((self.host,self.port))
        self.client, self.addr = self.server.accept()
        print("접속한 클라이언트 : ", self.addr)
        self.setPlayername(self.client.recv(1024).decode())
        self.createMessage(n=self.n,p=0)
        print(self.message)

        self.client.send(self.messagge.endcode())
        self.client.send(pickle.dumps(self.board))

        while True:
            try:
                x, y = map(int,input("(x,y)>>").split(","))
                if self.board[x][y] == "□":
                    self.board[x][y] = "★"
                else :
                    print("해당 위치에는 놓을 수 없습니다.")
                    continue
            except :
                print("잘못된 입력입니다.")
                continue

            self.createMessage(n=self.n,p=1)

            for i in range(n):
                for j in range(n):
                    if self.board[i][j] != "□":
                        res = self.winChecker(i,j,self.board[i][j], n)
                        if res:
                            self.client.sendall(self.message+res+"의 승리로 게임이 종료되었습니다.")
                            print(self.message)
                            self.client.close()

            self.client.sendall(self.message.encode())
            self.client.sendall(pickle.dumps(self.board))
            os.system("cls")
            print(self.message)


            self.board = pickle.loads(self.client.recv(4096))
            os.system("cls")
            self.createMessage(n=self.n,p=0)
            for i in range(n):
                for j in range(n):
                    if self.board[i][j] != "□":
                        res = self.winChecker(i,j,self.board[i][j], n)
                        if res:
                            self.client.sendall(self.message+res+"의 승리로 게임이 종료되었습니다.")
                            print(self.message)
                            self.client.close()
            self.client.sendall(self.message.encode())
            print(self.message)

    def setPlayername(self,name):
        self.players.append(name)

    def createMessage(self,p,n):
        self.message = "::CURRENT PLAYER : %s\n"%self.players[p]
        for i in range(n+1):
            if i == 0:
                self.message("x  ")
            else :
                self.messagge=(str((i-1)%10)+"  ")
        self.message+="\n"

        for i in range(n):
            self.messagge+=(str((i-1)%10)+" ")
            for j in range(n):
                self.message +=(self.board[i][j]+" ")
            self.message+="\n"
    
    def winChecker(self,x,y,mal,n):
        for vx,vy in self.vector:
            counter = 1
            for i in range(1,5):
                if 0<=x+(vx*i)<n and 0<=y+(vy*i)<20 and self.board[x+(vx*i)][y+(vy*i)] == mal:
                    if self.board[x+(vx*i)][y+(vy*i)] == "□":
                        break
                    else:
                        counter += 1
                        if counter == 5:
                            return mal
        return False

pname=input("플레이어 이름을 입력하세요 :")

while True:
    n=int(input("오목판의 크기를 입력하세요(5~20) :"))
    if 5>=n and n>20:
        print("판의 크기가 잘못되었습니다.")
        continue
    else :
        break

RunServer(socket.gethostbyname(socket.gethostname()),7777,pname,n).run()