class DataProcessor:
    def __init__(self):
        self.data = []

    def add_data(self, new_data):
        self.data.append(new_data)

processor = DataProcessor()
processor.add_data("New Entry")
print(processor.data)