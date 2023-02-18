import os
import sys
import time
import socket

def Server():

    server_socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_TCP.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    server_socket_TCP.bind(('', 41710))

    server_socket_TCP.listen()
    print('Server is ready. Listening address:', server_socket_TCP.getsockname())

    client_socket_TCP, client_address = server_socket_TCP.accept()
    print('A client has connected and it is at:', client_address)

    server_socket_TCP.close()
    client_socket_TCP.close()

    server_socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket_UDP.bind(('', 41710))

    #Test 3 Server to Client
    print('\nStart test3 - UDP pingpong\nFrom server to client')

    PPSend(5, 5, 1024, server_socket_UDP, client_address)
    



def Client(argv):

    client_socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_TCP.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    try:
        client_socket_TCP.connect((argv[1], 41710))
        print('Client has connected to server at:', client_socket_TCP.getpeername())
        print('Client\'s address:', client_socket_TCP.getsockname())
    except socket.error as err:
        print('Connection error: ', err)
        sys.exit(1)
    
    client_address = client_socket_TCP.getsockname()

    client_socket_TCP.close()

    client_socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket_UDP.bind(('', client_address[1]))

    #Test 3 Server to Client
    print('\nStart test3 - UDP pingpong\nFrom server to client\n* * * * *')
    PPReceive(5, 1024, client_socket_UDP)



def PPSend(data_size, num_msg, bufsize, self_socket: socket, target_address: tuple):
    #Generate a random byte of a given size (5 bytes)
    data = os.urandom(data_size)
    #For calculating the average round trip time
    rtt_total = 0
    #A for loop to send a pre-defined number of message 
    for _ in range(num_msg):
        #Start the timer
        start_time = time.perf_counter()
        #Send to data to the target address using socket.sendto() (UDP)
        self_socket.sendto(data, (target_address[0],target_address[1]))
        #Receive the data from the target address using socket.recvfrom() (UDP)
        data, address = self_socket.recvfrom(bufsize)
        #End the timer
        end_time = time.perf_counter()
        #Calculate the round trip time
        rtt = end_time - start_time
        #Add it to the average round trip time counter
        rtt_total += rtt
        #Display the single round trip time
        print(f'Reply from {address}: time = {"{:.5f}".format(rtt)} s')
    #Display the average round trip time
    print(f'Average RTT: {"{:.5f}".format(rtt_total/num_msg)} s')
    return 0

def PPReceive(num_msg, bufsize, self_socket: socket):
    #A for loop to receive a pre-defined number of message 
    for _ in range(num_msg):
        #Receive the data from the target address using socket.recvfrom() (UDP)
        data, address = self_socket.recvfrom(bufsize)
        #Send to data to the target address using socket.sendto() (UDP)
        self_socket.sendto(data, address)
    return 0


def update_progress(progress):
    sys.stdout.write('\r[{0}] {1}%'.format('*' * int(progress / 2.5), progress))
    sys.stdout.flush()


if __name__ == '__main__':
    b = b'OK'
    print(str(b) == 'OK')
    if len(sys.argv) == 1:
        Server()
    elif len(sys.argv) == 2:
        #The second argument is the IP of the Server
        Client(sys.argv)
    else:
        print('Argument Error, please enter zero or one argument')