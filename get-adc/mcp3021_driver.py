import smbus
import time

class MCP3021:
    def __init__(self, dynamic_range, verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose


    def deinit(self):
        self.bus.close()


    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)

        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF

        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        
        if self.verbose:
            print(f"Принятые данные: {data}," 
                   "Старший байт: {upper_data_byte:x}," 
                   "Младший байт: {lower_data_byte:x}," 
                   "Число: {number}")
        return number
    

    def get_voltage(self):
        return self.get_number() / 1023*self.dynamic_range
    
#======================================================================
# raspi-gpio set 2 a0
# raspi-gpio set 3 a0

dynamic_range = 5

if __name__ == "__main__":
    try:
        mcp = MCP3021(dynamic_range)

        while True:
            volt = mcp.get_voltage()
            print(f"Напряжение: {volt:.3f} В")
            time.sleep(0.5)

    finally:
        mcp.deinit()