# https://github.com/sparkfun/SparkFun_ISL29125_Breakout_Arduino_Library/blob/master/src/SparkFunISL29125.h
# https://github.com/sparkfun/ISL29125_Breakout/blob/V_H1.0_L1.0.1/Libraries/Arduino/examples/ISL29125Basics/ISL29125Basics.ino

#!/usr/bin/env python3

import smbus
import time

class BrightnessSensor:

    # hardware
    DEVICE_BUS = 1                                  # 0 gives Remote I/O error aka no device
    DEVICE_ADDR = 0x44

    # ISL29125 Registers
    DEVICE_ID = 0x00
    CONFIG_1 = 0x01
    CONFIG_2 = 0x02
    CONFIG_3 = 0x03
    THRESHOLD_LL = 0x04
    THRESHOLD_LH = 0x05
    THRESHOLD_HL = 0x06
    THRESHOLD_HH = 0x07
    STATUS = 0x08 
    GREEN_L = 0x09 
    GREEN_H = 0x0A
    RED_L = 0x0B
    RED_H = 0x0C
    BLUE_L = 0x0D
    BLUE_H = 0x0E

    # Configuration Settings
    CFG_DEFAULT = 0x00

    # CONFIG1
    # Pick a mode, determines what color[s] the sensor samples, if any
    CFG1_MODE_POWERDOWN = 0x00
    CFG1_MODE_G = 0x01
    CFG1_MODE_R = 0x02
    CFG1_MODE_B = 0x03
    CFG1_MODE_STANDBY = 0x04
    CFG1_MODE_RGB = 0x05
    CFG1_MODE_RG = 0x06
    CFG1_MODE_GB = 0x07

    # Light intensity range
    # In a dark environment 375Lux is best, otherwise 10KLux is likely the best option
    CFG1_375LUX = 0x00
    CFG1_10KLUX = 0x08

    # Change this to 12 bit if you want less accuracy, but faster sensor reads
    # At default 16 bit, each sensor sample for a given color is about ~100ms
    CFG1_16BIT = 0x00
    CFG1_12BIT = 0x10

    # Unless you want the interrupt pin to be an input that triggers sensor sampling, leave this on normal
    CFG1_ADC_SYNC_NORMAL = 0x00
    CFG1_ADC_SYNC_TO_INT = 0x20

    # CONFIG2
    # Selects upper or lower range of IR filtering
    CFG2_IR_OFFSET_OFF = 0x00
    CFG2_IR_OFFSET_ON = 0x80

    # Sets amount of IR filtering, can use these presets or any value between 0x00 and 0x3F
    # Consult datasheet for detailed IR filtering calibration
    CFG2_IR_ADJUST_LOW = 0x00
    CFG2_IR_ADJUST_MID = 0x20
    CFG2_IR_ADJUST_HIGH = 0x3F

    # CONFIG3
    # No interrupts, or interrupts based on a selected color
    CFG3_NO_INT = 0x00
    CFG3_G_INT = 0x01
    CFG3_R_INT = 0x02
    CFG3_B_INT = 0x03

    # How many times a sensor sample must hit a threshold before triggering an interrupt
    # More consecutive samples means more times between interrupts, but less triggers from short transients
    CFG3_INT_PRST1 = 0x00
    CFG3_INT_PRST2 = 0x04
    CFG3_INT_PRST4 = 0x08
    CFG3_INT_PRST8 = 0x0C

    # If you would rather have interrupts trigger when a sensor sampling is complete, enable this
    # If this is disabled, interrupts are based on comparing sensor data to threshold settings
    CFG3_RGB_CONV_TO_INT_DISABLE = 0x00
    CFG3_RGB_CONV_TO_INT_ENABLE = 0x10

    # STATUS FLAG MASKS
    FLAG_INT = 0x01
    FLAG_CONV_DONE = 0x02
    FLAG_BROWNOUT = 0x04
    FLAG_CONV_G = 0x10
    FLAG_CONV_R = 0x20
    FLAG_CONV_B = 0x30

    # Initializes brightness sensor to default configurations:
    # RGB detection and 10k sampling rate, maximum infrared filtering, no interrupts
    def __init__(self):
        self.bus = smbus.SMBus(self.DEVICE_BUS)                                                          # bus used to read / write
        self.bus.write_byte_data(self.DEVICE_ADDR, self.CONFIG_1, self.CFG1_MODE_RGB | self.CFG1_10KLUX) # configure mode & rate
        self.bus.write_byte_data(self.DEVICE_ADDR, self.CONFIG_2, self.CFG2_IR_ADJUST_HIGH)              # configure infrared filtering
        self.bus.write_byte_data(self.DEVICE_ADDR, self.CONFIG_3, self.CFG_DEFAULT)                      # we don't need interrupts

    # Returns value of blue register
    def read_blue(self) -> (int):
        return (self.bus.read_word_data(self.DEVICE_ADDR, self.BLUE_L))

    # Returns value of red register
    def read_red(self) -> (int):
        return (self.bus.read_word_data(self.DEVICE_ADDR, self.RED_L))
    
    # Returns value of green register
    def read_green(self) -> (int):
        return (self.bus.read_word_data(self.DEVICE_ADDR, self.GREEN_L))

    # Returns current brightness value
    def get_brightness(self):
        with open("/sys/class/backlight/10-0045/brightness", "r") as f:
            return f.read()
    
    # Writes new brightness value
    # new_brightness should be between 0 and 255
    # new_brightness can be a string or an int
    def write_brightness(self, new_brightness):
        with open("/sys/class/backlight/10-0045/brightness", "w") as f:
            f.write(str(new_brightness))
    
    def test():
        sensor = BrightnessSensor()
        cont = "y"
        while (cont == "y"):
            print(sensor.read_blue())
            print(sensor.read_red())
            print(sensor.read_green())
            print(sensor.get_brightness())
            print("enter next value")
            new_brightness = input()
            sensor.write_brightness(new_brightness)
            print("continue? y/n")
            cont = input()
        sensor.write_brightness(128)                    # reset brightness before exiting

    def test_values():
        sensor = BrightnessSensor()
        for i in range(20):
            print(str(i) + " blue: " + str(sensor.read_blue()) + " red: " + str(sensor.read_red()) + " green: " + str(sensor.read_green()))
            time.sleep(0.2)
            
    
#BrightnessSensor.test()
BrightnessSensor.test_values()
