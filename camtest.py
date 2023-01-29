#esp32 microPython with camudpserver.py 实时追踪物体

import socket
import cv2
import io
from PIL import Image
import numpy as np


# 上下翻转

def RotateClockWise180(img):

    new_img=np.zeros_like(img)

    h,w=img.shape[0],img.shape[1]

    for i in range(h): #上下翻转

        new_img[i]=img[h-i-1]

    return new_img

cammodel = "ov5640"     #ov2640 ov5640

serverport = 9090
camport = 81
camip = "192.168.1.6"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind(("0.0.0.0", serverport))

try:
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    client.sendto(str(serverport).encode(), (camip, camport))
except Exception as e:
    print(e)
    exit(0)

print("connected,start to recv cam")

selected = False
tracker = cv2.TrackerCSRT_create()
imgwith = 480
imghight = 320

while True:
    data, IP = s.recvfrom(100000)
    # print("recv len", len(data))
    bytes_stream = io.BytesIO(data)
    image = Image.open(bytes_stream)
    img = np.asarray(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32采集的是RGB格式，要转换为BGR（opencv的格式）

    if cammodel == "ov5640":
        img = RotateClockWise180(img)

    key = cv2.waitKey(1)

    if key == ord("r"):
        cv2.putText(img, "select object ", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        roi = cv2.selectROI(windowName="selectTarget", img=img, showCrosshair=True, fromCenter=False)
        tracker.init(img, roi)
        x, y, w, h = roi
        print(x, y, w, h)
        cv2.destroyWindow("selectTarget")
        selected = True

    if selected:

        success, bbox = tracker.update(img)
        # print(success)

        if success:
            #bbox0,bbox1左顶点xy坐标，bbox2宽，bbox3高
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            p3 = (int(imgwith/2-w/2), int(imghight/2-h/2))
            p4 = (int(imgwith/2+w/2), int(imghight/2+h/2))
            # print("p1", p1)
            # print("p2", p2)
            # print("p3", p3)
            # print("p4", p4)
            cv2.rectangle(img, p1, p2, (255, 0, 0), 2, 1)
            cv2.rectangle(img, p3, p4, (0, 0, 255), 2, 1)
        else:
            cv2.putText(img, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)


    cv2.imshow('video', img)

    if cv2.waitKey(1) == 27:
        print("exit")
        client.sendto(str(0).encode(), (camip, camport))
        client.close()
        exit(0)

    # if cv2.waitKey(1) == ord("q"):
    #     print("quit")
    #     break

