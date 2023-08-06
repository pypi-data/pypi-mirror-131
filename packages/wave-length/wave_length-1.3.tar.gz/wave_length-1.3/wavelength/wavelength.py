import yaml
import numpy as np
import pandas as pd
from .calculate import work as CAV


def get_function(data_array, size=50):
    # 380 —— 780
    new_data_array = [data_array[0]]
    for i, data in enumerate(data_array):
        if i + 1 > len(data_array) - 1:
            break

        last_value = new_data_array[-1]
        dis = data_array[i + 1] - data
        per_dis = dis / size
        for j in range(1, size + 1):
            new_data_array.append(last_value + j * per_dis)
    return new_data_array


def subdivide_CIE(X, Y, lam):
    new_X = [X[0]]
    new_y = [Y[0]]
    new_lam = [lam[0]]
    for i, xx in enumerate(X):
        if i + 1 > len(X) - 1:
            break
        last_x = new_X[-1]
        last_y = new_y[-1]
        last_lam = new_lam[-1]
        dis_x = X[i + 1] - xx
        dis_y = Y[i + 1] - Y[i]
        dis_lam = lam[i + 1] - lam[i]
        print(xx, last_x)
        for j in range(1, 51):
            new_X.append(last_x + j * (dis_x / 50))
            new_y.append(last_y + j * (dis_y / 50))
            new_lam.append(last_lam + j * (dis_lam / 50))
    return new_X, new_y, new_lam


def calculate_XY(file, Lambdas, function_R, function_G, function_B, start=380, end=780, draw=True, statr_line=8):
    with open(file, 'r') as p:
        datas = p.read()
    datas = datas.split("\n")[statr_line:-2]

    new_datas = []
    lambdas = []
    for dt in datas:
        lambda_dt = float(dt.split(";")[0].replace(" ", ""))
        value = float(dt.split(";")[1].replace(" ", ""))
        if lambda_dt >= start and (lambda_dt <= end):
            new_datas.append(value)
            lambdas.append(lambda_dt)
    max_spectrum_idx = np.argmax(np.array(new_datas))
    max_spectrum = lambdas[max_spectrum_idx]
    print("max spectrum: ", max_spectrum)

    if draw:
        import matplotlib.pyplot as plt
        plt.figure(2)
        plt.title("your spectrum ")
        plt.plot(np.array(lambdas), np.array(new_datas))

    print("lambda's length: ", len(new_datas))
    # 计算 380 —— 780
    Lambdas = get_function(Lambdas)  # 将波长段细化至0.1
    function_R = get_function(function_R)
    function_G = get_function(function_G)
    function_B = get_function(function_B)

    if draw:
        import matplotlib.pyplot as plt
        plt.figure(4)
        plt.plot(Lambdas, function_R, 'red')
        plt.plot(Lambdas, function_G, 'green')
        plt.plot(Lambdas, function_B, 'blue')

    X = 0
    Y = 0
    Z = 0
    for i in range(len(new_datas)):
        lmd = lambdas[i]
        dis_ = [np.abs(a - lmd) for a in Lambdas]
        min_dis_index = np.argmin(dis_)

        if min_dis_index + 1 == len(Lambdas):
            break

        # print(lmd, Lambdas[min_dis_index])
        if lmd >= Lambdas[min_dis_index]:
            X += (function_R[min_dis_index] + ((function_R[min_dis_index + 1] - function_R[min_dis_index]) / 1000)
                  * (lmd - Lambdas[min_dis_index]) * 1000) * new_datas[i]
            Y += (function_G[min_dis_index] + ((function_G[min_dis_index + 1] - function_G[min_dis_index]) / 1000)
                  * (lmd - Lambdas[min_dis_index]) * 1000) * new_datas[i]
            Z += (function_B[min_dis_index] + ((function_B[min_dis_index + 1] - function_B[min_dis_index]) / 1000)
                  * (lmd - Lambdas[min_dis_index]) * 1000) * new_datas[i]
        else:
            X += (function_R[min_dis_index] - ((function_R[min_dis_index] - function_R[min_dis_index - 1]) / 1000)
                  * (lmd - Lambdas[min_dis_index]) * 1000) * new_datas[i]
            Y += (function_G[min_dis_index] - ((function_G[min_dis_index] - function_G[min_dis_index - 1]) / 1000)
                  * (lmd - Lambdas[min_dis_index]) * 1000) * new_datas[i]
            Z += (function_B[min_dis_index] - ((function_B[min_dis_index] - function_B[min_dis_index - 1]) / 1000)
                  * (lmd - Lambdas[min_dis_index]) * 1000) * new_datas[i]

    xx = X / (X + Y + Z)
    yy = Y / (X + Y + Z)
    print('x: ', xx, ' y: ', yy)
    return xx, yy, max_spectrum


def calculate(x, y, Lambda, Lambda_x, Lambda_y):
    """
    计算主波长
    :param x:
    :param y:
    :param Lambda: 波长
    :param Lambda_x:
    :param Lambda_y:
    :return:
    """
    objects = []
    for i, lam in enumerate(Lambda):
        objects.append([lam, 0, [Lambda_x[i], Lambda_y[i], Lambda_x[i], Lambda_y[i]]])

    result, start_label, end_label = CAV(objects, [x, y], [0.333, 0.333])
    print('wave length: ', result)

    return result, start_label, end_label


def work(file, start=390, end=830, draw=True, statr_line=8):
    # 色度匹配图 0.1nm
    CIE = np.array(pd.read_csv("./cc2012xyz2_fine_5dp.csv"))[:, :3]  # 390 —— 830  0.1
    # CIE: [[波长1, x1, y1], [波长2, x1, y1], ...]
    Lambda = CIE[:, 0]
    Lambda_x = CIE[:, 1]
    Lambda_y = CIE[:, 2]

    # 匹配函数，间距5nm
    CIE = pd.read_excel("./2021-12-06_114911.xlsx")  # 380 —— 780 5
    function = np.array(CIE)[:, -3:]
    lambdas = np.array(CIE)[:, 0]

    x, y, max_spectrum = calculate_XY(file, lambdas, function[:, 0], function[:, 1], function[:, 2], start,
                                      end, draw, statr_line=statr_line)

    result_lambda, start_label, end_label = calculate(x, y, Lambda, Lambda_x, Lambda_y)

    print("wave length: ", result_lambda, "spectrum / peak: ", result_lambda / max_spectrum)

    if draw:
        import matplotlib.pyplot as plt
        labels = [400, 450, 475, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 625, 800]
        X = []
        Y = []
        for lb in labels:
            idx = np.argwhere(np.array(Lambda) == lb)[0][0]
            X.append(Lambda_x[idx])
            Y.append(Lambda_y[idx])

        plt.figure(3)
        plt.title("CIE1931")
        plt.legend(["x", "y"])
        plt.plot(Lambda_x, Lambda_y, 'red')
        plt.scatter(0.333, 0.333, edgecolors='black')
        plt.scatter(0.35, 0.333, s=500, marker='$white$')

        plt.scatter(x, y, edgecolors='black')
        plt.scatter(x + 0.025, y, s=500, marker='$target$')

        print(start_label)
        plt.plot(np.array([x, 0.3333, (start_label[0] + end_label[0]) / 2]),
                 np.array([y, 0.3333, (start_label[1] + end_label[1]) / 2]), 'blue')
        for i in range(len(X)):
            plt.scatter(X[i], Y[i])
            plt.scatter(X[i] - 0.05, Y[i], s=500, marker='${}$'.format(labels[i]))
        plt.show()

    return x, y, result_lambda, Lambda, Lambda_x, Lambda_y


if __name__ == '__main__':
    work(file=r"C:\mLED_project\04-算法开发\20211204-主波长计算\测试用 光谱数据\20211208-测试/BLED-1_2110229M1.txt", start=380)
