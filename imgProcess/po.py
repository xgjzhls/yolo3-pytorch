import cv2
import numpy as np
from matplotlib import pyplot as plt
import random
from handleXml import handleXml 
import os
def img_resize(image):
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架
    multi=round(random.random()*2) + 1
    # print(multi)
    width_new = width*multi
    height_new = height*multi
    # 判断图片的长宽比率
    if width / height >= width_new / height_new:
        img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
    else:
        img_new = cv2.resize(image, (int(width * height_new / height), height_new))
    return img_new

def pole(image):
    GrayImage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret,thresh1=cv2.threshold(GrayImage,250,255,cv2.THRESH_BINARY)
    return thresh1

def generatePadding(minPadding,maxPadding):

    top=random.randint(minPadding,maxPadding)
    bottom=maxPadding-top
    left=random.randint(minPadding,maxPadding)
    right=maxPadding-left
    return [top,bottom,left,right]

def getOriginalPadding(image):
    image=np.array(image)
    top=0
    bottom=0
    left=0
    right=0
    willBreak=False
    for rowIndex in range(0,len(image)):
        for column in image[rowIndex]:
            if column != 255:
                top=rowIndex
                willBreak=True
                break
        if willBreak==True:
            break
    
    willBreak=False
    for rowIndex in range(0,len(image)):
        for column in image[-rowIndex-1]:
            if column != 255:
                bottom=rowIndex
                willBreak=True
                break
        if willBreak==True:
            break
    willBreak=False
    image=np.transpose(image)
    for columnIndex in range(0,len(image)):
        for row in image[columnIndex]:
            if row != 255:
                left=columnIndex
                willBreak=True
                break
        if willBreak==True:
            break

    willBreak=False
    for columnIndex in range(0,len(image)):
        for row in image[-columnIndex-1]:
            if row != 255:
                right=columnIndex
                willBreak=True
                break
        if willBreak==True:
            break
    return [top,bottom,left,right]

imgPath='D:\\imgProcess\\train_multi_en_JPEGImages'     
xmlPath='D:\\imgProcess\\train_multi_en_Annotations'
imgOutputPath='D:\\imgProcess\\train_multi_en_JPEGImages_output'     
#获取该目录下所有文件，存入列表中
imgList=os.listdir(imgPath)

xmlHandler=handleXml(imgPath,xmlPath)
for i in imgList:
    
    #设置旧文件名（就是路径+文件名）
    # oldname=path+ os.sep + i   # os.sep添加系统分隔符
    name=i.split('.')[0]
    #设置新文件名
    # newname=path + os.sep +name+'.jpg'
    
    # os.rename(oldname,newname)   #用os模块中的rename方法对文件改名
    # print(oldname,'======>',newname)
    
    # 读图
    data = np.fromfile(f'{imgPath}\\{i}', dtype=np.uint8)  #先用numpy把图片文件存入内存：data，把图片数据看做是纯字节数据
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)  #从内存数据读入图片
    # img=cv2.imread(f'{imgPath}\\{i}') 
    # print(f'{imgPath}\\{i}')
    # 分辨率+
    img=img_resize(img) 
    # 二值化
    img=pole(img) 
    img_height,img_width=img.shape
    # 获取原图padding
    res=getOriginalPadding(img) 
    # print(res)
    top,bottom,left,right=generatePadding(30,200)
    # (上, 下) (左, 右) (上左, 右下)
    # 添加背景padding
    img=np.pad(img,((top,bottom),(left,right)),'constant',constant_values = (255,255))  

    # label坐标
    coord={
        'xmin':left+res[2],
        'ymin':top+res[0],
        'xmax':left+img_width-res[3],
        'ymax':top+img_height-res[1],
    }
    # 写入XML
    # label=name[0]
    label=i.split('_')
    label=label[0]+'_'+label[1]
    xmlHandler.writeXml(i,coord,label)
    # 写入新图片
    # cv2.imwrite(f'{imgOutputPath}\\{i}', img)  
    cv2.imencode('.jpg',img)[1].tofile(f'{imgOutputPath}\\{i}')