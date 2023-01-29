#on pc with cam server picowebcamserver.py
import time

import cv2
import socket
import requests
import numpy as np
import time
import threading

from io import BytesIO
from PIL import Image

selected = False
tracker = cv2.TrackerCSRT_create()
imgwith = 320
imghight = 240

# camip = "192.168.1.6"
# camport = 80

# client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)

# def sendCmd():
#     print("sendCmd started")
#     for i in range(1,10):
#
#         print(i)
#         client.sendto(str(i).encode(), (camip, camport))
#         time.sleep(3)
#
#
# t = threading.Thread(target=sendCmd, args=())
# t.start()

# time.sleep(3)


res = requests.get('http://192.168.1.6:81/stream', stream=True)
print(res.status_code)

imageBytes = bytes()
for data in res.iter_content(chunk_size=300):
    # 输出data 查看每一张图片的开始与结尾，查找图片的头与尾截取jpg。并把剩余部分imageBytes做保存
    imageBytes += data
    a = imageBytes.find(b'\xff\xd8')
    b = imageBytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = imageBytes[a:b+2]
        imageBytes = imageBytes[b+2:]

        bytes_stream = BytesIO(jpg)
        img = Image.open(bytes_stream)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        key = cv2.waitKey(1)
        # if key == ord("a") or key == ord("b"):
        #     client.sendto(str(key).encode(), (camip, camport))


        if key == ord("r"):
            cv2.putText(img, "select object ", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
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
                # bbox0,bbox1左顶点xy坐标，bbox2宽，bbox3高
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                p3 = (int(imgwith / 2 - w / 2), int(imghight / 2 - h / 2))
                p4 = (int(imgwith / 2 + w / 2), int(imghight / 2 + h / 2))
                # print("p1", p1)
                # print("p2", p2)
                # print("p3", p3)
                # print("p4", p4)
                cv2.rectangle(img, p1, p2, (255, 0, 0), 2, 1)
                cv2.rectangle(img, p3, p4, (0, 0, 255), 2, 1)
            else:
                cv2.putText(img, "Tracking failure detected", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # cv2.resize(img, None, fx=2, fy=2)
        cv2.imshow('video', img)

        if cv2.waitKey(1) == 27:
            print("exit")
            cv2.destroyAllWindows()
            exit(0)


