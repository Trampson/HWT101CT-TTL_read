from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


class SerialModule(QThread):
    """
    SerialModule handles serial communication using QSerialPort in an event-driven manner.
    It automatically detects the serial port and configures it for non-blocking reads.
    """
    data_received = pyqtSignal(bytes)
    error_occurred = pyqtSignal(str)

    def __init__(self, baudrate=9600):
        """
        Initialize the SerialModule with specified baudrate.

        :param baudrate: The baud rate for serial communication.
        """
        super(SerialModule, self).__init__()
        self.baudrate = baudrate
        self.serial_port = QSerialPort()
        self.serial_port.readyRead.connect(self.read_data)
        self._configure_serial_port()

    def close_serial_port(self):
        """
        Closes the serial port.
        """
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.close()

    def _configure_serial_port(self):
        """
        Configures the serial port by automatically detecting and setting it up.
        """
        try:
            port = self._auto_detect_serial_port()
            if port:
                self.serial_port.setPortName(port)
                self.serial_port.setBaudRate(self.baudrate)

                if not self.serial_port.open(QSerialPort.ReadWrite):
                    self.error_occurred.emit("Failed to open serial port.")
            else:
                self.error_occurred.emit("No serial port found. Please check your connections.")
        except Exception as e:
            self.error_occurred.emit(f"Error opening serial port: {str(e)}")

    @staticmethod
    def _auto_detect_serial_port():
        """
        Automatically detects the serial ports and returns the first one found.

        :return: The detected serial port name or None if no port is found.
        """
        ports = QSerialPortInfo.availablePorts()
        return ports[0].portName() if ports else None

    def read_data(self):
        """
        Reads data from the serial port and emits a signal with the received data.
        This method is called when the readyRead signal is emitted.
        """
        try:
            if self.serial_port and self.serial_port.isOpen():
                data = self.serial_port.readAll()
                self.data_received.emit(bytes(data))
        except Exception as e:
            self.error_occurred.emit(f"Error reading serial port: {str(e)}")

# Example Usage
# serial_module = SerialModule()
# serial_module.data_received.connect(lambda data: print("Data Received:", data))
# serial_module.error_occurred.connect(lambda error: print("Error:", error))
# serial_module.start()
