import pytesseract
from PIL import Image,ImageFilter
import cv2

def recognize(imgName):
    #使用路径导入图片
    im = Image.open(imgName)
    # 转化到灰度图
    imgry = im.convert('L')
    # 保存图像
    # imgry.save('g-' + imgName)
    # 二值化，采用阈值分割法，threshold为分割点
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    # out.save('b-' + imgName)
    #  识别
    out = out.resize((120, 38))
    # out.save('re-'+imgName)
    text = pytesseract.image_to_string(out)
    return text

def open_img(giffile):
    img = Image.open(giffile)
    img = img.convert('RGB')
    pixdata = img.load()
    return img,pixdata

def removeLine(imgName):
    (img, pixdata) = open_img(imgName)
    for x in range(img.size[0]):  # x坐标
        for y in range(img.size[1]):  # y坐标
            if pixdata[x, y][0] < 8 or pixdata[x, y][1] < 6 or pixdata[x, y][2] < 8 or (
                    pixdata[x, y][0] + pixdata[x, y][1] + pixdata[x, y][2]) <= 30:  # 确定颜色阈值
                if y == 0:
                    print("a")
                    pixdata[x, y] = (0, 0, 0)
                if y > 0:
                    if pixdata[x, y - 1][0] > 120 or pixdata[x, y - 1][1] > 136 or pixdata[x, y - 1][2] > 120:
                        pixdata[x, y] = (255, 255, 255)  # ?
                        print("b")
        # 二值化处理
    for y in range(img.size[1]):  # 二值化处理，这个阈值为R=95，G=95，B=95
        for x in range(img.size[0]):
            if pixdata[x, y][0] < 160 and pixdata[x, y][1] < 160 and pixdata[x, y][2] < 160:
                pixdata[x, y] = (0, 0, 0)
                print("c")
            else:
                pixdata[x, y] = (255, 255, 255)
                print("d")

    img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # 深度边缘增强滤波，会使得图像中边缘部分更加明显（阈值更大），相当于锐化滤波
    img.resize(((img.size[0]) * 2, (img.size[1]) * 2), Image.BILINEAR)
    # Image.BILINEAR指定采用双线性法对像素点插值
    new_address = 'F:\SoftwareEngineeing\Python\pics\\' + 'r-' + imgName
    img.save(new_address)
    print("除线成功！")
    recognize(new_address)


print(removeLine('image2.gif'))