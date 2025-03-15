from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VideoRequest(_message.Message):
    __slots__ = ("video_file", "model")
    VIDEO_FILE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    video_file: bytes
    model: str
    def __init__(self, video_file: _Optional[bytes] = ..., model: _Optional[str] = ...) -> None: ...

class VideoResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class LogEntry(_message.Message):
    __slots__ = ("ip_address", "grpc_system_response_time", "total_response_time")
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    GRPC_SYSTEM_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    ip_address: str
    grpc_system_response_time: float
    total_response_time: float
    def __init__(self, ip_address: _Optional[str] = ..., grpc_system_response_time: _Optional[float] = ..., total_response_time: _Optional[float] = ...) -> None: ...

class LogResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
