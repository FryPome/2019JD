from PIL import Image,ImageChops
from collections import defaultdict
import pytesseract
import sys

def get_line(bmp,w,h,n,width,threshold,color):
    print(n)
    if n == 0:
        print("n=0")
        for i in range(h):
            if bmp.getpixel((n,i)) == 1:
                width[n] = i;
                get_line(bmp, w, h, n+1, width, threshold,color);

    elif 0 < n < w-1:
        has_more = False;
        if 0 <= width[n-1] <= h-1:
            if bmp.getpixel((n,width[n-1])) == 1:
                width[n] = width[n-1];
                has_more = True;
                get_line(bmp, w,h,n+1, width, threshold,color);
        if width[n-1]-1 >= 0:
            # 越界处理
            if bmp.getpixel((n,width[n-1]-1)) == 1:
                width[n] = width[n-1] - 1;
                has_more = True;
                get_line(bmp,w,h, n+1, width, threshold,color);
        if width[n-1]+1 < h:
            if bmp.getpixel((n, width[n-1]+1)) == 1:
                width[n] = width[n-1]+1;
                print(width[n-1],"e")
                has_more = True;
                get_line(bmp, w, h, n+1, width, threshold,color);
        if n>=threshold and has_more== False:
            for j in range(w):
                if width[j] != -1:
                    bmp.putpixel((j,width[j]),0)
            return
    elif n == w-1:
        # 出口
        for j in range(w):
             if width[j] <= 0:
                bmp.putpixel((j,width[j]),255)
                print(j)
        print("cccccc")
    bmp.save('red-' + img_path)
    # exit(0)

def clear_line(b,wei,hei,threshold):
    width = {}
    for j in range(wei):
        width[j] = -1
    get_line(b,wei,hei,0,width,threshold,(0,0,0))
    return b

# 按照阈值进行二值化处理
# threshold: 像素阈值
# def get_bin_table(threshold=180):
#     # 获取灰度转二值的映射table
#     table = []
#     for i in range(256):
#         rate = 0.1  # 在threshold的适当范围内进行处理
#         if threshold * (1 - rate) <= i <= threshold * (1 + rate):
#             table.append(1)
#         else:
#             table.append(0)
#     return table

def get_bin_table(threshold=150):
    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

# 获取图片中像素点数量最多的像素
def get_threshold(image):
    pixel_dict = defaultdict(int)

    # 像素及该像素出现次数的字典
    rows, cols = image.size
    for i in range(rows):
        for j in range(cols):
            pixel = image.getpixel((i, j))
            pixel_dict[pixel] += 1
    count_max = max(pixel_dict.values())  # 获取像素出现出多的次数
    pixel_dict_reverse = {v: k for k, v in pixel_dict.items()}
    threshold = pixel_dict_reverse[count_max]  # 获取出现次数最多的像素点
    return threshold

def recognize(imgName):
    #使用路径导入图片
    im = Image.open(imgName)
    # 转化到灰度图
    imgry = im.convert('L')
    # 保存图像
    # imgry.save('g-' + imgName)
    # 二值化，采用阈值分割法，threshold为分割点
    # threshold = 140
    # table = []
    # for j in range(256):
    #     if j < threshold:
    #         table.append(0)
    #     else:
    #         table.append(1)
    # out = imgry.point(table, '1')
    # out.save('b-' + imgName)
    #  识别
    out = im.resize((120, 38))
    # out.save('re-'+imgName)
    text = pytesseract.image_to_string(out)
    return text

img_path = "image3.png"
img = Image.open(img_path)
# img = img.convert('L')  # 转化为灰度图
img = img.convert('L')
# 获取图片中的出现次数最多的像素，即为该图片的背景
# max_pixel = get_threshold(img)
# 将图片进行二值化处理
# print(max_pixel)
table = get_bin_table()
out = img.point(table, '1')
out.save('b-' + img_path)
w,h = out.size
bmp = clear_line(out, w, h, 140)
bmp.save("c-" + img_path)
text = recognize('c-' + img_path)
print("a"+text)


