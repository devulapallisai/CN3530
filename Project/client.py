import socket
import threading

def request_generator(request_type="GET",*args):
	''' This function takes request_type and args as arguments where request_type tells whether request is 
	PUT/DELETE/GET and args are corresponding keys (or) values needed for those requests'''
	if(request_type=="GET"):
		return r"GET /assignment2?request="+args[0]+r" HTTP/1.1"+"\r\n\r\n"

	elif(request_type=="PUT"):
		return r"PUT /assignment2/"+args[0]+r"/"+args[1]+r" HTTP/1.1"+"\r\n\r\n"

	elif(request_type=="DELETE"):
		return r"DELETE /assignment2/"+args[0]+r" HTTP/1.1"+"\r\n\r\n"

	else:
		return None

def send_request(client_port, request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', client_port))
    client_socket.sendall(request.encode())
    response = client_socket.recv(1024).decode()
    client_socket.close()
    return response

def send_multiple_requests(client_port, requests):
    threads = []
    for request in requests:
        thread = threading.Thread(target=send_request, args=(client_port, request))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    client_port = 5000
    requests = [request_generator("PUT", "key1", "val1"), request_generator("PUT", "key2", "val2"),
                request_generator("GET", "key1"), request_generator("DELETE", "key2")]
    
    for _ in range(3):
        send_multiple_requests(client_port, requests)
