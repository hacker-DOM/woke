import json
import collections
from typing import Union

from protocol_structures import (
    RequestMessage,
    ResponseMessage,
    ResponseError,
    NotificationMessage,
)


# TODO Buffering messages


class RPCProtocolError(Exception):
    pass


class TcpCommunicator:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    def read(self, args):
        return self.reader.read(args).decode("utf-8")

    def write(self, output):
        self.writer.write(output.encode("utf-8"))
        self.writer.flush()

    def read_line(self, *args):
        return self.reader.readline(*args).decode("utf-8")


class RPCProtocol:
    """
    Json rpc comunication
    """

    def __init__(self, reader):
        self.reader = reader
        # For buffering messages
        self.msg_buffer = collections.deque()

    def _read_header(self):
        """
        Reads message header (Content length only)
        """
        # Is there anything to read ?
        try:
            line = self.reader.read_line()
        except Exception:
            raise EOFError()
        # It is, read header then
        if line.startswith("Content-Length: ") and line.endswith("\r\n"):
            content_length = int(line.split(":")[-1])
        else:
            raise RPCProtocolError(f"Invalid HTTP header: {line}")
        # Skip unnecessary header part
        while line != "\r\n":
            line = self.reader.read_line()
        # Return content length
        return content_length

    def _read_content(self, len) -> dict:
        """
        Reads message content
        """

        body = self.reader.read(len)
        return json.loads(body)

    def recieve_message(self) -> Union[RequestMessage, NotificationMessage]:
        """
        Get content length parameters from http header
        (Is useless variable at this point, but function
            make steps over the header and stop before content)
        Get RPC message body content
        """
        # if self.msg_buffer:
        #    return self.msg_buffer.popleft()
        try:
            len = self._read_header()
            json_content = self._read_content(len)
            if "id" in json_content:
                message_object = RequestMessage(
                    json_rpc=json_content["jsonrpc"],
                    id=json_content["id"],
                    method=json_content["method"],
                    params=json_content["params"],
                )
            else:
                message_object = NotificationMessage(
                    json_rpc=json_content["jsonrpc"],
                    method=json_content["method"],
                    params=json_content["params"],
                )
        except Exception:
            raise RPCProtocolError(f"Invalid Request")

        # self.buffer.append(message)
        return message_object

    def send_rpc_response(self, response: ResponseMessage):
        """
        Response object to be send
        """
        return self._send(response.dict())

    def send_rpc_request(self, request: RequestMessage):
        """
        Request object to be send
        """
        return self._send(request.dict())

    def send_rpc_error(self, error: ResponseError):
        """
        Error object to be send
        """
        return self._send(error.dict())

    def send_rpc_notification(self, notification: NotificationMessage):
        """
        Notification object to be send
        """
        return self._send(notification.dict())

    def _send(self, message: dict):
        """
        Formats object to message and sends it
        """
        message_str = json.dumps(message, separators=(",", ":"))
        content_length = len(message_str)
        response = f"Content-Length: {content_length}\r\nContent-Type: application/vscode-jsonrpc; charset=utf8\r\n\r\n{message_str}"
        # print(f"RESPONSE:\n{response}\n")
        print("RESPONSE HAVE BEEN SENT")
        # raise EOFError()
        self.reader.write(response)
