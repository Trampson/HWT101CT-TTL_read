import serial
import struct

def parse_data(data):
    # 检查协议头和数据长度
    if data[0] != 0x55 or len(data) != 11:
        print("Invalid data")
        return None

    # 检查校验和
    if sum(data[:-1]) % 256 != data[-1]:
        print("Checksum error")
        return None

    # 解析数据
    type = data[1]
    data1 = struct.unpack('<h', bytes(data[2:4]))[0]
    data2 = struct.unpack('<h', bytes(data[4:6]))[0]
    data3 = struct.unpack('<h', bytes(data[6:8]))[0]
    data4 = struct.unpack('<h', bytes(data[8:10]))[0]

    return type, data1, data2, data3, data4

def read_serial_data():
    ser = serial.Serial('COM8', 9600, timeout=1)

    try:
        while True:
            # 读取11字节的数据
            data = ser.read(11)
            if len(data) == 11:
                parsed_data = parse_data(data)
                if parsed_data:
                    print("Type:", parsed_data[0], "Data:", parsed_data[1:])
    except KeyboardInterrupt:
        ser.close()
        print('Serial connection closed')

read_serial_data()
