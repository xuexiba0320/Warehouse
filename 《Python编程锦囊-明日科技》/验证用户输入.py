# text= input()
# if text.isdigit():
#     print('ok')
#
# if str.isdigit(text):
#     print('ok2')

data = '123456789'
for i in range(0,9,1):
    print(data[i], end='')
print('\n')
for i in range(8,-1,-1):
    print(data[i], end='')