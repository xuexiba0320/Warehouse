import base64

a = "this is a test"
bs64 = base64.b64encode(a.encode('utf-8'))  # 对字符串编码
print(bs64)
'''
结果：
>>>: b'dGhpcyBpcyBhIHRlc3Q='
'''
debs64 = base64.b64decode(bs64)   # 对base64编码进行解码
print(debs64)

'''
结果：
>>>: b'this is a test'
'''
