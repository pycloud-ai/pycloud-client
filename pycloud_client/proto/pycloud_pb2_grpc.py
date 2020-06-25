#
# Copyright (C) 2020 PyCloud - All Rights Reserved
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import grpc

import pycloud_client.proto.pycloud_pb2 as pycloud__pb2


class EndpointStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.ProcessRequest = channel.unary_unary(
            "/pycloud.ai.Endpoint/ProcessRequest",
            request_serializer=pycloud__pb2.Request.SerializeToString,
            response_deserializer=pycloud__pb2.Response.FromString,
        )


class EndpointServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def ProcessRequest(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_EndpointServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ProcessRequest": grpc.unary_unary_rpc_method_handler(
            servicer.ProcessRequest,
            request_deserializer=pycloud__pb2.Request.FromString,
            response_serializer=pycloud__pb2.Response.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "pycloud.ai.Endpoint", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
