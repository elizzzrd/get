import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time
import adcplot
from r2r_adc import R2R_ADC


#======================================================================
# SAR ADC — Successive Approximation Register ADC

voltage_values = []
time_values = []
duration = 3.0
adc = R2R_ADC(3.300)

try:
    start_time = time.time_ns()
    time_0 = start_time

    while ((time_0 - start_time) / 1e9 < duration):
        time_0 = time.time_ns()
        volt = adc.get_sar_voltage()
        
        print(volt, (time_0 - start_time) / 1e9)

        time_values.append((time_0 - start_time) / 1e9)
        voltage_values.append(volt)

    adcplot.plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
    adcplot.plot_sampling_period_hist(time_values)
        
finally:
    adc.deinit()