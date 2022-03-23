# lange = {'1':'11', '2':'22', '3':'33'}
# for key, values in lange.items():
#     print(key+values)

data = ['1','2','3','4','5','6','7']
res = zip(data)
for i in res:
    print(i[0])
print(''.join(data))
dd = ''
for i in data:
    dd = dd + i
print(dd)