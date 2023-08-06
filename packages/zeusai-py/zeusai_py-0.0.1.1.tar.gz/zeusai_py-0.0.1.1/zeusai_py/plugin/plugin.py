import json
import sys

from zeusai_py.io import client
from zeusai_py import exceptions


def _send_request(endpoint: str, params) -> None:
    """Helper function to send a request to the host.

    :param endpoint: String, the endpoint to send the request for.
    :param params: The appropriate params for the endpoint.
    :return: None
    """
    sys.stdout.write(json.dumps({"endpoint": endpoint, "params": params}))
    sys.stdout.flush()


def _get_response() -> dict:
    """Helper function to wait for and returns a response, or raises an exception.

    Note that this blocks until a response is received from the host.

    :raise: InvalidEndpoint, InvalidParams, ForbiddenInStandalone, NotImplementedError
    :return: Dictionary containing the response from the server.
    """
    # Get and load the input
    response = sys.stdin.readline()
    response = json.loads(response)
    if response["endpoint"] == "ERROR":
        params = response["params"]
        error = params["error"]

        # Raise different exceptions depending on the error.
        if error == "invalid endpoint":
            raise exceptions.InvalidEndpoint
        elif error == "invalid params":
            raise exceptions.InvalidParams
        elif error == "forbidden in standalone":
            raise exceptions.ForbiddenInStandalone
        elif error == "not implemented":
            raise NotImplementedError
        else:
            raise exceptions.PluginError
    else:  # If it's not an error:
        # Verify the validity of the response.
        try:
            _ = response["endpoint"]
            _ = response["params"]
        except KeyError:
            raise exceptions.InvalidResponse
        return response


def variable(variables: list) -> dict:
    """Gets a the value of a list of variables from the host.

    :param variables: List of variables to get the values of
    :type variables: List

    :raise: See _get_response().
    :return: Dictionary, containing {key: value} pairs: {variable_name: value}
    """
    _send_request("variable", variables)
    response = _get_response()
    return response["params"]


def followup(question: str) -> None:
    """ Ask the user a followup question, and get their response.

    :param question: The question to ask the user.
    :type question: String

    :raise: See _get_response().
    :return:
    """
    _send_request("followup", question)
    response = _get_response()
    return response["params"]


def simulate_client() -> client.Client:
    """Switches the way requests to and from the server are processed to use the
    I/O API instead of the Plugin API.

    NOTE: THIS IS IRREVERSIBLE! ONCE THE PLUGIN IS USING THE CLIENT API, IT CANNOT
    GO BACK TO THE PLUGIN API.

    :raise: See _get_response().
    :return: Instance of Client
    """
    _send_request("simulate client", "")
    _get_response()
    return client.Client()


def log(level: str, message: str) -> None:
    """Logs `message` with the priority of `level` to the Log File and console, respecting the user's settings.

    `message` is always prefixed with the plugin's name before logging, so it's clear where it's coming from.

    :param level: The logging level, options are: debug
    :type level:
    :param message:
    :type message:

    :raise:
    :return:
    """
    params = {"level": level, "message": message}
    _send_request("log", params)
    _get_response()
