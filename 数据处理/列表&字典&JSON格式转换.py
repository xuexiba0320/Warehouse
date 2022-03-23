import json

# list转换成json：
str_json = json.dumps(list, ensure_ascii=False, indent=2)
# json转换成list：
list = json.loads(str_json)

# list 转成Json格式数据
import json
import numpy as np

lst = []
keys = [str(x) for x in np.arange(len(lst))]
list_json = dict(zip(keys, lst))
str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string

# python格式化保存list到json文件
# 一
json_file_path = '/home/zxq/PycharmProjects/data/ciga_call/result.json'
json_file = open(json_file_path, mode='w')

save_json_content = []
img_name_list = []
for img_name in img_name_list:
    result_json = {
        "image_name": img_name,
        "category": 1,
        "score": 0.99074}
    save_json_content.append(result_json)
json.dump(save_json_content, json_file, indent=4)


# json.dump(save_json_content, json_file, ensure_ascii=False, indent=4) # 保存中文

# 二
def main():
    mydict = {
        'name': 'Catherine',
        'age': 30,
        'qq': 123456,
        'friends': ['Mike', 'Joey'],
        'cars': [
            {'brand': 'BYD', 'max_speed': 180},
            {'brand': 'JEEP', 'max_speed': 280},
            {'brand': 'Benz', 'max_speed': 320}
        ]
    }
    try:
        with open('data.json', 'w', encoding='utf-8') as fs:
            json.dump(mydict, fs)
    except IOError as e:
        print(e)
    print('保存数据完成!')


if __name__ == '__main__':
    main()

# Python将list元素转存为CSV文件
import pandas as pd

list = [[1, 2, 3], [4, 5, 6], [7, 9, 9]]
# 下面这行代码运行报错
# list.to_csv('e:/testcsv.csv',encoding='utf-8')
name = ['one', 'two', 'three']
test = pd.DataFrame(columns=name, data=list)  # 数据有三列，列名分别为one,two,three
print(test)
test.to_csv('e:/testcsv.csv', encoding='gbk')
