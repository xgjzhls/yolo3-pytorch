# bin/bash
PATH=$PATH
prefix=train_multi_en_
rm -rf /d/oracle/yolov3-pytorch/VOCdevkit/VOC2007/Annotations
rm -rf /d/oracle/yolov3-pytorch/VOCdevkit/VOC2007/JPEGImages
cp -r /d/imgProcess/${prefix}Annotations /d/oracle/yolov3-pytorch/VOCdevkit/VOC2007/Annotations
cp -r /d/imgProcess/${prefix}JPEGImages_output /d/oracle/yolov3-pytorch/VOCdevkit/VOC2007/JPEGImages
/d/ProgramData/Anaconda3/envs/tfgpu220/python.exe /d/oracle/yolov3-pytorch/VOCdevkit/VOC2007/voc2yolo3.py
/d/ProgramData/Anaconda3/envs/tfgpu220/python.exe /d/oracle/yolov3-pytorch/voc_annotation.py