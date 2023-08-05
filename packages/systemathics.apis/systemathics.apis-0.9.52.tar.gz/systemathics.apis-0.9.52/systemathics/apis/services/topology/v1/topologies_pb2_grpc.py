# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from systemathics.apis.services.topology.v1 import topologies_pb2 as systemathics_dot_apis_dot_services_dot_topology_dot_v1_dot_topologies__pb2


class TopologiesServiceStub(object):
    """Called to request topology over a look back-period with a given time granularity.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Topologies = channel.unary_unary(
                '/systemathics.apis.services.topology.v1.TopologiesService/Topologies',
                request_serializer=systemathics_dot_apis_dot_services_dot_topology_dot_v1_dot_topologies__pb2.TopologiesRequest.SerializeToString,
                response_deserializer=systemathics_dot_apis_dot_services_dot_topology_dot_v1_dot_topologies__pb2.TopologiesResponse.FromString,
                )


class TopologiesServiceServicer(object):
    """Called to request topology over a look back-period with a given time granularity.
    """

    def Topologies(self, request, context):
        """Gets topology per a given time granularity
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TopologiesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Topologies': grpc.unary_unary_rpc_method_handler(
                    servicer.Topologies,
                    request_deserializer=systemathics_dot_apis_dot_services_dot_topology_dot_v1_dot_topologies__pb2.TopologiesRequest.FromString,
                    response_serializer=systemathics_dot_apis_dot_services_dot_topology_dot_v1_dot_topologies__pb2.TopologiesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'systemathics.apis.services.topology.v1.TopologiesService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TopologiesService(object):
    """Called to request topology over a look back-period with a given time granularity.
    """

    @staticmethod
    def Topologies(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/systemathics.apis.services.topology.v1.TopologiesService/Topologies',
            systemathics_dot_apis_dot_services_dot_topology_dot_v1_dot_topologies__pb2.TopologiesRequest.SerializeToString,
            systemathics_dot_apis_dot_services_dot_topology_dot_v1_dot_topologies__pb2.TopologiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
