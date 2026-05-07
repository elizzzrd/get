import smbus
import RPi.GPIO as GPIO
import time
import adc_plot


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


voltage_values = []
time_values = []
duration = 5.0
adc = MCP3021(3.300)

try:
    start_time = time.time_ns()
    time_0 = start_time
    while ((time_0 - start_time) / 1e9 < duration):
        time_0 = time.time_ns()
        volt = adc.get_voltage()
        print(volt)
        time_values.append((time_0 - start_time) / 1e9)
        voltage_values.append(volt)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
    adc_plot.plot_sampling_period_hist(time_values)
        
finally:
    adc.deinit()
    