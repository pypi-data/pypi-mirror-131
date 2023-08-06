
import numpy as np


def calculate_conner(labels, label_positions, pt_head, pt_center):
    if pt_head[0] - pt_center[0] != 0:
        k = (pt_head[1] - pt_center[1]) / (pt_head[0] - pt_center[0])
    else:
        k = 1000

    def line(x):
        return k * x + pt_head[1] - k * pt_head[0]

    def dis(pt0, pt1, pt_h, pt_c):
        # 由center向head延申一条直线，如果这条直线与pt0-pt1相交，返回True。否则返回False
        # 简化为求直线pt0-pt1与直线center-head的交点，如果该交点在center——>head方向上，返回True，否则返回False
        k_0_1 = (pt0[1] - pt1[1]) / (pt0[0] - pt1[0])
        b_0_1 = pt1[1] - k_0_1 * pt1[0]
        k_c_h = k
        b_c_h = pt_h[1] - k_c_h * pt_h[0]
        corner_x = (b_c_h - b_0_1) / (k_0_1 - k_c_h)
        corner_y = k_0_1 * corner_x + b_0_1
        vector_corner_center = (corner_y - pt_c[1], corner_x - pt_c[0])
        vector_head_center = (pt_h[1] - pt_c[1], pt_h[0] - pt_c[0])
        if vector_corner_center[0] * vector_head_center[0] + vector_corner_center[1] * vector_head_center[1] > 0:
            return True
        else:
            return False

    start_label = None
    end_label = None
    start_value = 0
    end_value = 0
    for i, pt in enumerate(label_positions):
        if i == len(label_positions) - 1:
            break
        # print(labels[i], labels[i + 1])
        # print((pt[1] - line(pt[0])) * (label_positions[i + 1][1] - line(label_positions[i + 1][0])))
        # print(dis(pt, label_positions[i + 1], pt_head, pt_center))
        if (pt[1] - line(pt[0])) * (label_positions[i + 1][1] - line(label_positions[i + 1][0])) <= 0:
            if dis(pt, label_positions[i + 1], pt_head, pt_center):
                # 刻度从左往右分布
                start_label = pt    # 指针左边的点
                end_label = label_positions[i + 1]     # 指针右边的点
                start_value = labels[i]
                end_value = labels[i + 1]
                print("start and end position: ", start_label, end_label)
                break

    if start_label != None and end_label != None:    # 能够找到指针左右分布的坐标
        length_s_t = np.sqrt((pt_head[0] - start_label[0]) ** 2 + (pt_head[1] - start_label[1]) ** 2)
        length_e_t = np.sqrt((pt_head[0] - end_label[0]) ** 2 + (pt_head[1] - end_label[1]) ** 2)
        length_s_c = np.sqrt((pt_center[0] - start_label[0]) ** 2 + (pt_center[1] - start_label[1]) ** 2)
        length_e_c = np.sqrt((pt_center[0] - end_label[0]) ** 2 + (pt_center[1] - end_label[1]) ** 2)
        length_c_t = np.sqrt((pt_center[0] - pt_head[0]) ** 2 + (pt_center[1] - pt_head[1]) ** 2)
        length_s_e = np.sqrt((start_label[0] - end_label[0]) ** 2 + (start_label[1] - end_label[1]) ** 2)

        cos_s_c_t = (length_s_c ** 2 + length_c_t ** 2 - length_s_t ** 2) / (2 * length_s_c * length_c_t)
        cos_e_c_t = (length_e_c ** 2 + length_c_t ** 2 - length_e_t ** 2) / (2 * length_e_c * length_c_t)
        cos_s_c_e = (length_s_c ** 2 + length_e_c ** 2 - length_s_e ** 2) / (2 * length_s_c * length_e_c)

        s_c_t = np.arccos(cos_s_c_t)
        e_c_t = np.arccos(cos_e_c_t)
        s_c_e = np.arccos(cos_s_c_e)
        print("left-right-angle: ", s_c_t, e_c_t, s_c_e)

        if abs(s_c_e - s_c_t - e_c_t) <= 0.1:
            # 计算读数
            result = (s_c_t / s_c_e) * (end_value - start_value) + start_value
            print("normal top————left: {}, right: {}, {}".format(start_value, end_value, result))

            return result, start_label, end_label
        else:
            result = (s_c_t / (s_c_t + e_c_t)) * (end_value - start_value) + start_value
            print("normal down————left: {}, right: {}, {}".format(start_value, end_value, result))

            return result, start_label, end_label

    else:     # 不能找到指针左右分布的坐标，则利用单坐标计算
        distances = [np.sqrt((obj[0] - pt_head[0]) ** 2 + (obj[1] - pt_head[1]) ** 2) for obj in label_positions]
        min_dis = np.min(distances)
        index = np.argwhere(np.array(distances) == min_dis)[0][0]
        min_dis_poistion = label_positions[index]
        min_dis_value = labels[index]
        print("min dis value: ", min_dis_value)

        if min_dis_value == labels[0]:  # 指针在坐标，靠近实际刻度的最小值
            start_label = min_dis_poistion
            end_label = label_positions[index + 1]

            start_label_value = min_dis_value
            end_label_value = labels[index + 1]

            length_s_t = np.sqrt((pt_head[0] - start_label[0]) ** 2 + (pt_head[1] - start_label[1]) ** 2)
            # length_e_t = np.sqrt((pt_head[0] - end_label[0]) ** 2 + (pt_head[1] - end_label[1]) ** 2)
            length_s_c = np.sqrt((pt_center[0] - start_label[0]) ** 2 + (pt_center[1] - start_label[1]) ** 2)
            length_e_c = np.sqrt((pt_center[0] - end_label[0]) ** 2 + (pt_center[1] - end_label[1]) ** 2)
            length_c_t = np.sqrt((pt_center[0] - pt_head[0]) ** 2 + (pt_center[1] - pt_head[1]) ** 2)
            length_s_e = np.sqrt((start_label[0] - end_label[0]) ** 2 + (start_label[1] - end_label[1]) ** 2)

            cos_s_c_t = (length_s_c ** 2 + length_c_t ** 2 - length_s_t ** 2) / (2 * length_s_c * length_c_t)
            # cos_e_c_t = (length_e_c ** 2 + length_c_t ** 2 - length_e_t ** 2) / (2 * length_e_c * length_c_t)
            cos_s_c_e = (length_s_c ** 2 + length_e_c ** 2 - length_s_e ** 2) / (2 * length_s_c * length_e_c)

            s_c_t = np.arccos(cos_s_c_t)
            # e_c_t = np.arccos(cos_e_c_t)
            s_c_e = np.arccos(cos_s_c_e)

            result = start_label_value - (s_c_t / s_c_e) * (end_label_value - start_label_value)

            print("min left ————left: {}, right: {}, {}".format(start_label_value, end_label_value, result))

            if result >= 390:
                return result, start_label, end_label
            else:
                return 0, start_label, end_label

        else:   # 指针在右边，靠近实际刻度的最大值
            start_label = label_positions[index - 1]
            end_label = min_dis_poistion

            start_label_value = labels[index - 1]
            end_label_value = min_dis_value

            # length_s_t = np.sqrt((pt_head[0] - start_label[0]) ** 2 + (pt_head[1] - start_label[1]) ** 2)
            length_e_t = np.sqrt((pt_head[0] - end_label[0]) ** 2 + (pt_head[1] - end_label[1]) ** 2)
            length_s_c = np.sqrt((pt_center[0] - start_label[0]) ** 2 + (pt_center[1] - start_label[1]) ** 2)
            length_e_c = np.sqrt((pt_center[0] - end_label[0]) ** 2 + (pt_center[1] - end_label[1]) ** 2)
            length_c_t = np.sqrt((pt_center[0] - pt_head[0]) ** 2 + (pt_center[1] - pt_head[1]) ** 2)
            length_s_e = np.sqrt((start_label[0] - end_label[0]) ** 2 + (start_label[1] - end_label[1]) ** 2)

            # cos_s_c_t = (length_s_c ** 2 + length_c_t ** 2 - length_s_t ** 2) / (2 * length_s_c * length_c_t)
            cos_e_c_t = (length_e_c ** 2 + length_c_t ** 2 - length_e_t ** 2) / (2 * length_e_c * length_c_t)
            cos_s_c_e = (length_s_c ** 2 + length_e_c ** 2 - length_s_e ** 2) / (2 * length_s_c * length_e_c)

            # s_c_t = np.arccos(cos_s_c_t)
            e_c_t = np.arccos(cos_e_c_t)
            s_c_e = np.arccos(cos_s_c_e)

            result = end_label_value + (e_c_t / s_c_e) * (end_label_value - start_label_value)

            print("max right ————left: {}, right: {}, {}".format(start_label_value, end_label_value, result))

            return result, start_label, end_label


def work(number_objects, pt_head, pt_center):
    """
    Args:
        number_objects: 长度必须大于等于2
        pt_head:
        pt_center:

    Returns:

    """
    labels = [float(obj[0]) for obj in number_objects]
    labels_positions = [[(obj[2][0] + obj[2][2]) / 2, (obj[2][1] + obj[2][3]) / 2] for obj in number_objects]
    print("labels: ", labels)
    print("positions", labels_positions)
    result, start_label, end_label = calculate_conner(labels, labels_positions, pt_head, pt_center)

    return result, start_label, end_label
