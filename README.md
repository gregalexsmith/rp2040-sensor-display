# Adafruit Sensor Board

A sensor board with CircuitPython and the Adafruit Feather Series using the following hardware:

- [Adafruit Feather RP2040](https://www.adafruit.com/product/4884)
- [Adafruit FeatherWing OLED](https://www.adafruit.com/product/4650).
- [Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor](https://www.adafruit.com/product/4867)

## Development

The code in this repo is a copy of the code running on the device. To develop changes:

1. plug in the device
1. open the Mu editor to see serial output
1. run `code /Volumes/CIRCUITPY` to open the directory in VS Code

Once changes have been made and tested, commit them by:

1. running `./copyfiles` to copy the files from the device to this repo
1. commit the changes