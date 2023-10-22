import displayio
import terminalio
from adafruit_display_text import label
from constants import GRAPH_WIDTH, GRAPH_HEIGHT


class SensorView:
    def __init__(self, oled):
        self.bitmap = displayio.Bitmap(128, 32, 2)
        self.palette = displayio.Palette(2)
        self.palette[0] = 0x000000
        self.palette[1] = 0xffffff
        self.tile_grid = displayio.TileGrid(
            self.bitmap, pixel_shader=self.palette)

        self.group = displayio.Group()
        oled.show(self.group)
        self.group.append(self.tile_grid)

        self.text_area_co2 = label.Label(
            terminalio.FONT, text="", color=0xFFFF00, x=0, y=8)
        self.text_area_temp = label.Label(
            terminalio.FONT, text="", color=0xFFFF00, x=0, y=18)
        self.text_area_hum = label.Label(
            terminalio.FONT, text="", color=0xFFFF00, x=0, y=28)
        self.group.append(self.text_area_co2)
        self.group.append(self.text_area_temp)
        self.group.append(self.text_area_hum)

    def clear_bitmap(self):
        for x in range(128):
            for y in range(32):
                self.bitmap[x, y] = 0

    def draw_graph(self, data_list, y_position):
        min_val = min(data_list)
        max_val = max(data_list)
        range_val = max_val - min_val if max_val != min_val else 1

        for i in range(min(GRAPH_WIDTH, len(data_list))):
            val = data_list[-(i+1)]
            normalized_val = ((val - min_val) / range_val) * GRAPH_HEIGHT
            self.bitmap[GRAPH_WIDTH - i, y_position +
                        GRAPH_HEIGHT - int(normalized_val)] = 1

    def update_display(self, mode, sensor_data):
        data = sensor_data.data
        min_data = sensor_data.min_data
        max_data = sensor_data.max_data
        past_values = sensor_data.past_values

        if mode == 'A':
            self.clear_bitmap()
            if data["co2"] is not None:
                self.text_area_co2.text = "CO2: %d PPM" % data["co2"]
                self.text_area_temp.text = "Temp: %0.1f C" % data["temp"]
                self.text_area_hum.text = "Hum: %0.1f %%" % data["hum"]
        elif mode == 'B':
            self.clear_bitmap()
            self.text_area_co2.text = "CO2: %d-%d PPM" % (
                min_data["co2"], max_data["co2"])
            self.text_area_temp.text = "Temp: %0.1f-%0.1f C" % (
                min_data["temp"], max_data["temp"])
            self.text_area_hum.text = "Hum: %0.1f-%0.1f %%" % (
                min_data["hum"], max_data["hum"])
        elif mode == 'C':
            self.clear_bitmap()
            self.text_area_co2.text = ""
            self.text_area_temp.text = ""
            self.text_area_hum.text = ""
            self.draw_graph(past_values["co2"], 0)
            self.draw_graph(past_values["temp"], 10)
            self.draw_graph(past_values["hum"], 23)

    def enter_sleep_mode(self):
        self.clear_bitmap()
        self.text_area_co2.text = ""
        self.text_area_temp.text = ""
        self.text_area_hum.text = ""
