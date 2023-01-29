import cv2


# tracker = cv2.TrackerCSRT_create()

cap = cv2.VideoCapture("http://192.168.31.93/mjpeg")
print("cap")

selected = False


while True:


    ret, frame = cap.read()
    # key = cv2.waitKey(1)

    # if (ret == True and not selected) or (key == ord("r")) :
    #     cv2.putText(frame, "select object ", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    #     roi = cv2.selectROI(windowName="selectTarget", img=frame, showCrosshair=True, fromCenter=False)
    #     tracker.init(frame, roi)
    #     x, y, w, h = roi
    #     print(x, y, w, h)
    #     cv2.destroyWindow("selectTarget")
    #     selected = True
    #
    # success, bbox = tracker.update(frame)

    if ret == True:
        # if success:
        #     p1 = (int(bbox[0]), int(bbox[1]))
        #     p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        #     cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        # else:
        #     cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        cv2.imshow('video', frame)
    else:
        print("ret=false")

    if cv2.waitKey(1) == 27:
            exit(0)




# img = cv2.imread("/Users/junjun/Documents/地球上线/图片 1.png")
# roi = cv2.selectROI(windowName="test", img = img, showCrosshair=True, fromCenter=False)
# x,y,w,h = roi
# cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
# cv2.imshow("roi", img)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()