from PIL import Image
import numpy as np
import collections


def find_border(path, threshold):
    image = Image.open(path)
    image = image.convert('L')
    # image.show()
    # image.save('gray.png')
    ary = np.array(image)
    target_list = []
    y_dict = {}
    temp = []
    for c in range(len(ary[0]) - 1):
        for r in range(len(ary)):
            value = int(ary[r][c]) - int(ary[r][c + 1])
            if value > threshold:
                target_list.append(c)

                temp.append(r)
                y_dict[c] = temp[:]

        temp.clear()

    result = collections.Counter(target_list).most_common(3)

    refer1, refer2, refer3 = _get_refers(result, y_dict)

    result2 = (refer1, refer2, refer3)
    result3 = _judge_x_pos(result2)

    return result3


def _get_refers(result, y_dict):
    """输出3处坐标的(横坐标,最小y值,最大y值)"""
    refer = (result[0][0], result[1][0], result[2][0])
    refer1 = (refer[0], min(y_dict[refer[0]]), max(y_dict[refer[0]]))
    # refer1 =  (146, 24, 76)

    refer2 = (refer[1], min(y_dict[refer[1]]), max(y_dict[refer[1]]))
    refer3 = (refer[2], min(y_dict[refer[2]]), max(y_dict[refer[2]]))
    return refer1, refer2, refer3


def _judge_deference(tup1, tup2):
    """判断两个x坐标y值相差范围,value越小,证明两者y值范围越相似"""
    value = abs(tup1[1] - tup2[1]) + abs(tup1[2] - tup2[2])
    return value


def _judge_x_pos(tup):
    """三选一,输出y值范围最相似的坐标及y范围相差值"""
    t1 = tup[0][0], tup[1][0], _judge_deference(tup[0], tup[1])
    t2 = tup[1][0], tup[2][0], _judge_deference(tup[1], tup[2])
    t3 = tup[0][0], tup[2][0], _judge_deference(tup[0], tup[2])
    new_tup = (t1, t2, t3)

    value = min(t1[2], t2[2], t3[2])
    for item in new_tup:
        if item[2] == value:
            return item


if __name__ == '__main__':
    res = find_border("2.png", 70)
    print(res)
    ...
