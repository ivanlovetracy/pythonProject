import socket
import cv2
import io
from PIL import Image
import numpy as np

# Image.LOAD_TRUNCATED_IMAGES = True

ip = "192.168.1.6"
port = 81
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((ip, port))
except:
    s.close()
    print("connect error")
    exit(0)

print("connected")

while True:
    data, IP = s.recv(100000)
    # print(data)
    print("buflen", len(data))
    bytes_stream = io.BytesIO(data)
    print(bytes_stream)
    # if not bytes_stream.endswith(b'\xff\xd9'):
    #     bytes_stream = bytes_stream + b'\xff\xd9'
    image = Image.open(bytes_stream)
    img = np.asarray(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32采集的是RGB格式，要转换为BGR（opencv的格式）
    cv2.imshow("ESP32 Capture Image", img)
    if cv2.waitKey(1) == ord("q"):
        break
