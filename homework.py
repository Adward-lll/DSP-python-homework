import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import tkinter as tk
from tkinter import messagebox, ttk
import sympy as sp
# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 极零图
def plot_pz(system):
    plt.figure(figsize=(10, 6))
    plt.title("极零图")
    zeros, poles, _ = signal.tf2zpk(system.num, system.den)
    plt.scatter(np.real(zeros), np.imag(zeros), marker='o', label='零点')
    plt.scatter(np.real(poles), np.imag(poles), marker='x', label='极点')
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.xlabel('实部')
    plt.ylabel('虚部')
    plt.legend()
    plt.grid(True)
    plt.show()

# 幅频特性
def plot_bode(system):
    w, mag, phase = signal.bode(system)
    plt.figure(figsize=(10, 6))
    plt.semilogx(w, mag, label='幅度')
    plt.title("幅频特性曲线")
    plt.xlabel('频率 (rad/s)')
    plt.ylabel('增益 (dB)')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.semilogx(w, phase, label='相位')
    plt.title("相频特性曲线")
    plt.xlabel('频率 (rad/s)')
    plt.ylabel('相位 (degrees)')
    plt.legend()
    plt.grid(True)
    plt.show()

# 单位冲激响应
def plot_impulse_response(t, y):
    plt.figure(figsize=(10, 6))
    plt.title("单位冲激响应")
    plt.plot(t, y)
    plt.xlabel('时间 (s)')
    plt.ylabel('响应')
    plt.grid(True)
    plt.show()

# 设计并应用滤波器
def design_and_apply_filter(cutoff_freq, fs, filter_type, t, y):
    if filter_type == 'lowpass':
        b, a = signal.butter(5, cutoff_freq / (0.5 * fs), btype='low')
    elif filter_type == 'highpass':
        b, a = signal.butter(5, cutoff_freq / (0.5 * fs), btype='high')
    else:
        raise ValueError("Unsupported filter type. Choose 'lowpass' or 'highpass'.")

    filtered_impulse = signal.filtfilt(b, a, y)

    plt.figure(figsize=(10, 6))
    plt.title(f"{filter_type.capitalize()} Filtered Impulse Response")
    plt.plot(t, filtered_impulse, label=f'{filter_type.capitalize()} Filtered', linestyle='--')
    plt.plot(t, y, label='Original', linestyle='-')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

# 定义主函数
def calculate_system():

    try:
        s = sp.symbols('s')
        # 用户输入分子系数
        print("输入分子系数（b1, b0, ...），请按顺序输入，以'0'结束呀：")
        b_coeffs = []
        while True:
            input_str = input("> ")
            if input_str == '0':
                break
            else:
                try:
                    # 尝试将输入转换为浮点数
                    b_coeffs.append(float(input_str))
                except ValueError:
                    # 如果转换失败，打印错误消息并继续循环
                    print("输入无效，请输入一个数字。")

        # 用户输入分母系数
        print("请输入分母系数（a2, a1, a0, ...），请按顺序输入，以'0'结束呀：")
        a_coeffs = []
        while True:
            input_str = input("> ")
            if input_str == '0':
                break
            else:
                try:
                    # 尝试将输入转换为浮点数
                    a_coeffs.append(float(input_str))
                except ValueError:
                    # 如果转换失败，打印错误消息并继续循环
                    print("输入无效，请输入一个数字。")

        # 构建分子和分母多项式
        numerator = sum([b * s ** i for i, b in enumerate(b_coeffs)])
        denominator = sum([a * s ** i for i, a in enumerate(a_coeffs)])

        # 定义系统函数 H(s)
        H_s = sp.simplify(numerator / denominator)

        # 输出系统函数 H(s)
        print("系统函数 H(s) 是:")
        print(H_s)

        a = list(map(float, entry_a.get().split(',')))
        b = list(map(float, entry_b.get().split(',')))
        cutoff_freq = float(entry_cutoff.get())
        fs = int(float(entry_fs.get()))
        filter_type = filter_type_var.get()

        system = signal.TransferFunction(b, a)

        plot_pz(system)
        plot_bode(system)
        time = np.linspace(0, 10, 500)
        t, y = signal.impulse(system, T=time)
        plot_impulse_response(t, y)
        design_and_apply_filter(cutoff_freq, fs, filter_type, t, y)

    except ValueError as e:
        messagebox.showerror("输入错误", str(e))

# 创建GUI界面
root = tk.Tk()
root.title("数字信号处理-系统分析与设计和滤波器设计-sbh")

label_a = tk.Label(root, text="请输入数组a (系数列表，逗号分隔):")
label_a.pack(pady=5)
entry_a = tk.Entry(root, width=40)
entry_a.pack(pady=5)

label_b = tk.Label(root, text="请输入数组b (系数列表，逗号分隔):")
label_b.pack(pady=5)
entry_b = tk.Entry(root, width=40)
entry_b.pack(pady=5)

label_cutoff = tk.Label(root, text="截止频率 (Hz):")
label_cutoff.pack(pady=5)
entry_cutoff = tk.Entry(root)
entry_cutoff.pack(pady=5)

label_fs = tk.Label(root, text="采样频率 (Hz):")
label_fs.pack(pady=5)
entry_fs = tk.Entry(root)
entry_fs.pack(pady=5)

label_filter_type = tk.Label(root, text="请选择滤波器类型:")
label_filter_type.pack(pady=5)
filter_type_var = tk.StringVar(value='lowpass')
ttk.Combobox(root, textvariable=filter_type_var, values=['lowpass', 'highpass'], state="readonly").pack(pady=5)

button_calculate = tk.Button(root, text="计算并绘制对用图像", command=calculate_system)
button_calculate.pack(pady=20)

root.mainloop()