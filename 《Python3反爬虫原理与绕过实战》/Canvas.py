import time

from selenium import webdriver
from selenium.webdriver.common.by import By
browser = webdriver.Chrome() # 驱动Chrome浏览器打开滑动验证码示例页面
browser.get('http://www.porters.vip/captcha/jigsawCanvas.html')
# time.sleep(2)

# 定位滑块
jigsawCircle = browser.find_element(By.CSS_SELECTOR,'#jigsawCircle')

# 定位背景图片
jigsawCanvas = browser.find_element(By.CSS_SELECTOR,'#jigsawCanvas')
jigsawCanvas.screenshot('before.png')
action = webdriver.ActionChains(browser)

# 点击并保持不松开
action.click_and_hold(jigsawCircle).perform()

# 执行JavaScript隐藏圆角矩形的HTML代码
scripts = """ var missblock = document.getElementById('missblock'); missblock.style['visibility'] = 'hidden'; """
browser.execute_script(scripts)

# 再次截图
jigsawCanvas.screenshot('after.png')


from PIL import Image

# 打开待对比的图片
image_a = Image.open('after.png').convert('RGB')
image_b = Image.open('before.png').convert('RGB')

from PIL import ImageChops

# 使用ImageChops模块中的differencd()方法对比图片像素的不同
diff = ImageChops.difference(image_a, image_b)

# 获取图片差异位置坐标,getbbox()方法会返回图片差异的坐标信息，坐标顺序为：左、上、右、下。
diff_position = diff.getbbox()
print(diff_position)

position_x = diff_position[0]
# 设置移动距离
action.move_by_offset(int(position_x) - 10, 0)
action.release().perform()

