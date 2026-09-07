import socket
import struct 
import textwrap

# unpack ethernet frame 
"""
we see some data flowing across the network and then we pass it into
this function, when the data is passed it grabs the first 14 bytes(dest, source, type) and 
unpacks it and then returns all the data after 
"""
def ethernet_frame(data):
    dest_mac, source_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return  get_mac_addr(dest_mac),get_mac_addr(source_mac), socket.htons(proto), data[14:]

# Return properly formatted mac address (ie AA:BB:CC:DD:EE)
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr) 
    return ':'.join(bytes_str).upper() 










