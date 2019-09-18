from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread 

# Inicia as "listas" com as relações de clientes e endereços, para fins
# de broadcast:
clients = {}
addresses = {}

# Seta o host como si mesmo, devido ao fato de ser um servidor.
host = ''
# Declara a porta a ser utilizada para comunicação.
port = 33000
# Determina o tamanho máximo de uma mensagem.
bufferSize = 1024

# Seta o endereço e o socket a ser utilizado.
address = (host, port)
server = socket(AF_INET, SOCK_STREAM)
server.bind(address)

# Função a qual gerencia os recebimentos de requisição de clientes.
def acceptIncomingConnections():
    while True:
        # Aceita a conexão.
        client, client_address = server.accept()
        # Printa para o servidor que o cliente de IP "x" se conectou.
        print("%s:%s has connected." % client_address)
        # Envia para o cliente uma mensagem para determinação do nome.
        client.send(str("Welcome! Type your name and press enter: ").encode())
        # Adiciona o cliente à lista de clientes.
        addresses[client] = client_address
        # Inicia a thread a qual lida com o cliente a ser conectado.
        Thread(target=handleClient, args=(client,)).start()

# Função a qual lida com cada cliente, passando o retorno de "server.accept()"
# como parâmetro.
def handleClient(client):
	# A primeira mensagem a ser enviada pelo cliente é uma mensagem a
	# qual contém o nome a ser utilizado pelo sistema para o reconhecimento
	# de usuários.
    name = client.recv(bufferSize).decode('utf8')
    # Envio de uma mensagem de boas vindas ao usuário.
    welcome = 'Welcome %s! If you want to quit, type {quit} before closing the window.' %name
    client.send(str(welcome).encode())
    # Envio por broadcast, excluindo o próprio cliente, de uma mensagem
    # indicativa de que um novo usuário se conectou.
    msg = "%s entrou no chat." % name
    broadcast(str(msg).encode(), client)
    clients[client] = name
    # Loop que gerencia os envios de mensagens do cliente.
    while True:
        msg = client.recv(bufferSize)
        if msg != str("{quit}").encode():
            broadcast(msg, client, (name+": ").encode())
        else:
            # Envio, por broadcast, de uma mensagem de desconexão de cliente.
            broadcast(str("%s has left the chat." %name).encode(), client)
            # Gerenciamento dos clientes que se desconectaram.
            print("%s disconnected." %name)
            # Remoção do cliente da lista de clientes.
            del clients[client]
            break

# Envia a mensagem para todos os clientes conectados ao socket, exceto
# o cliente passado por parâmetro.
def broadcast(msg, client, prefix=""):
    for sock in clients:
        if sock != client:
            sock.send((str(prefix) + str(msg)).encode())

# Main:
if __name__ == "__main__":
    # Gerencia o número máximo de conexões.
    server.listen(10)
    print("Waiting for connection.")
	
	# Inicia a thread a qual tem como intuito aceitar conexões:
    accept_thread = Thread(target=acceptIncomingConnections)
    accept_thread.start()
    
    accept_thread.join()
    
    server.close()
