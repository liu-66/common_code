#coding: utf-8
import cv2
import numpy as np
import imutils

# 填充孔洞
def fillHole(im_in):
    im_floodfill = im_in.copy()

    # 用于填充的面罩,大小需要比图像长 2 像素。
    h, w = im_in.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # 从点(0,0)进行洪水填充
    cv2.floodFill(im_floodfill, mask, (0,0), 255);

    # 反转泛洪图像
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # 组合两个图像以获取前景
    im_out = im_in | im_floodfill_inv

    return im_out


capture = cv2.VideoCapture()

while True:

    #ret, frame = cap.read()
    frame = cv2.imread("1.jpg")
    #frame = cv2.resize(frame,(820,616),)

    # HSV颜色区间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(30,30))
    # 腐蚀
    mask=cv2.erode(mask,kernel)
    # 膨胀
    mask=cv2.dilate(mask,kernel)


    # 描边
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #填充孔洞
    mask = fillHole(mask)

    for n in range(len(contours)):

        cnt = contours[n]

        # 最小外接圆
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (255, 0, 0), 2)

        # 中心点
        cv2.circle(frame, centre, 4, (0, 255, 255), -1)
        # 标出中心的坐标
        cv2.putText(frame, "{}centre:{},{}".format(n,x,y), (x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # 画线
        cv2.line(frame, centre, centre, (0,255,255), 3)
        
        # 提取与绘制轮廓
        cv2.drawContours(frame, contours, n, (0, 255, 0), 2)

        # 外接矩形框，没有方向角
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 最小外接矩形框，有方向角
        rect = cv2.minAreaRect(cnt)
        box = cv2.cv.Boxpoints() if imutils.is_cv2()else cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

        # 椭圆拟合
        ellipse = cv2.fitEllipse(cnt)
        cv2.ellipse(frame, ellipse, (255, 255, 0), 2)

        # 直线拟合
        rows, cols = frame.shape[:2]
        [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
        lefty = int((-x * vy / vx) + y)
        righty = int(((cols - x) * vy / vx) + y)
        frame = cv2.line(frame, (cols - 1, righty), (0, lefty), (0, 255, 255), 2)

    cv2.imshow("frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break