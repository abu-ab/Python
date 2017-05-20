# -*- coding: utf-8 -*-：
import re
import zlib
import cv2


def face_detect(path):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("/home/jhy/haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

    if len(rects) == 0:
        return False

    rects[:, 2:] += rects[:, :2]
    # 对图像中的人脸进行高亮的显示处理
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (172, 255, 0), 2)
        cv2.imwrite("/home/jhy/hahahahaha.jpg", img)

    return True


print face_detect("/home/jhy/img/1.jpg")