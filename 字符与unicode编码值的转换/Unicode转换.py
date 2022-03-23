 # 将Unicode转换成普通的Python字符串:"编码(encode)"

from urllib.parse import unquote, quote

from numpy.compat import unicode

unicodestring = '27721'

utf8string = unicodestring.encode("utf-8")
print(utf8string)
asciistring = unicodestring.encode("ascii")
print(asciistring)

isostring = unicodestring.encode("ISO-8859-1")
print(asciistring)

utf16string = unicodestring.encode("utf-16")
print(utf16string)

# 将普通的Python字符串转换成Unicode: "解码(decode)"

plainstring1 = unicode(utf8string, "utf-8")
print(plainstring1)

plainstring2 = unicode(asciistring, "ascii")
print(plainstring2)

plainstring3 = unicode(isostring, "ISO-8859-1")
print(plainstring3)

plainstring4 = unicode(utf16string, "utf-16")
print(plainstring4)

assert plainstring1 == plainstring2 == plainstring3 == plainstring4