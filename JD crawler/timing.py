import matplotlib.pyplot as plt
import cv2

# 读取图像
good_img = cv2.imread('image3.png')  # 可以读取tif格式图片
# img.show()              #显示图像

gen_img = cv2.imread('red.png')

err = cv2.absdiff(good_img, gen_img)
cv2.imshow('err', err)
