import board
import busio
import adafruit_scd30


class SCD30Sensor:
    def __init__(self, i2c=None):
        # setup board
        if i2c is None:
            self.i2c = board.I2C()
        else:
            self.i2c = i2c
        # self.i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
        self.scd = adafruit_scd30.SCD30(self.i2c)

        # Initialization logic
        # scd.temperature_offset = 10
        print("Temperature offset:", self.scd.temperature_offset)
        self.scd.measurement_interval = 4
        print("Measurement interval:", self.scd.measurement_interval)
        self.scd.self_calibration_enabled = False
        print("Self-calibration enabled:", self.scd.self_calibration_enabled)
        self.scd.ambient_pressure = 1017.99
        print("Ambient Pressure:", self.scd.ambient_pressure)
        self.scd.altitude = 127.136
        print("Altitude:", self.scd.altitude, "meters above sea level")
        self.scd.forced_recalibration_reference = 409
        print("Forced recalibration reference:",
              self.scd.forced_recalibration_reference)
        print("")

    def data_available(self):
        return self.scd.data_available

    def fetch_data(self):
        return self.scd.CO2, self.scd.temperature, self.scd.relative_humidity
