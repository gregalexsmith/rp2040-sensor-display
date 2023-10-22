from constants import GRAPH_WIDTH


class SensorData:
    def __init__(self):
        self.data = {"co2": None, "temp": None, "hum": None}
        self.min_data = {"co2": float('inf'), "temp": float(
            'inf'), "hum": float('inf')}
        self.max_data = {"co2": float(
            '-inf'), "temp": float('-inf'), "hum": float('-inf')}
        self.past_values = {"co2": [], "temp": [], "hum": []}

    def update_min_max(self, co2, temp, hum):
        self.min_data["co2"] = min(self.min_data["co2"], co2)
        self.min_data["temp"] = min(self.min_data["temp"], temp)
        self.min_data["hum"] = min(self.min_data["hum"], hum)

        self.max_data["co2"] = max(self.max_data["co2"], co2)
        self.max_data["temp"] = max(self.max_data["temp"], temp)
        self.max_data["hum"] = max(self.max_data["hum"], hum)

    def add_past_values(self, co2, temp, hum):
        self.past_values["co2"].append(co2)
        self.past_values["temp"].append(temp)
        self.past_values["hum"].append(hum)
        for key in self.past_values:
            if len(self.past_values[key]) > GRAPH_WIDTH:
                self.past_values[key] = self.past_values[key][-GRAPH_WIDTH:]


class SensorDataManager:
    def __init__(self, sensor):
        self.sensor = sensor
        self.data = {"co2": None, "temp": None, "hum": None}
        self.sensor_data = SensorData()

    def fetch_and_update_data(self):
        co2, temp, hum = self.sensor.fetch_data()
        self.sensor_data.data["co2"], self.sensor_data.data["temp"], self.sensor_data.data["hum"] = co2, temp, hum
        self.sensor_data.add_past_values(co2, temp, hum)
        self.sensor_data.update_min_max(co2, temp, hum)

    def data_available(self):
        return self.sensor.data_available()

    def get_data(self):
        return self.sensor_data
