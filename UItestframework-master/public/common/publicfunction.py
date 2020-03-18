#coding=utf-8

# 截图放到report下的img目录下
def get_img(dr, img_path,filename):
    path = img_path + '\\' + filename
    dr.take_screenshot(path)

