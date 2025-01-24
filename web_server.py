from socket import *
import sys  # For program termination
import os

# Create a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 6789
serverSocket.bind(("0.0.0.0", serverPort))
serverSocket.listen(1)

print("The server is ready to receive")

while True:
    try:
        # Establish the connection
        print("Ready to serve...")
        connectionSocket, addr = serverSocket.accept()

        try:
            # Receive the request message from the client
            message = connectionSocket.recv(1024).decode()
            print(f"Received message: {message}")

            # Extract the requested file name from the message
            if len(message) > 0:
                filename = message.split()[1]

                # Try opening the requested file (Remove the leading '/')
                file_path = filename[1:]  # Removes the leading slash
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as f:
                        outputdata = f.read()

                    # Send HTTP header line into socket
                    connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

                    # Send the content of the requested file to the client
                    connectionSocket.send(outputdata.encode())

                else:
                    # If file is not found, send 404 error
                    error_message = "HTTP/1.1 404 Not Found\r\n\r\n<html><head></head><body><h1>404 Not Found</h1></body></html>"
                    connectionSocket.send(error_message.encode())

            connectionSocket.close()

        except FileNotFoundError:
            # Send response message for file not found
            error_message = "HTTP/1.1 404 Not Found\r\n\r\n<html><head></head><body><h1>404 Not Found</h1></body></html>"
            connectionSocket.send(error_message.encode())
            connectionSocket.close()

        except Exception as e:
            print(f"Error while processing request: {e}")
            connectionSocket.close()

    except KeyboardInterrupt:
        print("\nShutting down the server.")
        serverSocket.close()
        sys.exit()

    except Exception as e:
        print(f"Server error: {e}")
        serverSocket.close()
        sys.exit()
