import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter

# 时长为 1s
t = 1
# 采样率为 60Hz
f_s = 60
t_split = np.arange(0, t * f_s)

# 1Hz 与 25Hz 叠加的正弦信号
x_1hz = t_split * 1 * np.pi * 2 / f_s
x_25hz = t_split * 25 * np.pi * 2 / f_s
signal_sin_1hz = np.sin(x_1hz)
signal_sin_25hz = np.sin(x_25hz)
signal_sin = signal_sin_1hz + 0.25 * signal_sin_25hz

# 通带边缘频率为 10Hz
p_f = 10
# 阻带边缘频率为 22Hz
r_f = 22
# 阻带衰减为 44dB，窗内项数为 17 的汉宁窗函数
N = 17


# 回绕函数
def revolve(x, n):
    y = np.zeros(n)
    for i, v in enumerate(x):
        y[i % n] += v
    return y


# TODO: 补全这部分代码
# 构建低通滤波器
# 函数需要返回滤波后的信号
def filter_fir(input_signal):
    f_c = (p_f + r_f) / 2
    omega_c = 2 * np.pi * f_c / f_s

    def h(n):
        return omega_c / np.pi if n == 0 else np.sin(n * omega_c) / (n * np.pi)

    def w(n):
        return 0.5 + 0.5 * np.cos(2 * np.pi * n / (N - 1))

    h_prime = [h(n - 8) * w(n - 8) for n in range(N)]
    return revolve(np.convolve(h_prime, input_signal, mode='full'), t * f_s)


# TODO: 首先正向对信号滤波(此时输出信号有一定相移)
# 将输出信号反向，再次用该滤波器进行滤波
# 再将输出信号反向
# 函数需要返回零相位滤波后的信号
def filter_zero_phase(input_signal):
    forward_signal = filter_fir(input_signal)
    backward_signal = filter_fir(forward_signal[::-1])
    return backward_signal[::-1]


if __name__ == "__main__":
    delay_filtered_signal = filter_fir(signal_sin)
    zero_phase_filtered_signal = filter_zero_phase(signal_sin)

    plt.plot(t_split, signal_sin, label='origin')
    plt.plot(t_split, delay_filtered_signal, label='fir')
    plt.plot(t_split, zero_phase_filtered_signal, label='zero phase')

    plt.show()
