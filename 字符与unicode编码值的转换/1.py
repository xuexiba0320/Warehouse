

s = u'\x77\x71\x66\x44\x6c\x43\x67\x3d'

s2 = s.encode('raw_unicode_escape').decode('utf-8')
print(s2)


a = '\x77\x71\x66\x44\x6c\x43\x67\x3d'
print(a.encode().decode())