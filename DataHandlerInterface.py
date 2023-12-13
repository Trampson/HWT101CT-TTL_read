import logging
import threading

class DataHandlerInterface:
    """
    Interface for all data handlers.
    """
    def process_data(self, data):
        raise NotImplementedError

class AngularVelocityHandler(DataHandlerInterface):
    def __init__(self):
        self.lock = threading.Lock()

    def process_data(self, data):
        with self.lock:
            # Thread-safe processing of angular velocity data
            # ...
            processed_data = {'Wy': data[1]/32768*2000, 'Wz': data[2]/32768*2000}

            return processed_data

class AngleHandler(DataHandlerInterface):
    def __init__(self):
        self.lock = threading.Lock()

    def process_data(self, data):
        with self.lock:
            # Thread-safe processing of angle data
            # ...
            processed_data = {'Yaw': data[2]/32768*180, 'Version': data[3]}
            return processed_data

class DataProcessorFactory:
    def create_processor(self, type_byte):
        if type_byte == 0x52:
            return AngularVelocityHandler()
        elif type_byte == 0x53:
            return AngleHandler()
        else:
            return None

class DataProcessor:
    def __init__(self):
        self.factory = DataProcessorFactory()
        self.logger = logging.getLogger(__name__)

    def process_parsed_data(self, parsed_data):
        processor = self.factory.create_processor(parsed_data['type'])
        if processor:
            try:
                return processor.process_data(parsed_data['data'])
            except Exception as e:
                self.logger.exception(f"Error processing data: {e}")
                return None
        else:
            self.logger.error(f"No processor found for type: {parsed_data['type']}")
            return None

# Example Usage
# ...
