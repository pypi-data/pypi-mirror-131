import socket
import json
import threading
from zeusai_py.io import _socket_io


class Client:
    def __init__(self, host: str, port: int) -> None:
        """ The class that handles connecting to and interacting with the ZeusAI server's
        I/O API.

        :param host:
        :param port:
        :return:
        """
        self.host = host
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))
        self.reader = _socket_io.SocketStreamReader(self.conn)
        self.output_func = None
        self.recv_thread = threading.Thread(target=self._recv_loop)

    def authenticate(self, username: str, password: str) -> None:
        """ Authenticate with the ZeusAI server.

        :param username:
        :param password:
        :return:
        """
        request_dict = {"endpoint": "auth", "params": {"user": username, "pass": password}}
        self._send_request(request_dict)

    def input(self, input_: str) -> None:
        """ Provide an input to the AI

        :param input_: String containing the user's input.
        :return:
        """
        request_dict = {"endpoint": "input", "params": input_}
        self._send_request(request_dict)

    def set_output_func(self, func) -> None:
        """ Set the output function to func.

        :param func: a function to be called by the recv_thread when the AI provides an output to the user.
            Should take a param for a string containing the AI output.
        :return: None
        """
        self.output_func = func

    def _get_response(self) -> dict:
        response = self.reader.readline()
        response = json.loads(response)
        return response

    def _send_request(self, request_dict: dict) -> None:
        """Serializes request_dict into a JSON bytes object and sends it to the server.

        :param request_dict: Dictionary containing a valid request for the ZeusAI Server API
        :return: None
        """
        serialized_json = json.dumps(request_dict) + "\n"
        serialized_json = serialized_json.encode("utf8")
        self.conn.sendall(serialized_json)

    def _recv_loop(self) -> None:
        """ Loop which runs in a thread to get output from the AI server.
        Takes a set of functions which are called when the associated endpoint is called."""
        while True:
            response = self._get_response()
            if response["endpoint"] == "output":
                self.output_func(response["params"])
