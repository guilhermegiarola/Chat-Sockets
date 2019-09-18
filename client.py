from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys

# Determina o tamanho máximo a ser enviado a cada mensagem.
buffSize = 1024

# Função a qual gerencia o envio de uma mensagem.
def send():
		msg = raw_input()
		client_socket.send(str(msg).encode())

# Função a qual gerencia o recebimento de uma mensagem.
def receive():
	# Loop "infinito" o qual tem como intuito gerenciar o recebimento de 
	# mensagens até que a mensagem "{quit}" seja recebida.
	while True:
		message = client_socket.recv(buffSize).decode('utf8')
		# Caso a mensagem seja "{quit}":
		if message == "{quit}":
			onClosing(message)
			return 0
		# Caso contrário:
		else:
			print(message)

# Função a qual gerencia o término da conexão ao servidor e termina a 
# thread de recebimento.	
def onClosing(msg):
	client_socket.send(str(msg).encode())
	stop(receive_thread)
	return

# Configuração do socket de comunicação.
client_socket = socket(AF_INET,SOCK_STREAM)
address = ('127.0.0.1', 33000)
# Conexão ao endereço determinado.
client_socket.connect(address)

# Inicialização da thread de recebimento.
receive_thread = Thread(target=receive)
receive_thread.start()

# Loop infinito para envio (o qual é terminado somente com o recebimento
# da mensagem "{quit}":
while True:
	send()
