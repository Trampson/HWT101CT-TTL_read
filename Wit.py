import struct
import logging

class WitDataParser:
    """
    WitDataParser handles the parsing of serial data according to a specific protocol.
    """

    PROTOCOL_HEADER = 0x55
    PACKET_LENGTH = 11
    MAX_BUFFER_SIZE = 256  # 定义最大缓冲区大小

    def __init__(self):
        """
        Initialize the DataParser.
        """
        self.logger = logging.getLogger(__name__)
        self.buffer = bytearray()

    def process_data_stream(self, stream_data):
        """
        Process the incoming data stream and extract complete data packets.
        """
        self.buffer.extend(stream_data)
        packets = []

        while len(self.buffer) >= self.PACKET_LENGTH:
            header_index = self.buffer.find(self.PROTOCOL_HEADER)

            # 保持缓冲区大小在合理范围内
            if len(self.buffer) > self.MAX_BUFFER_SIZE or header_index == -1:
                self.buffer = self.buffer[-self.MAX_BUFFER_SIZE:]
                break

            if header_index > 0:
                # 发现非数据包头部的数据，将其移除
                del self.buffer[:header_index]

            if len(self.buffer) < self.PACKET_LENGTH:
                break

            packet = self.buffer[:self.PACKET_LENGTH]
            if self._verify_checksum(packet):
                parsed_packet = self._parse_packet(packet)
                if parsed_packet:
                    packets.append(parsed_packet)
                del self.buffer[:self.PACKET_LENGTH]
            else:
                # 校验和失败，移除头部，寻找下一个可能的数据包
                self.logger.error("Checksum mismatch.")
                del self.buffer[0]

        return packets

    def _parse_packet(self, packet):
        """
        Parse a single data packet.
        """
        _, type_byte, *data_bytes, _ = packet
        parsed_data = {'type': type_byte, 'data': []}
        for i in range(0, len(data_bytes), 2):
            data = self._convert_to_short(data_bytes[i], data_bytes[i + 1])
            parsed_data['data'].append(data)
        return parsed_data

    @staticmethod
    def _convert_to_short(low_byte, high_byte):
        """
        Convert two bytes (low and high) to a signed short value.
        """
        return struct.unpack('<h', bytes([low_byte, high_byte]))[0]

    @staticmethod
    def _verify_checksum(packet):
        """
        Verify the checksum of the given data packet.
        """
        checksum = sum(packet[:-1]) & 0xFF
        return checksum == packet[-1]

# Example Usage
# parser = WitDataParser()
# while serial_data_available:
#     raw_data = read_serial_data()
#     for parsed_data in parser.process_data_stream(raw_data):
#         print("Parsed Data:", parsed_data)
