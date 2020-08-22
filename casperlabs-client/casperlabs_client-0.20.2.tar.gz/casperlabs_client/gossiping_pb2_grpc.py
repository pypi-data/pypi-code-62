# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import consensus_pb2 as consensus__pb2
from . import empty_pb2 as empty__pb2
from . import gossiping_pb2 as gossiping__pb2


class GossipServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NewBlocks = channel.unary_unary(
                '/io.casperlabs.comm.gossiping.GossipService/NewBlocks',
                request_serializer=gossiping__pb2.NewBlocksRequest.SerializeToString,
                response_deserializer=gossiping__pb2.NewBlocksResponse.FromString,
                )
        self.NewDeploys = channel.unary_unary(
                '/io.casperlabs.comm.gossiping.GossipService/NewDeploys',
                request_serializer=gossiping__pb2.NewDeploysRequest.SerializeToString,
                response_deserializer=gossiping__pb2.NewDeploysResponse.FromString,
                )
        self.StreamAncestorBlockSummaries = channel.unary_stream(
                '/io.casperlabs.comm.gossiping.GossipService/StreamAncestorBlockSummaries',
                request_serializer=gossiping__pb2.StreamAncestorBlockSummariesRequest.SerializeToString,
                response_deserializer=consensus__pb2.BlockSummary.FromString,
                )
        self.StreamLatestMessages = channel.unary_stream(
                '/io.casperlabs.comm.gossiping.GossipService/StreamLatestMessages',
                request_serializer=gossiping__pb2.StreamLatestMessagesRequest.SerializeToString,
                response_deserializer=consensus__pb2.Block.Justification.FromString,
                )
        self.StreamBlockSummaries = channel.unary_stream(
                '/io.casperlabs.comm.gossiping.GossipService/StreamBlockSummaries',
                request_serializer=gossiping__pb2.StreamBlockSummariesRequest.SerializeToString,
                response_deserializer=consensus__pb2.BlockSummary.FromString,
                )
        self.StreamDeploySummaries = channel.unary_stream(
                '/io.casperlabs.comm.gossiping.GossipService/StreamDeploySummaries',
                request_serializer=gossiping__pb2.StreamDeploySummariesRequest.SerializeToString,
                response_deserializer=consensus__pb2.DeploySummary.FromString,
                )
        self.GetBlockChunked = channel.unary_stream(
                '/io.casperlabs.comm.gossiping.GossipService/GetBlockChunked',
                request_serializer=gossiping__pb2.GetBlockChunkedRequest.SerializeToString,
                response_deserializer=gossiping__pb2.Chunk.FromString,
                )
        self.StreamDeploysChunked = channel.unary_stream(
                '/io.casperlabs.comm.gossiping.GossipService/StreamDeploysChunked',
                request_serializer=gossiping__pb2.StreamDeploysChunkedRequest.SerializeToString,
                response_deserializer=gossiping__pb2.Chunk.FromString,
                )
        self.GetGenesisCandidate = channel.unary_unary(
                '/io.casperlabs.comm.gossiping.GossipService/GetGenesisCandidate',
                request_serializer=gossiping__pb2.GetGenesisCandidateRequest.SerializeToString,
                response_deserializer=consensus__pb2.GenesisCandidate.FromString,
                )
        self.AddApproval = channel.unary_unary(
                '/io.casperlabs.comm.gossiping.GossipService/AddApproval',
                request_serializer=gossiping__pb2.AddApprovalRequest.SerializeToString,
                response_deserializer=empty__pb2.Empty.FromString,
                )
        self.StreamDagSliceBlockSummaries = channel.unary_stream(
                '/io.casperlabs.comm.gossiping.GossipService/StreamDagSliceBlockSummaries',
                request_serializer=gossiping__pb2.StreamDagSliceBlockSummariesRequest.SerializeToString,
                response_deserializer=consensus__pb2.BlockSummary.FromString,
                )


class GossipServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def NewBlocks(self, request, context):
        """Notify the callee about new blocks being available on the caller.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NewDeploys(self, request, context):
        """Notify the callee about new deploys being available on the caller.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamAncestorBlockSummaries(self, request, context):
        """Retrieve the ancestors of certain blocks in the DAG; to be called repeatedly
        as necessary to synchronize DAGs between peers.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamLatestMessages(self, request, context):
        """Retrieve latest messages as the callee knows them.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamBlockSummaries(self, request, context):
        """Retrieve arbitrary block summaries, if the callee knows about them.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamDeploySummaries(self, request, context):
        """Retrieve arbitrary deploy summaries, if the callee knows about them.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBlockChunked(self, request, context):
        """Retrieve an arbitrarily sized block as a stream of chunks, with optionally compressed content.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamDeploysChunked(self, request, context):
        """Retrieve an arbitrary list of deploys, with optionally compressed contents.
        One use case would be to gossip deploys between nodes so that they can be included
        in a block by the first validator who gets to propose a block. The second case is
        to retrieve all the deploys which are missing from the body of a block, i.e. haven't
        been downloaded yet as part of earlier blocks or deploy gossiping.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGenesisCandidate(self, request, context):
        """Retrieve the Genesis candidate supported by this node. Every node should either produce one from specification,
        get one from its bootstrap, or have it persisted from earlier runs.
        While the node is initializing and it hasn't obtained the candidate yet it will return UNAVAILABLE.
        Once the node is serving a candidate identity, it should also be prepared to serve the full block on request.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddApproval(self, request, context):
        """Add a signature to the list of approvals of a given candidate. If the block hash in the request doesn't match
        the callee's candidate it will return INVALID_ARGUMENT, otherwise add the signature and forward it to its peers.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamDagSliceBlockSummaries(self, request, context):
        """Returns block summaries between two ranks (inclusive) in ascending topological order.
        Used to gradually perform initial synchronization for new peers in the network.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GossipServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'NewBlocks': grpc.unary_unary_rpc_method_handler(
                    servicer.NewBlocks,
                    request_deserializer=gossiping__pb2.NewBlocksRequest.FromString,
                    response_serializer=gossiping__pb2.NewBlocksResponse.SerializeToString,
            ),
            'NewDeploys': grpc.unary_unary_rpc_method_handler(
                    servicer.NewDeploys,
                    request_deserializer=gossiping__pb2.NewDeploysRequest.FromString,
                    response_serializer=gossiping__pb2.NewDeploysResponse.SerializeToString,
            ),
            'StreamAncestorBlockSummaries': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamAncestorBlockSummaries,
                    request_deserializer=gossiping__pb2.StreamAncestorBlockSummariesRequest.FromString,
                    response_serializer=consensus__pb2.BlockSummary.SerializeToString,
            ),
            'StreamLatestMessages': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamLatestMessages,
                    request_deserializer=gossiping__pb2.StreamLatestMessagesRequest.FromString,
                    response_serializer=consensus__pb2.Block.Justification.SerializeToString,
            ),
            'StreamBlockSummaries': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamBlockSummaries,
                    request_deserializer=gossiping__pb2.StreamBlockSummariesRequest.FromString,
                    response_serializer=consensus__pb2.BlockSummary.SerializeToString,
            ),
            'StreamDeploySummaries': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamDeploySummaries,
                    request_deserializer=gossiping__pb2.StreamDeploySummariesRequest.FromString,
                    response_serializer=consensus__pb2.DeploySummary.SerializeToString,
            ),
            'GetBlockChunked': grpc.unary_stream_rpc_method_handler(
                    servicer.GetBlockChunked,
                    request_deserializer=gossiping__pb2.GetBlockChunkedRequest.FromString,
                    response_serializer=gossiping__pb2.Chunk.SerializeToString,
            ),
            'StreamDeploysChunked': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamDeploysChunked,
                    request_deserializer=gossiping__pb2.StreamDeploysChunkedRequest.FromString,
                    response_serializer=gossiping__pb2.Chunk.SerializeToString,
            ),
            'GetGenesisCandidate': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGenesisCandidate,
                    request_deserializer=gossiping__pb2.GetGenesisCandidateRequest.FromString,
                    response_serializer=consensus__pb2.GenesisCandidate.SerializeToString,
            ),
            'AddApproval': grpc.unary_unary_rpc_method_handler(
                    servicer.AddApproval,
                    request_deserializer=gossiping__pb2.AddApprovalRequest.FromString,
                    response_serializer=empty__pb2.Empty.SerializeToString,
            ),
            'StreamDagSliceBlockSummaries': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamDagSliceBlockSummaries,
                    request_deserializer=gossiping__pb2.StreamDagSliceBlockSummariesRequest.FromString,
                    response_serializer=consensus__pb2.BlockSummary.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'io.casperlabs.comm.gossiping.GossipService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GossipService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def NewBlocks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/io.casperlabs.comm.gossiping.GossipService/NewBlocks',
            gossiping__pb2.NewBlocksRequest.SerializeToString,
            gossiping__pb2.NewBlocksResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NewDeploys(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/io.casperlabs.comm.gossiping.GossipService/NewDeploys',
            gossiping__pb2.NewDeploysRequest.SerializeToString,
            gossiping__pb2.NewDeploysResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamAncestorBlockSummaries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/io.casperlabs.comm.gossiping.GossipService/StreamAncestorBlockSummaries',
            gossiping__pb2.StreamAncestorBlockSummariesRequest.SerializeToString,
            consensus__pb2.BlockSummary.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamLatestMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/io.casperlabs.comm.gossiping.GossipService/StreamLatestMessages',
            gossiping__pb2.StreamLatestMessagesRequest.SerializeToString,
            consensus__pb2.Block.Justification.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamBlockSummaries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/io.casperlabs.comm.gossiping.GossipService/StreamBlockSummaries',
            gossiping__pb2.StreamBlockSummariesRequest.SerializeToString,
            consensus__pb2.BlockSummary.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamDeploySummaries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/io.casperlabs.comm.gossiping.GossipService/StreamDeploySummaries',
            gossiping__pb2.StreamDeploySummariesRequest.SerializeToString,
            consensus__pb2.DeploySummary.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBlockChunked(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/io.casperlabs.comm.gossiping.GossipService/GetBlockChunked',
            gossiping__pb2.GetBlockChunkedRequest.SerializeToString,
            gossiping__pb2.Chunk.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamDeploysChunked(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/io.casperlabs.comm.gossiping.GossipService/StreamDeploysChunked',
            gossiping__pb2.StreamDeploysChunkedRequest.SerializeToString,
            gossiping__pb2.Chunk.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGenesisCandidate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/io.casperlabs.comm.gossiping.GossipService/GetGenesisCandidate',
            gossiping__pb2.GetGenesisCandidateRequest.SerializeToString,
            consensus__pb2.GenesisCandidate.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddApproval(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/io.casperlabs.comm.gossiping.GossipService/AddApproval',
            gossiping__pb2.AddApprovalRequest.SerializeToString,
            empty__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamDagSliceBlockSummaries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/io.casperlabs.comm.gossiping.GossipService/StreamDagSliceBlockSummaries',
            gossiping__pb2.StreamDagSliceBlockSummariesRequest.SerializeToString,
            consensus__pb2.BlockSummary.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
