import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import adc_plot
from r2r_adc import R2R_ADC


#======================================================================
# ADC SC (последовательного счета)

voltage_values = []
time_values = []
duration = 1.0
dynamic_range = 3.3
print(dy)

adc = R2R_ADC(dynamic_range, compare_time=0.0001)

try:
    start_time = time.time_ns()     # return nanoseconds
    time_0 = start_time
    print(start_time)

    while (time_0 - start_time) / 1e9 < duration:
        print("in cycle")
        time_0 = time.time_ns()
        print(time_0)
        print((time_0 - start_time) / 1e9)
        volt = adc.get_sc_voltage()

        print(volt, (time_0 - start_time) / 1e9)

        time_values.append((time_0 - start_time) / 1e9)
        voltage_values.append(volt)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
    adc_plot.plot_sampling_period_hist(time_values)


finally:
    adc.deinit()