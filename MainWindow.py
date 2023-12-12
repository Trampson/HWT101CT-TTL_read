from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
import sys
from AttitudeSensor import SerialReader

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

app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())
