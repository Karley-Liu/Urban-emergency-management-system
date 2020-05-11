import datetime

import cv2
import os
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from record.models import Record


def record(request):
    return render(request,'admin/record.html')

def startRecord(request):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('U','2','6','3')
    dt=datetime.date.today()
    outfile = 'static/video/{}.mp4'.format(dt)
    out = cv2.VideoWriter('../../Envs/virtual_env/Lib/site-packages/simpleui/{}'.format(outfile),fourcc,30.0,(640,480))


    while(cap.isOpened()):
        ret,frame = cap.read()

        if ret == True:
            frame = cv2.flip(frame,1)
            out.write(frame)

            cv2.imshow('camera',frame)
            if cv2.waitKey(1) & 0xFF == ord('1'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    rd = Record.objects.filter(datetime=dt).first()
    if rd:
        pass
    else:
        rd = Record(record_url=outfile,datetime=dt)
        rd.save()
    return JsonResponse({"res":"请求成功"})


def checkRecord(request,video_id):
    videoID = video_id
    record = Record.objects.filter(id=videoID).first()

    videoURL = record.record_url
    def on_change(x):
        # 设置播放的帧数
        cap.set(cv2.CAP_PROP_POS_FRAMES, x)
    # 调用摄像头
    cap = cv2.VideoCapture('../../Envs/virtual_env/Lib/site-packages/simpleui/{}'.format(videoURL))
    cv2.namedWindow("frame",cv2.WINDOW_AUTOSIZE)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cv2.createTrackbar("Frame", "frame", 0, int(frame_count), on_change)
    # 定义HOG对象，采用默认参数，或者按照下面的格式自己设置
    defaultHog = cv2.HOGDescriptor()
    # 设置SVM分类器，用默认分类器
    defaultHog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    c = 2
    timeF = 3
    while 1:
        framePos = cap.get(cv2.CAP_PROP_POS_FRAMES)
        cv2.setTrackbarPos("Frame", "frame", int(framePos))
        ret, frame = cap.read()
        img = frame
        (h, w) = img.shape[:2]
        width = 900
        r = width / float(w)
        dim = (width, int(h * r))
        if ret:
            # 获取摄像头拍摄到的画面
            if (c % timeF == 0):
                # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                (peoples, weights) = defaultHog.detectMultiScale(img, winStride=(4, 4), padding=(8, 8), scale=1.4)
                # peoples = np.array([[x, y, x + w, y + h] for (x, y, w, h) in peoples])
                # pick = non_max_suppression(peoples, probs=None, overlapThresh=0.65)
                for (x, y, w, h) in peoples:
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # print(type(peoples))
                num_p = len(peoples)
                # print(num_p)
                txt = 'Current have peoples:{}\nq:quit the frame'.format(str(num_p))
                y,dy = 0,20
                for i, line in enumerate(txt.split('\n')):
                    y += dy
                    cv2.putText(img,line,(10,y),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),2)
                # 实时展示效果画面
                cv2.imshow('frame', img)
                # 每5毫秒监听一次键盘动作
                if cv2.waitKey(50) & 0xFF == ord('q'):
                    break
            c += 1
            # print(c)

        else:
            break

    cv2.destroyAllWindows()
    cap.release()
    return JsonResponse({"res":"调用成功"})