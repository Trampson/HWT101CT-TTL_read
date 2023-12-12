import serial
import struct


def parse_data(data):
    # 检查协议头和校验和
    if data[0] != 0x55 or (sum(data[:-1]) & 0xFF) != data[-1]:
        return None

    data_type = data[1]
    if data_type == 0x52:
        # 角速度
        Wy = ((data[5] << 8) | data[4]) if data[5] < 128 else (((data[5] << 8) | data[4]) - 65536)
        Wz = ((data[7] << 8) | data[6]) if data[7] < 128 else (((data[7] << 8) | data[6]) - 65536)
        Wy = Wy / 32768 * 2000  # 角速度y
        Wz = Wz / 32768 * 2000  # 角速度z
        return {"type": "Angular Velocity", "Wy": Wy, "Wz": Wz}
        # return Wy, Wz

    elif data_type == 0x53:
        # 角度
        Yaw = ((data[7] << 8) | data[6]) if data[7] < 128 else (((data[7] << 8) | data[6]) - 65536)
        Yaw = Yaw / 32768 * 180  # 偏航角Z
        Version = (data[9] << 8) | data[8]  # 版本号
        return {"type": "Angle", "Yaw": Yaw, "Version": Version}
        #return Yaw, Version

    else:
        return None

def read_serial_data():
    ser = serial.Serial('COM8', 9600, timeout=1)

    try:
        while True:
            # 读取11字节的数据
            data = ser.read(11)
            if len(data) == 11:
                parsed_data = parse_data(data)
                if parsed_data:
                    print(parsed_data)
    except KeyboardInterrupt:
        ser.close()
        print('Serial connection closed')

read_serial_data()
