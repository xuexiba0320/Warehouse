name = '王张里吴李周李陈王杨张吴周王刘赵黄吴杨李'

myname = set(name)
print(myname)
newname = list(myname)
print(newname)
data = ''.join(newname)
print(data)
newname.sort(key=name.index)
print(newname)
data = ''.join(newname)
print(name)
print(data)

print('************************')

zd={}.fromkeys(name)
print(zd)
mylist = list(zd.keys())
print(''.join(mylist))