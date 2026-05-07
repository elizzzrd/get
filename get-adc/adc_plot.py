import matplotlib.pyplot as plt
import numpy as np

def plot_voltage_vs_time(time, voltage, max_voltage):

    plt.figure(figsize=(10,6))
    plt.plot(time, voltage)

    plt.suptitle("График зависимости напряжения на входе АЦП от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.axis((0, np.max(time), 0, max_voltage))
    plt.grid(visible=True)
    plt.show()


def plot_sampling_period_hist(time):
    
    plt.figure(figsize=(10,6))

    intervals = []
    last = 0

    for sampling_period in time:
        intervals.append(sampling_period - last)
        last = sampling_period
    plt.hist(intervals)

    
    plt.suptitle("Распределение периодов дискретизации измерений по времени на одно измерение")
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений, В")
    plt.xlim(0, 0.006)
    plt.grid(visible=True)
    plt.show()
    print(np.mean(intervals))