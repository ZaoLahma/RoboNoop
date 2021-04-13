class DriverContext():
    def __init__(self):
        self.drivers = {}

    def add_driver(self, driver_id, driver):
        self.drivers[driver_id] = driver

    def get_driver(self, driver_id):
        return self.drivers[driver_id]