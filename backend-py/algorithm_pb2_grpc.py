# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import algorithm_pb2 as algorithm__pb2

GRPC_GENERATED_VERSION = '1.70.0'
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
        + f' but the generated code in algorithm_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class AlgorithmServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UploadFile = channel.stream_unary(
                '/algorithm.AlgorithmService/UploadFile',
                request_serializer=algorithm__pb2.FileChunk.SerializeToString,
                response_deserializer=algorithm__pb2.UploadResponse.FromString,
                _registered_method=True)
        self.GetJobStatus = channel.unary_unary(
                '/algorithm.AlgorithmService/GetJobStatus',
                request_serializer=algorithm__pb2.JobStatusRequest.SerializeToString,
                response_deserializer=algorithm__pb2.JobStatusResponse.FromString,
                _registered_method=True)
        self.DownloadFile = channel.unary_stream(
                '/algorithm.AlgorithmService/DownloadFile',
                request_serializer=algorithm__pb2.DownloadRequest.SerializeToString,
                response_deserializer=algorithm__pb2.FileChunkResponse.FromString,
                _registered_method=True)
        self.ConfirmDelete = channel.unary_unary(
                '/algorithm.AlgorithmService/ConfirmDelete',
                request_serializer=algorithm__pb2.DownloadRequest.SerializeToString,
                response_deserializer=algorithm__pb2.ConfirmDeleteResponse.FromString,
                _registered_method=True)


class AlgorithmServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def UploadFile(self, request_iterator, context):
        """Upload a file
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetJobStatus(self, request, context):
        """Get job status
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DownloadFile(self, request, context):
        """Download processed file
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConfirmDelete(self, request, context):
        """Confirm delete after download
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AlgorithmServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UploadFile': grpc.stream_unary_rpc_method_handler(
                    servicer.UploadFile,
                    request_deserializer=algorithm__pb2.FileChunk.FromString,
                    response_serializer=algorithm__pb2.UploadResponse.SerializeToString,
            ),
            'GetJobStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetJobStatus,
                    request_deserializer=algorithm__pb2.JobStatusRequest.FromString,
                    response_serializer=algorithm__pb2.JobStatusResponse.SerializeToString,
            ),
            'DownloadFile': grpc.unary_stream_rpc_method_handler(
                    servicer.DownloadFile,
                    request_deserializer=algorithm__pb2.DownloadRequest.FromString,
                    response_serializer=algorithm__pb2.FileChunkResponse.SerializeToString,
            ),
            'ConfirmDelete': grpc.unary_unary_rpc_method_handler(
                    servicer.ConfirmDelete,
                    request_deserializer=algorithm__pb2.DownloadRequest.FromString,
                    response_serializer=algorithm__pb2.ConfirmDeleteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'algorithm.AlgorithmService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('algorithm.AlgorithmService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AlgorithmService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def UploadFile(request_iterator,
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
            '/algorithm.AlgorithmService/UploadFile',
            algorithm__pb2.FileChunk.SerializeToString,
            algorithm__pb2.UploadResponse.FromString,
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
    def GetJobStatus(request,
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
            '/algorithm.AlgorithmService/GetJobStatus',
            algorithm__pb2.JobStatusRequest.SerializeToString,
            algorithm__pb2.JobStatusResponse.FromString,
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
    def DownloadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/algorithm.AlgorithmService/DownloadFile',
            algorithm__pb2.DownloadRequest.SerializeToString,
            algorithm__pb2.FileChunkResponse.FromString,
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
    def ConfirmDelete(request,
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
            '/algorithm.AlgorithmService/ConfirmDelete',
            algorithm__pb2.DownloadRequest.SerializeToString,
            algorithm__pb2.ConfirmDeleteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
