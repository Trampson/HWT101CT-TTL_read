import serial
from PyQt5.QtCore import QThread, pyqtSignal

class SerialReader(QThread):
    data_received = pyqtSignal(bytes)

    def __init__(self, port='COM8', baudrate=9600, timeout=1):
        super().__init__()
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            if self.ser.in_waiting:
                data = self.ser.read(11)
                if len(data) == 11:
                    self.data_received.emit(data)

    def stop(self):
        self.running = False
        if self.ser.is_open:
            self.ser.close()

    @staticmethod
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

        elif data_type == 0x53:
            # 角度
            Yaw = ((data[7] << 8) | data[6]) if data[7] < 128 else (((data[7] << 8) | data[6]) - 65536)
            Yaw = Yaw / 32768 * 180  # 偏航角Z
            Version = (data[9] << 8) | data[8]  # 版本号
            return {"type": "Angle", "Yaw": Yaw, "Version": Version}

        else:
            return None

