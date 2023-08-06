"""
When the IO package is run on its own, it runs a basic interactive CLI.
This __main__ module also works as an example of a basic client for other developers
"""
from zeusai_py import io
import getpass


def output(ai_out: str):
    """"""
    print(ai_out)


def main():
    host = input("ZeusAI Server Host: ")
    port = int(input("ZeusAI Server Port: "))
    client = io.Client(host, port)
    username = input("Username: ")
    password = getpass.getpass()
    client.authenticate(username, password)
    client.set_output_func(output)
    client.recv_thread.start()
    while True:
        user_input = input("Input: ")
        client.input(user_input)


if __name__ == "__main__":
    main()
