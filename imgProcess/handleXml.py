import re
from PIL import Image
class handleXml:
    imgPath=''
    xmlPath=''
    imgName=''
    coord={
        'xmin':0,
        'ymin':0,
        'xmax':55,
        'ymax':55,
    }
    fileName=''
    def __init__(self,imgPath,xmlPath):
        self.imgPath="/".join(re.split(r"[/\\]",imgPath))
        self.xmlPath="/".join(re.split(r"[/\\]",xmlPath))
    def writeXml(self,imgName,coord,label):
        t=imgName.split('.')
        self.fileName = t[:-1][0]
        imgInfo = Image.open(self.imgPath+'/'+imgName).size
        file = open(f'{str(self.xmlPath)}/{str(self.fileName)}.xml', 'w',encoding='utf-8' )
        foler=self.xmlPath.split('/')[-1]
        file.write(
f'''<annotation>
    <folder>{foler}</folder>
    <filename>{imgName}</filename>
    <path>{self.imgPath}/{imgName}</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>{imgInfo[0]}</width>
        <height>{imgInfo[1]}</height>
        <depth>1</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>{label}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{coord['xmin']}</xmin>
            <ymin>{coord['ymin']}</ymin>
            <xmax>{coord['xmax']}</xmax>
            <ymax>{coord['ymax']}</ymax>
        </bndbox>
    </object>
</annotation>
'''
        )
# 使用方式
# imgPath='C:/imgs'
# xmlPath='C:/xmls'
# imgName='word1.png'
# coord={
#         'xmin':0,
#         'ymin':0,
#         'xmax':55,
#         'ymax':55,
#     }
# 实例化handleXml后输入img和xml文件夹的绝对路径
# temp=handleXml(imgPath,xmlPath)
# 输入img名字
# temp.writeXml(imgName,coord)
