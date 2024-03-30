from simple_logger import SimpleLogger

import logging
import pty
import socket
import os
import select
import subprocess
from concurrent.futures import ThreadPoolExecutor


class TelnetServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.executor = ThreadPoolExecutor(max_workers=10)

        self.logger = SimpleLogger(__name__).logger

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.logger.info(f"Telnet server started on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.executor.submit(self.handle_client, client_socket)
        except KeyboardInterrupt:
            self.stop()

    def handle_client(self, client_socket):
        self.logger.info(f"Connected client: {client_socket.getpeername()}")
        master_fd, slave_fd, shell_pid = None, None, None

        try:
            master_fd, slave_fd = pty.openpty()
            shell_pid = subprocess.Popen(['/bin/bash'], stdin=slave_fd, stdout=slave_fd, stderr=slave_fd)

            os.close(slave_fd)

            inputs = [client_socket, master_fd]

            while True:
                readable, _, _ = select.select(inputs, [], [])
                for fd in readable:
                    if fd == client_socket:
                        data = client_socket.recv(1024)
                        if not data:
                            # Client closed the connection
                            self.close_connection(client_socket, master_fd, shell_pid.pid)
                            return
                        os.write(master_fd, data)
                    elif fd == master_fd:
                        output = os.read(master_fd, 1024)
                        client_socket.sendall(output)
        except Exception as e:
            self.logger.error(f"Error handling client: {e}")
        finally:
            self.close_connection(client_socket, master_fd, shell_pid.pid)

    @classmethod
    def close_connection(cls, client_socket, master_fd, shell_pid):
        client_socket.close()
        os.close(master_fd)
        os.kill(shell_pid, 9)

    def stop(self):
        self.logger.info("Stopping Telnet server...")
        self.server_socket.close()
        self.executor.shutdown()
        self.logger.info("Telnet server stopped.")


if __name__ == "__main__":
    telnet_server = TelnetServer("", 2333)
    telnet_server.start()
