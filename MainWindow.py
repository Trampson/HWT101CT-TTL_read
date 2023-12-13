from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, QThread
import sys
from queue import Queue
from SerialModule import SerialModule
from Wit import WitDataParser
from DataHandlerInterface import DataProcessor

class MainWindow(QMainWindow):
    """
    主窗口类，负责初始化 UI 和数据处理线程。
    """
    update_text_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_processing_thread()

    def init_ui(self):
        """
        初始化用户界面。
        """
        self.text_edit = QTextEdit(self)
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Data Processing Application")

    def setup_processing_thread(self):
        """
        设置并启动数据处理线程。
        """
        self.data_queue = Queue()
        self.data_processor = DataProcessor()
        self.data_thread = DataProcessingThread(self.data_queue, self.data_processor, self.update_text_signal)
        self.update_text_signal.connect(self.update_text_edit)
        self.data_thread.start()

    def update_text_edit(self, text):
        """
        更新文本编辑框的内容。
        """
        self.text_edit.append(text)

    def closeEvent(self, event):
        """
        处理窗口关闭事件，确保线程和资源被适当清理。
        """
        self.data_queue.put(None)
        self.data_thread.wait()
        super().closeEvent(event)

class DataProcessingThread(QThread):
    """
    数据处理线程类，负责从数据队列中读取并处理数据。
    """
    def __init__(self, data_queue, data_processor, update_signal):
        super().__init__()
        self.data_queue = data_queue
        self.data_processor = data_processor
        self.update_signal = update_signal

    def run(self):
        """
        线程运行函数，从队列中读取数据并处理。
        """
        while True:
            raw_data = self.data_queue.get()
            if raw_data is None:
                break
            parsed_data = WitDataParser().process_data_stream(raw_data)
            for data_packet in parsed_data:
                processed_data = self.data_processor.process_parsed_data(data_packet)
                self.update_signal.emit(str(processed_data))

def main():
    """
    应用程序的主入口点。
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    serial_module = SerialModule()
    serial_module.data_received.connect(lambda data: main_window.data_queue.put(data))
    serial_module.error_occurred.connect(lambda error: print("Error:", error))
    serial_module.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
