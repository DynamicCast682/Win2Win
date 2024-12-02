import numpy as np
import pytest
import socket

from funcs import SocketFrame


# @pytest.fixture(scope='module')
# def server_socket():
#   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   server_socket.bind(('0.0.0.0', 1684))
#   server_socket.listen(1)
#   return server_socket
#
# @pytest.fixture(scope='module')
# def conn(server_socket):
#   conn, addr = server_socket.accept()
#   return conn
#
# def test_socketframe():
#   start_frame = SocketFrame(
#     None,
#     np.array([1, 2, 3])
#   )