'''
Name: Tsang Edmund Chiu Yat
UID: 3035667261
Development platform: VSCode, Window 11 (64-bit)
Python version: 3.10.10
Port range: 41710 to 41719
'''
import os
import sys
import time
import socket

def Client(argv):
    server_port = 41710
    #Start a client side TCP socket
    client_socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_TCP.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    try:
        #Connecting to the server address given by the argument and pre-located port
        client_socket_TCP.connect((argv[1], server_port))
        print('Client has connected to server at:', client_socket_TCP.getpeername())
        print('Client\'s address:', client_socket_TCP.getsockname())
    except socket.error as err:
        #If there is an error, print out the error and terminate the program
        print('Connection error: ', err)
        sys.exit(1)

    #Test 1 Server to Client
    print('\nStart test1 - large transfer\nFrom server to client')
    #Before receiving the data, send the ready acknowledgement
    client_socket_TCP.send(b'ok')
    print('Acknowledgment sent')
    Receive(200000000, 1024, client_socket_TCP)

    #Test 1 Client to Server
    print('From client to server')
    #Before sending the data, wait for the ready acknowledgement
    msg = client_socket_TCP.recv(5)
    print('Acknowledgment received: ', msg.decode())
    Send(200000000, 1024, 'client', client_socket_TCP)


    #Test 2 Server to Client
    print('\nStart test2 - small transfer\nFrom server to client')
    #Before receiving the data, send the ready acknowledgement
    client_socket_TCP.send(b'ok')
    print('Acknowledgment sent')
    Receive(10000, 1024, client_socket_TCP)

    #Test 2 Client to Server
    print('From client to server')
    #Before sending the data, wait for the ready acknowledgement
    msg = client_socket_TCP.recv(5)
    print('Acknowledgment received: ', msg.decode())
    Send(10000, 1024, 'client', client_socket_TCP)

    #Save the Client TCP port for the UDP socket
    client_address = client_socket_TCP.getsockname()
    #Close the TCP socket
    client_socket_TCP.close()

    #Start a client side UDP socket
    client_socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Locate the port for the UDP socket
    client_socket_UDP.bind(('', client_address[1]))

    #Test 3 Server to Client
    print('\nStart test3 - UDP pingpong\nFrom server to client')
    #Before receiving the data, send the ready acknowledgement
    client_socket_UDP.sendto(b'ok', (argv[1], server_port))
    print('Acknowledgment sent')
    PPReceive(5, 1024, client_socket_UDP)


    #Test 3 Client to Server
    print('\nFrom client to server')
    #Before sending the data, wait for the ready acknowledgement
    msg, _ = client_socket_UDP.recvfrom(5)
    print('Acknowledgment received: ', msg.decode())
    PPSend(5, 5, 1024, client_socket_UDP, (argv[1], server_port))
    print('End of all benchmarks')

    #Close the client side UDP socket
    client_socket_UDP.close()

    return 0

def Server():
    server_port = 41710
    #Start a server side TCP socket
    server_socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_TCP.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    #Locate the port for the TCP socket
    server_socket_TCP.bind(('', server_port))
    #Listen for client action
    server_socket_TCP.listen()
    print('Server is ready. Listening address:', server_socket_TCP.getsockname())
    #Accept Client connection
    client_socket_TCP, client_address = server_socket_TCP.accept()
    print('A client has connected and it is at:', client_address)
              
    #Test 1 Server to Client
    print('\nStart test 1 - large transfer\nFrom server to client')
    #Before sending the data, wait for the ready acknowledgement
    msg = client_socket_TCP.recv(5)
    print('Acknowledgment received: ', msg.decode())
    Send(200000000, 1024, 'server', client_socket_TCP)


    #Test 1 Client to Server
    print('From client to server')
    #Before receiving the data, send the ready acknowledgement
    client_socket_TCP.send(b'ok')
    print('Acknowledgment sent')
    Receive(200000000, 1024, client_socket_TCP)

    #Test 2 Server to Client
    print('\nStart test2 - small transfer\nFrom server to client')
    #Before sending the data, wait for the ready acknowledgement
    msg = client_socket_TCP.recv(5)
    print('Acknowledgment received: ', msg.decode())
    Send(10000, 1024, 'server', client_socket_TCP)


    #Test 2 Client to Server
    print('From client to server')
    #Before receiving the data, send the ready acknowledgement
    client_socket_TCP.send(b'ok')
    print('Acknowledgment sent')
    Receive(10000, 1024, client_socket_TCP)

    #Close both client and server TCP socket
    server_socket_TCP.close()
    client_socket_TCP.close()

    #Start a server side UDP socket
    server_socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Locate the same port as the TCP socket for the UDP socket
    server_socket_UDP.bind(('', server_port))


    #Test 3 Server to Client
    print('\nStart test3 - UDP pingpong\nFrom server to client')
    #Before sending the data, wait for the ready acknowledgement
    msg, _ = server_socket_UDP.recvfrom(5)
    print('Acknowledgment received: ', msg.decode())
    PPSend(5, 5, 1024, server_socket_UDP, client_address)


    #Test 3 Client to Server
    print('From client to server')
    #Before receiving the data, send the ready acknowledgement
    server_socket_UDP.sendto(b'ok', client_address)
    print('Acknowledgment sent')
    PPReceive(5, 1024, server_socket_UDP)
    print('\nEnd of all benchmarks')

    #Close the server side UDP socket
    server_socket_UDP.close()

    return 0


def Send(data_size, buff_size, send_side, target_socket: socket):
    #Generate a random byte of a given size (20000000 bytes)
    data = os.urandom(data_size)
    #i is used for the wile loop
    i = 0
    #total sent is the total amount of data sent in byte
    total_sent = 0
    #Start the timer and progress bar
    update_progress(0)
    start_time = time.perf_counter()
    while i < data_size:
        #Slice the data in to blocks of pre-defined size
        #Send to data to the target socket using socket.send()
        sent = target_socket.send(data[i:i+buff_size])
        #Count the btyes of data sent
        total_sent += sent
        #Update i for while loop and progress bar
        i += buff_size
        update_progress(int((total_sent / data_size) * 100))
    #Stop the timer
    end_time = time.perf_counter()
    #Displaying performance data
    print(f'\nSent total: {total_sent} bytes')
    print(f'Elapsed time: {round(end_time - start_time, 6)}s')
    if send_side == 'server':
        print(f'Throughput(from server to client): {round((total_sent/1000000)/(end_time - start_time),6)} Mb/s')
    elif send_side == 'client':
        print(f'Throughput(from client to server): {round((total_sent/1000000)/(end_time - start_time),6)} Mb/s')
    return 0

def Receive(data_size, buff_size, self_socket: socket):
    # receive data using socket.recv_into() with the specified buffer size
    received_data = bytearray()
    while len(received_data) < data_size:
        data = bytearray(buff_size)
        num_bytes_received = self_socket.recv_into(data, buff_size)
        if not num_bytes_received:
            break
        received_data += data[:num_bytes_received]
    print(f'Received total: {len(received_data)} bytes')

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
        #Receive the data from the target address using socket.recvfrom() (UDP) as acknowledgement
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
    num_received = 0
    update_progress(0)
    for _ in range(num_msg):
        #Receive the data from the target address using socket.recvfrom() (UDP)
        data, address = self_socket.recvfrom(bufsize)
        #Send the data to the target address using socket.sendto() (UDP) as acknowledgement 
        self_socket.sendto(data, address)
        num_received += 1
        update_progress(int((num_received / num_msg) * 100))
    return 0

def update_progress(progress):
    sys.stdout.write('\r[{0}] {1}%'.format('*' * int(progress / 2.5), progress))
    sys.stdout.flush()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Server()
    elif len(sys.argv) == 2:
        #The second argument is the IP of the Server
        Client(sys.argv)
    else:
        print('Argument Error, please enter zero or one argument')