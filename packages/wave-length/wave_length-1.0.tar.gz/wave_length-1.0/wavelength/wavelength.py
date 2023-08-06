import cv2
import numpy as np
import pandas as pd


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


def calculate_XY(file, Lambdas, function_R, function_G, function_B, show_spectrum=False, start=380, end=780, readline=9):
    # file = r"C:\mLED_project\04-算法开发\20211204-主波长计算\测试用 光谱数据\20211208-测试/GLED-1.txt"      # 360 —— 800
    with open(file, 'r') as p:
        datas = p.read()
    datas = datas.split("\n")[readline:-2]

    new_datas = []
    lambdas = []
    for dt in datas:
        lambda_dt = float(dt.split(";")[0].replace(" ", ""))
        value = float(dt.split(";")[1].replace(" ", ""))
        if lambda_dt >= start and (lambda_dt <= end):
            new_datas.append(value)
            lambdas.append(lambda_dt)

    if show_spectrum:
        import matplotlib.pyplot as plt
        plt.figure(2)
        plt.title("your spectrum ")
        plt.plot(np.array(lambdas), np.array(new_datas))

    print("your data's length: ", len(new_datas))
    # 计算 380 —— 780
    Lambdas = get_function(Lambdas)  # 将波长段细化至0.1
    function_R = get_function(function_R)
    function_G = get_function(function_G)
    function_B = get_function(function_B)

    X = 0
    Y = 0
    Z = 0
    for i in range(len(new_datas)):
        lmd = lambdas[i]
        dis_ = [np.abs(a - lmd) for a in Lambdas]
        min_dis_index = np.argmin(dis_)

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
    return xx, yy


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
    # 粗定位
    x_index = np.argwhere(np.abs(np.array(Lambda_x) - x) <= 0.001)[:, 0]    # X 坐标相近的点
    y_index = np.argwhere(np.abs(np.array(Lambda_y) - y) <= 0.001)[:, 0]    # Y 坐标相近的点
    """
        由于lambda、lambda_x和lambda_y是同步的，所以取x_index与y_index相近的位置进行拟合即可
    """
    # 1、找两个数组中相同的元素
    indexs = list(x_index.copy())
    for y in y_index:
        indexs.append(y)
    indexs = sorted(indexs)
    similar = []
    counts_dict = {item: indexs.count(item) for item in indexs}
    for item in counts_dict.items():
        if item[1] > 1:
            similar.append(item[0])

    # 存在重复元素，取多个重复元素的均值
    if len(similar) > 0:
        result_lambda = []
        for idx in similar:
            result_lambda.append(Lambda[idx])
        return np.mean(np.array(result_lambda))
    # 不存在重复的元素，取最相近的两个元素的均值
    else:
        min_dis = 1000
        min_dis_indexs = []
        for i in x_index:
            for j in y_index:
                if np.abs(i - j) <= min_dis:
                    min_dis_indexs = [i, j]
        result_lambda = [Lambda[min_dis_indexs[0]], Lambda[min_dis_indexs[1]]]
        return np.mean(np.array(result_lambda))


def work(file, draw=True, start=380, end=780, read_line=9):
    """
    :param file: 保存你自己光谱数据的文件。  .txt文件
    :param draw: 是否展示光谱绘制图
    :param start: 计算波谱的起点——默认为 380nm。自定义值必须在区间 [380, 780]中
    :param end: 计算波谱的终点——默认为780nm。 自定义值必须在区间 [380, 780]中
    :return:
    """
    CIE = pd.read_excel("./2021-12-06_114911.xlsx")
    function = np.array(CIE)[:, -3:]
    lambdas = np.array(CIE)[:, 0]
    x, y = calculate_XY(file, lambdas, function[:, 0], function[:, 1], function[:, 2], draw, start, end, read_line)

    CIE = np.array(pd.read_csv("./cc2012xyz2_fine_5dp.csv"))[:, :3]
    # CIE: [[波长1, x1, y1], [波长2, x1, y1], ...]
    Lambda = CIE[:, 0]
    Lambda_x = CIE[:, 1]
    Lambda_y = CIE[:, 2]

    result_lambda = calculate(x, y, Lambda, Lambda_x, Lambda_y)
    print("wave length: ", result_lambda)

    if draw:
        import matplotlib.pyplot as plt
        plt.figure(1)
        plt.title("CIE1931")
        plt.plot(Lambda, Lambda_x, 'blue')
        plt.plot(Lambda, Lambda_y, 'red')
        plt.legend(["x", "y"])
        plt.show()

    return x, y, result_lambda, Lambda, Lambda_x, Lambda_y


if __name__ == '__main__':
    work(r"C:\mLED_project\04-算法开发\20211204-主波长计算\测试用 光谱数据\20211208-测试/GLED-1.txt", start=420)
