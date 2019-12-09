import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

cap = cv2.VideoCapture(1)

while True:
    # 等待视频流
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()

    width = int(depth_frame.get_width()/2)
    height = int(depth_frame.get_height()/2)
    #print(width)
    #print(height)

    # 拿到距离信息
    dist = 0
    for y in range(width-5,width+5):
        for x in range(height-5,height+5):
            dist += depth_frame.get_distance(x, y)
    print(dist/100)

    if dist < 1:
        ret, color_frame = cap.read()
        color_frame = cv2.resize(color_frame,(640,480))
        cv2.imwrite("img.png",color_frame)