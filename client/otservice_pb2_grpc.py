# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import otservice_pb2 as otservice__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in otservice_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class OtServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UploadVideo = channel.stream_unary(
                '/otservice.OtService/UploadVideo',
                request_serializer=otservice__pb2.VideoRequest.SerializeToString,
                response_deserializer=otservice__pb2.VideoResponse.FromString,
                _registered_method=True)
        self.SendLogEntry = channel.unary_unary(
                '/otservice.OtService/SendLogEntry',
                request_serializer=otservice__pb2.LogEntry.SerializeToString,
                response_deserializer=otservice__pb2.LogResponse.FromString,
                _registered_method=True)


class OtServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def UploadVideo(self, request_iterator, context):
        """Upload the video file using client streaming.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendLogEntry(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OtServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UploadVideo': grpc.stream_unary_rpc_method_handler(
                    servicer.UploadVideo,
                    request_deserializer=otservice__pb2.VideoRequest.FromString,
                    response_serializer=otservice__pb2.VideoResponse.SerializeToString,
            ),
            'SendLogEntry': grpc.unary_unary_rpc_method_handler(
                    servicer.SendLogEntry,
                    request_deserializer=otservice__pb2.LogEntry.FromString,
                    response_serializer=otservice__pb2.LogResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'otservice.OtService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('otservice.OtService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class OtService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def UploadVideo(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/otservice.OtService/UploadVideo',
            otservice__pb2.VideoRequest.SerializeToString,
            otservice__pb2.VideoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SendLogEntry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/otservice.OtService/SendLogEntry',
            otservice__pb2.LogEntry.SerializeToString,
            otservice__pb2.LogResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
