import socket
import threading

clients = []

# Function to broadcast messages to all clients except the sender
def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

# Function to process input and generate appropriate messages
def process_input(message):
    if "vehicle_count" in message:
        vehicle_count = int(message.split(":")[1])
        if vehicle_count > 20:
            return "Traffic Signal at Junction 1 is now RED due to heavy traffic."
        else:
            return "Traffic Signal at Junction 1 is now GREEN. Traffic is normal."
    elif "emergency" in message:
        emergency_type = message.split(":")[1].strip()
        return f"Emergency Alert: {emergency_type} approaching, giving priority."
    else:
        return "Unknown input. No action taken."

# Function to handle each client connection
def handle_client(client_socket, address):
    global clients
    print(f"Connection from {address} has been established.")
    clients.append(client_socket)
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received from {address}: {message}")
                # Process input message and generate output
                update = process_input(message)
                print(f"Sending update: {update}")
                # Broadcast update to all clients
                broadcast_message(update, client_socket)
            else:
                break
        except:
            break
    
    print(f"Connection with {address} closed.")
    clients.remove(client_socket)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.98.239", 9999))  # Bind to one of the laptops' IP
    server.listen(5)
    print("Server started and listening on 192.168.98.239:9999")
    
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
