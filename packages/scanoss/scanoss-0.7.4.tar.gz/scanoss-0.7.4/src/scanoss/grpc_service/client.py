"""
 SPDX-License-Identifier: MIT

   Copyright (c) 2021, SCANOSS

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
"""

import os
import logging
import grpc
from .unary_pb2_grpc import UnaryStub
from .unary_pb2 import Message
from ..scanossbase import ScanossBase

# DEFAULT_URL      = "https://osskb.org/api/scan/direct"
DEFAULT_URL      = "localhost:9000"
SCANOSS_GRPC_URL = os.environ.get("SCANOSS_GRPC_URL") if os.environ.get("SCANOSS_GRPC_URL") else DEFAULT_URL

class ScanossGrpcClient(ScanossBase):
    """
    Client for gRPC functionality
    """

    def __init__(self, url: str = None, debug: bool = False, trace: bool = False, quiet: bool = False):
        """

        :param url:
        :param debug:
        :param trace:
        :param quiet:
        """
        logging.basicConfig(level=logging.DEBUG)
        self.debug = debug
        self.quiet = quiet
        self.trace = trace
        self.url = url if url else SCANOSS_GRPC_URL
        self.channel = grpc.insecure_channel(self.url)  # instantiate a channel
        self.stub = UnaryStub(self.channel)             # bind the client and the server

    def request(self, message: str = None):
        """
        Client function to call the rpc for GetServerResponse
        :param message: Message to send to the service
        :return: Server response or None
        """
        if not message:
            self.print_stderr(f'ERROR: No message supplied to send to gRPC service.')
            return None
        try:
            return self.stub.GetServerResponse(Message(message=message))
        except Exception as e:
            self.print_stderr(f'ERROR: Problem encountered sending gRPC message: {e}')
        return None
    

