import enum
from typing import Any, Optional, Union

from pydantic import BaseModel

from .methods import RequestMethodEnum


class Message(BaseModel):
    json_rpc: str


class RequestMessage(Message):
    id: Union[int, str]
    """
    The request id.
    """
    method: RequestMethodEnum
    """
    The method to be invoked.
    """
    params: Optional[Any]


class ResponseError(BaseModel):
    code: int
    """
    A number indicating the error type that occurred.
    """
    message: str
    """
    A string providing a short description of the error.
    """
    data: Optional[Any]
    """
    A primitive or structured value that contains additional
    information about the error. Can be omitted.
    """


class ResponseMessage(Message):
    id: Union[int, str, None]
    """
    The request id.
    """
    result: Optional[Any]
    """
    The result of a request. This member is REQUIRED on success.
    This member MUST NOT exist if there was an error invoking the method.
    """
    error: Optional[ResponseError]
    """
    The error object in case a request fails.
    """


class NotificationMessage(Message):
    method: str
    """
    The method to be invoked.
    """
    params: Optional[Any]
    """
    The notification's params.
    """


class CancelParams(BaseModel):
    id: Union[str, int]
    """
    The request id to cancel.
    """


class ErrorCodes(enum.IntEnum):
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    jsonrpcReservedErrorRangeStart = -32099
    serverErrorStart = -32099  # yeah, the same
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001
    jsonrpcReservedErrorRangeEnd = -32000
    serverErrorEnd = -32000  # again
    lspReservedErrorRangeStart = -32899
    ContentModified = -32801
    RequestCancelled = -32800
    lspReservedErrorRangeEnd = -32800  # ...
