# HWT101CT-TTL_read

## 项目简介
这个项目提供了一个使用 PyQt 和 pySerial 库与 Wit-Motion 铝壳倾角仪和惯导传感器 HWT101CT-TTL 通信的接口。该接口允许用户通过串口连接读取角速度和角度数据。项目旨在提供一个简洁、易用的接口，以便开发者和爱好者能够轻松集成和使用这些传感器。

## 主要特性
- **串口通信**：使用 pySerial 库实现与 Wit-Motion 传感器的串口通信。
- **数据读取**：能够读取传感器提供的角速度和角度数据。
- **PyQt GUI**：包含一个基于 PyQt 的 MainWindow 类，展示了如何在 PyQt 应用程序中调用和显示数据。
- **灵活性**：read_serial_data.py 脚本可以独立运行，用于直接从串口读取数据。
- **封装性**：AttitudeSensor.py 中封装了 SerialReader 类，其中包含用于解析传感器数据的静态方法 parse_data。

## 安装
要使用本项目，你需要先安装以下依赖：

```bash
pip install pyqt5 pyserial
```

## 使用说明
1. 在SerialReader中设置好读取信号的串口，确保程序内的串口与设备所连接的串口保持一致

2. 运行 read_serial_data.py 以直接从串口读取数据。

3. 在 AttitudeSensor.py 中，SerialReader 类提供了读取和解析数据的功能。你可以在此基础上进行扩展或集成到你的应用程序中。

4. 若要查看 PyQt GUI 示例，请运行 MainWindow。

## 贡献
欢迎对本项目进行贡献！如果你有任何改进意见或功能请求，请提交 Pull Request 或开 Issue。

## License
This project is licensed under the [MIT License](LICENSE).

## 许可
该项目采用 MIT 许可证。
