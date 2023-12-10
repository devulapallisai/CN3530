import socket
import threading

class LoadBalancer:
    def __init__(self, server_addresses, algorithm):
        self.server_addresses = server_addresses
        self.algorithm = algorithm
        self.current_index = 0
        self.lock = threading.Lock()

    def start(self, host, port):
        balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        balancer_socket.bind((host, port))
        balancer_socket.listen(5)
        print("Load Balancer is running on",host,port)

        while True:
            client_socket, client_address = balancer_socket.accept()
            print("Received connection from",client_address)

            # Choose the backend server using the specified algorithm
            with self.lock:
                backend_address = self.choose_backend()

            # Forward the connection to the selected backend server
            threading.Thread(target=self.forward, args=(client_socket, backend_address)).start()

    def choose_backend(self):
        # Implement different load balancing algorithms here
        if self.algorithm == "round-robin":
            backend_address = self.server_addresses[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.server_addresses)
            return backend_address
        else:
            # Add more algorithms as needed
            pass

    def forward(self, client_socket, backend_address):
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect(backend_address)

        # Forward data from client to backend
        threading.Thread(target=self.forward_data, args=(client_socket, backend_socket)).start()

        # Forward data from backend to client
        self.forward_data(backend_socket, client_socket)

    def forward_data(self, source, destination):
        while True:
            data = source.recv(1024)
            if not data:
                break
            destination.sendall(data)

if __name__ == "__main__":
    # Define the addresses of backend servers
    backend_servers = [("10.0.0.3", 8000), ("10.0.0.4", 8000), ("10.0.0.5", 8000), ("10.0.0.6", 8000), ("10.0.0.7", 8000), ("10.0.0.8", 8000), ("10.0.0.9", 8000)]

    # Create a load balancer with round-robin algorithm
    load_balancer = LoadBalancer(server_addresses=backend_servers, algorithm="round-robin")

    # Start the load balancer on a specific host and port
    load_balancer.start(host="10.0.0.2", port=8888)