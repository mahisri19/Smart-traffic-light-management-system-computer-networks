import socket
import threading
import time
import matplotlib.pyplot as plt

# Global lists to store latency and throughput values for graphing
latencies = []
throughputs = []
message_counts = []

# Function to measure latency and throughput
def receive_messages(client):
    total_bytes_received = 0
    message_count = 0

    while True:
        try:
            start_time = time.time()  # Record the time before receiving the message
            message = client.recv(1024)
            if message:
                total_bytes_received += len(message)
                message_count += 1
                latency = time.time() - start_time  # Time taken for round trip
                throughput = total_bytes_received / latency  # Throughput calculation
                latencies.append(latency * 1000)  # Store latency in milliseconds
                throughputs.append(throughput)    # Store throughput
                message_counts.append(message_count)

                print(f"Received update: {message.decode('utf-8')}")
                print(f"Latency: {latency * 1000:.2f} ms")  # Latency in milliseconds
                print(f"Throughput: {throughput:.2f} bytes/sec")
        except Exception as e:
            print(f"Error: {e}")
            client.close()
            break

# Function to plot the graph
def plot_graph():
    plt.figure(figsize=(10, 5))

    # Plot Latency
    plt.subplot(1, 2, 1)
    plt.plot(message_counts, latencies, label='Latency (ms)', color='b', marker='o')
    plt.xlabel('Message Count')
    plt.ylabel('Latency (ms)')
    plt.title('Latency over Messages')
    plt.grid(True)
    plt.legend()

    # Plot Throughput
    plt.subplot(1, 2, 2)
    plt.plot(message_counts, throughputs, label='Throughput (bytes/sec)', color='r', marker='x')
    plt.xlabel('Message Count')
    plt.ylabel('Throughput (bytes/sec)')
    plt.title('Throughput over Messages')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.98.239", 9999))  # Replace with server's IP

    # Start a thread to handle receiving messages from the server
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        try:
            # Take user input and send it to the server
            traffic_data = input("Enter traffic data (e.g., 'vehicle_count: 10' or 'emergency: fire truck'): ")
            if traffic_data:
                start_time = time.time()  # Measure time before sending
                client.send(traffic_data.encode('utf-8'))
                # Optionally record latency for sending as well
                latency = time.time() - start_time
                print(f"Message sent latency: {latency * 1000:.2f} ms")
        except Exception as e:
            print(f"Error: {e}")
            client.close()
            break

    # Plot the graph once the connection is closed or the program ends
    plot_graph()

if _name_ == "_main_":
    main()
