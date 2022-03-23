import re
print("""
    *******************************
             企业编码管理系统
    *******************************
        1、生成6位
        2、生成9位
        3、生成25位
        4、半智能
        5、退出系统
""")

option_str = input("请通过数字键或者方向键选择功能:")
option = re.sub(r"\D", "", option_str)[0]
# print(option)

if int(option) == 1:
    print(1)
if int(option) == 2:
    print(2)
if int(option) == 3:
    print('yuyruirtuey')
if int(option) == 4:
    print(4)
if int(option) == 5:
    print(5)