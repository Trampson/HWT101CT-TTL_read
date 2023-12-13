from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
import sys
from AttitudeSensor import SerialReader
from queue import Queue
from threading import Thread
from SerialModule import SerialModule
from Wit import WitDataParser
from DataHandlerInterface import DataProcessor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.serialReader = SerialReader()
        self.serialReader.data_received.connect(self.handleDataReceived)
        self.serialReader.start()

    def initUI(self):
        # 初始化UI组件
        self.textEdit = QTextEdit(self)
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def handleDataReceived(self, data):
        # 处理接收到的数据
        parsed_data = SerialReader.parse_data(data)
        # 更新UI或其他处理
        self.textEdit.append(str(parsed_data))

    def closeEvent(self, event):
        self.serialReader.stop()
        super().closeEvent(event)


class DataProcessingThread(Thread):
    def __init__(self, data_queue, data_processor):
        super().__init__()
        self.data_queue = data_queue
        self.data_processor = data_processor

    def run(self):
        while True:
            raw_data = self.data_queue.get()
            if raw_data is None:
                break  # 结束线程
            parsed_data = WitDataParser().process_data_stream(raw_data)
            for data_packet in parsed_data:
                processed_data = self.data_processor.process_parsed_data(data_packet)
                print("Final Processed Data:", processed_data)
                # 这里可以进一步处理数据或将数据发送到其他模块


def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()

    # 创建队列和处理器
    data_queue = Queue()
    data_processor = DataProcessor()

    # 创建并配置串口模块
    serial_module = SerialModule()
    serial_module.data_received.connect(lambda data: data_queue.put(data))
    serial_module.error_occurred.connect(lambda error: print("Error:", error))
    serial_module.start()

    # 启动数据处理线程
    processing_thread = DataProcessingThread(data_queue, data_processor)
    processing_thread.start()

    # 启动事件循环
    exit_code = app.exec_()

    # 清理和退出
    data_queue.put(None)  # 发送结束信号
    processing_thread.wait()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

# app = QApplication(sys.argv)
# mainWin = MainWindow()
# mainWin.show()
# sys.exit(app.exec_())