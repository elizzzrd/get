import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time
import adc_plot


#======================================================================
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):

        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)


    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()


    def number_to_dac(self, number):
        GPIO.output(self.bits_gpio, [int(element) for element in bin(number)[2:].zfill(8)])
    
    
    def sequential_counting_adc(self):
        num = 0
        self.number_to_dac(num)
        time.sleep(self.compare_time)

        while(not GPIO.input(self.comp_gpio)):
            time.sleep(self.compare_time)
            num += 1
            if num > 255:
                break
            self.number_to_dac(num)
        self.number_to_dac(0)
        return num
    
    def successive_approximation_adc(self):
        result = 0
        
        for i in range(7, -1, -1):          
            probe = result | (1 << i)       # устанавливаем пробный бит
            self.number_to_dac(probe)       
            time.sleep(self.compare_time)
            
            if not GPIO.input(self.comp_gpio):  # Uцап <= Uвх
                result = probe                  # оставляем бит
            
        self.number_to_dac(0)
        return result
    

    def get_sc_voltage(self):
        return self.sequential_counting_adc() * self.dynamic_range / 255
    
    def get_sar_voltage(self):
        return self.successive_approximation_adc() * self.dynamic_range / 255


#======================================================================

dynamic_range = 3.3

try:
    adc = R2R_ADC(dynamic_range)

    while True:
        #volt = adc.get_sc_voltage()
        volt = adc.get_sar_voltage()
        print(f"Напряжение: {volt:.3f} В")
        time.sleep(0.1)

finally:
    adc.deinit()