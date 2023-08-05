import logging
import GetData

class DataFormation:
    def __init__(self, columns, data):
        self.columns = columns
        self.data = data

    def formData(self):
        logging.info("Forming Data...")
        return self.data