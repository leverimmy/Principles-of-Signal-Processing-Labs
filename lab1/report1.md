# 实验一：傅里叶级数的可视化 - 实验报告

熊泽恩 计24 2022011223

## 任务一：可视化方波信号

方波信号为
$$
f(t) = 0.5\;\textrm{sgn}(\sin t) + 0.5.
$$
其傅里叶级数展开为 $g(t) = a_0 + \sum_{i = 1}^{+\infty}(a_n\cos nt + b_n \sin nt)$，其中
$$
a_0 = \frac{1}{2\pi}\int_{0}^{2\pi}f(t)\text{d}t = \frac{1}{2\pi}\int_{0}^{\pi}1\text{d}t = \frac{1}{2}.
$$
当 $n \neq 0$ 时，
$$
a_n = \frac{1}{\pi}\int_{0}^{2\pi}f(t)\cos nt \text{d}t = \frac{1}{\pi}\int_{0}^{\pi}\cos nt \text{d}t = \frac{1}{n\pi}\left(\sin nt\right)\bigg\vert_{0}^{\pi} = 0.
$$
接下来考虑 $b_n$：
$$
b_n = \frac{1}{\pi}\int_{0}^{2\pi}f(t)\sin nt \text{d}t = \frac{1}{\pi}\int_{0}^{\pi}\sin nt \text{d}t = \frac{1}{n\pi}\left(-\cos nt\right)\bigg\vert_{0}^{\pi} = \frac{1 - \cos n\pi}{n\pi},
$$
当 $n$ 为奇数时，$b_n = \frac{2}{n\pi}$；当 $n$ 为偶数时，$b_n = 0$。

此时我们显式地得到了 $a_0, a_n, b_n$ 的表达式，编写代码如下：

```python
# TODO: 2. Please implement the function that calculates the Nth fourier coefficient
# Note that n starts from 0
# For n = 0, return a0; n = 1, return b1; n = 2, return a1; n = 3, return b2; n = 4, return a2 ...
# n = 2 * m - 1(m >= 1), return bm; n = 2 * m(m >= 1), return am. 
def fourier_coefficient(n):
    if n == 0:
        return 0.5
    elif n % 2 == 0:
        return 0
    elif n % 4 == 1:
        return 2 / (n * np.pi)
    else:
        return 0


# TODO: 3. implement the signal function
def square_wave(t):
    return 0.5 * np.sign(np.sin(t)) + 0.5
```

然后就能够得到 `square_2.mp4`、`square_4.mp4`、`square_8.mp4` 等视频文件。

## 任务二：可视化半圆波信号（选做）

半圆波信号为
$$
f(t) = \begin{cases}
		\sqrt{\pi^2 - (t - \pi)^2}, & t \in [0, 2\pi), \\
		f(t + 2\pi), & t < 0, \\
		f(t - 2\pi), & t \ge 2\pi.
		\end{cases}
$$
代码如下：

```python
# TODO: optional. implement the semi circle wave function
def semi_circle_wave(t):
    t %= 2 * np.pi
    return np.sqrt(np.pi ** 2 - (t - np.pi) ** 2)
```

对于傅里叶系数而言，由定义：
$$
\begin{align*}
a_0 & = \frac{1}{2\pi}\int_{0}^{2\pi}f(t)\text{d}t, \\
a_n & = \frac{1}{\pi}\int_{0}^{2\pi}f(t)\cos nt\text{d}t, \\
b_n & = \frac{1}{\pi}\int_{0}^{2\pi}f(t)\sin nt\text{d}t.
\end{align*}
$$
使用 `scipy` 中的 `integrate` 包，可以方便地进行定积分：

```python
def fourier_coefficient(n):
    def fa(x):
        return semi_circle_wave(x) * np.cos(n / 2 * x)

    def fb(x):
        return semi_circle_wave(x) * np.sin((n + 1) / 2 * x)

    if n == 0:
        return integrate.quad(fa, 0, 2 * np.pi)[0] / (2 * np.pi)
    elif n % 2 == 0:
        return integrate.quad(fa, 0, 2 * np.pi)[0] / np.pi
    else:
        return integrate.quad(fb, 0, 2 * np.pi)[0] / np.pi
```

然后就能够得到 `semi_circle_2.mp4`、`semi_circle_4.mp4`、`semi_circle_8.mp4` 等视频文件。
