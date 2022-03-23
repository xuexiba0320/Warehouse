word = '编号    姓名      性别    年级 学校     奖项'
list = word.split()
print(list)
listnew = [i for i in list if i != '']
print(listnew)
new = '--'.join(listnew)
print(new)
new = '**'.join(list)
print(new)

nba = '哈登: 31.6  伦纳德: 31.2   娇子: 28.6'
nbanew = nba.split()
print(nbanew)

emty = ['', 'huojiang', '', 'hureren', 'yongshi']
data = [i for i in emty if i != '']
print(data)

# 删除小写字母
import re
data = 'ABjgKJHGSggrkjHKJFGJSDFLGa'
res = re.sub('[a-z]', '', data)
print(res)