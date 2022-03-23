#encoding=utf-8
#author: walker
#date: 2014-05-15
#function: 更改图片尺寸大小
import os
import os.path
from PIL import Image
'''
filein: 输入图片
fileout: 输出图片
width: 输出图片宽度
height:输出图片高度
type:输出图片类型（png, gif, jpeg...）
'''
def ResizeImage(filein, fileout, width, height, type):
    img = Image.open(filein)
    out = img.resize((width, height),Image.ANTIALIAS) #resize image with high-quality
    out.save(fileout, type)

if __name__ == "__main__":
    filein = r'dataset\test_16472498047834163.png'
    fileout = r'dataset\tes2_16472498047834163.png'
    width = 100
    height = 60
    type = 'png'
    ResizeImage(filein, fileout, width, height, type)

