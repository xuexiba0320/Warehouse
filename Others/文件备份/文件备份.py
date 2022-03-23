# 输入需要备份的文件名称
old_name = input('请输入需要备份的文件名称：')  # word.txt
# 进行文件名称的逗号索引定位
index = old_name.index('.')
print(index)
# 名称切片
print(old_name[:index])  # word
print(old_name[index:])  # .text
# 构建备份文件名称
new_name = old_name[:index] + '[备份文件]' + old_name[index:]
print(new_name)

# 文件数据备份
"""
打开原文件,读取数据
打开备份文件
将原文件的数据存入备份文件
关闭原文件、备份文件
"""
with open('word.txt', 'rb')as f_old:
    # 读取数据
    data = f_old.read()
    with open(new_name, 'wb')as f_new:
        # 将原文件读取出数据写入备份文件中
        data_new = f_new.write(data)
        print(data_new)
