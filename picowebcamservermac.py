# on esp32-cam with client mjpegclient.py

import picoweb
import ulogging as logging
import gc
import ujson
import network
import camera
import time
import _thread
import socket


def startCamServer():
    try:
        camera.init(0, format=camera.JPEG)
    except Exception as e:
        print("cam init fail")
        pass
    #     camera.deinit()
    #     print("cam reinit")
    #     time.sleep(1)
    #     camera.init(0, format=camera.JPEG)

    camera.flip(1)
    camera.framesize(camera.FRAME_QVGA)

    app = picoweb.WebApp(__name__)

    def send_frame():
        while True:
            buf = camera.capture()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf)
            del buf
            gc.collect()

    @app.route("/stream")
    def index_mjpeg(req, resp):
        yield from picoweb.start_response(resp, content_type="multipart/x-mixed-replace; boundary=frame")
        while True:
            yield from resp.awrite(next(send_frame()))
            gc.collect()

    logging.basicConfig(level=logging.INFO)

    print("start camserver")
    app.run(debug=True, host=ip, port=camport)


def startCmdServer():
    cmdServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    cmdServer.bind((ip, cmdport))
    print("udp cmdserver is listening on port", cmdport)

    while True:
        data, clientAddress = cmdServer.recvfrom(1024)
        print("recv cmd:", data)


sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
while not sta_if.isconnected():
    print('.')
    time.sleep(1)
    try:
        sta_if.connect('Xiaomi_4CDD_ykd', 'chr18929390642')
    except Exception as e:
        print(e)
        time.sleep(3)

ip, mask, gateway, dns = sta_if.ifconfig()
camport = 81
cmdport = 80
print("ip:", ip)
time.sleep(3)

# 创建互斥锁
gLock = _thread.allocate_lock()

# 获得互斥锁
gLock.acquire()

# 创建线程1
t1 = _thread.start_new_thread(startCmdServer, ())

# 休眠
time.sleep(5)

# 释放互斥锁
gLock.release()

# gLock.acquire()
# t2 = _thread.start_new_thread(startCamServer, ())
# time.sleep(5)
# gLock.release()

startCamServer()

# print("camserver,cmdserver are running on thread:")

