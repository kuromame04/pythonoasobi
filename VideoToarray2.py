import numpy
import cv2
import time
import numba
import ffmpeg 
import playsound
import asyncio
import threading
import shutil # TODO Windowサイズに合わせてレンダリングサイズを自動調整
import sys

f=open(r"./result.txt",mode="w")
path=r"badapple"

def mp4tomp3(path): # FFmpegパス通ってねーじゃねーか　ころすぞー☆
    try:
        stream=ffmpeg.input(f"{path}.mp4")
        stream=ffmpeg.output(stream,f"{path}.mp3")
        ffmpeg.run(stream)
        return True
    except  Exception as e:
        print(e); return False
        
def thread():
    playsound.playsound(f"{path}.mp3")
        
res=mp4tomp3(path)

if res ==False:
    print("FFmpegERROR")
    sys.exit(0)

terminal_size = shutil.get_terminal_size()

array=cv2.VideoCapture(f"{path}.mp4")
fps=array.get(cv2.CAP_PROP_FPS)
framearray=[]
frame_spilit=10
x_split=array.get(cv2.CAP_PROP_FRAME_WIDTH)//terminal_size.columns
y_split=array.get(cv2.CAP_PROP_FRAME_HEIGHT)//terminal_size.lines-1

if  array.isOpened():
    frame_count=0
    while True:
        frame_count+=1 
        ret,frame=array.read()
        if ret==False:
            break
        if array.get(cv2.CAP_PROP_POS_FRAMES) %frame_spilit==0:
            dataarray=[]
            for i,data in enumerate(frame):
                if i %y_split==0:
                    pixelarray=[]
                    for r,datax in enumerate(data):
                        if r %x_split==0:
                            R,G,B=frame[i][r]
                            #if R >=127 or G >=127 or B >=127:
                                #frame[i][r]=[0,0,0]
                                #pixelarray.append(frame[i][r])
                            #elif R <=128 or G <=128 or B <=128:
                                #frame[i][r]=[255,255,255]
                            pixelarray.append(frame[i][r])
                    dataarray.append(pixelarray)
            print(f"{(frame_count/frame_spilit)}  {str(len(pixelarray))}")# framearray[frame]dataarray[y][pixel] | framearray[][][]
            framearray.append(dataarray)
    thread1=threading.Thread(target=thread)
    thread1.start()
    for i in framearray:
        for r in i: 
            list=[]
            for s in r:
                
                list.append(str(chr(97+s[0].tolist()//32+s[1].tolist()//32+s[2].tolist()//32)))
            print("".join(list))
        time.sleep(frame_spilit/fps)
        print("\033[2J") # ここすると遅くなる疑惑ある
    f.write(str(framearray))
    f.close()
else:
    print("error")
    

